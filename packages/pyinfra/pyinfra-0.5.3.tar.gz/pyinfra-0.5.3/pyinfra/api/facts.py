# pyinfra
# File: pyinfra/api/facts.py
# Desc: the facts API

'''
The pyinfra facts API. Facts enable pyinfra to collect remote server state which
is used to "diff" with the desired state, producing the final commands required
for a deploy.
'''

from __future__ import division, unicode_literals

from inspect import ismethod
from socket import (
    error as socket_error,
    timeout as timeout_error,
)

import click
import six

from gevent.lock import Semaphore
from paramiko import SSHException

from pyinfra import logger

from .util import get_arg_value, log_host_command_error, make_hash, underscore


# Index of snake_case facts -> CamelCase classes
FACTS = {}


def is_fact(name):
    return name in FACTS


def get_fact_names():
    '''
    Returns a list of available facts in camel_case format.
    '''

    return list(six.iterkeys(FACTS))


class FactMeta(type):
    '''
    Metaclass to dynamically build the facts index.
    '''

    def __init__(cls, name, bases, attrs):
        if attrs.get('abstract'):
            return

        # Get the an instance of the fact, attach to facts
        FACTS[underscore(name)] = cls


@six.add_metaclass(FactMeta)
class FactBase(object):
    abstract = True

    @staticmethod
    def default():
        '''
        Set the default attribute to be a type (eg list/dict).
        '''

    def process(self, output):
        return output[0]

    def process_pipeline(self, args, output):
        return {
            arg: self.process([output[i]])
            for i, arg in enumerate(args)
        }


def get_facts(state, name, args=None):
    '''
    Get a single fact for all hosts in the state.
    '''

    args = args or []

    # Create an instance of the fact
    fact = FACTS[name]()

    # If we're inactive: just return the defaults
    if not state.active:
        return {
            host.name: fact.default()
            for host in state.inventory
        }

    # Apply args or defaults
    sudo = state.config.SUDO
    sudo_user = state.config.SUDO_USER
    su_user = state.config.SU_USER
    ignore_errors = state.config.IGNORE_ERRORS

    # Get the current op meta
    current_op_hash = state.current_op_hash
    current_op_meta = state.op_meta.get(current_op_hash)

    # If inside an operation, fetch config meta
    if current_op_meta:
        sudo = current_op_meta['sudo']
        sudo_user = current_op_meta['sudo_user']
        su_user = current_op_meta['su_user']
        ignore_errors = current_op_meta['ignore_errors']

    # Make a hash which keeps facts unique - but usable cross-deploy/threads.
    # Locks are used to maintain order.
    fact_hash = make_hash((name, args, sudo, sudo_user, su_user, ignore_errors))

    # Lock!
    state.fact_locks.setdefault(fact_hash, Semaphore()).acquire()

    # Already got this fact? Unlock and return 'em
    if state.facts.get(fact_hash):
        state.fact_locks[fact_hash].release()
        return state.facts[fact_hash]

    # Execute the command for each state inventory in a greenlet
    greenlets = {}

    for host in state.inventory:
        if host in state.ready_host_names:
            continue

        # Work out the command
        command = fact.command

        if ismethod(command):
            # Generate actual arguments by pasing strings as jinja2 templates
            host_args = [get_arg_value(state, host, arg) for arg in args]

            command = command(*host_args)

        greenlets[host.name] = state.fact_pool.spawn(
            host.run_shell_command, state, command,
            sudo=sudo, sudo_user=sudo_user, su_user=su_user,
            print_output=state.print_fact_output,
        )

    hostname_facts = {}
    failed_hosts = set()

    # Collect the facts and any failures
    for hostname, greenlet in six.iteritems(greenlets):
        status = False
        stdout = []

        try:
            status, stdout, _ = greenlet.get()

        except (timeout_error, socket_error, SSHException) as e:
            kwargs = {}

            if not ignore_errors:
                kwargs['callback'] = lambda: failed_hosts.add(hostname)

            log_host_command_error(
                host,
                e,
                timeout=current_op_meta['timeout'],
                **kwargs
            )

        data = fact.default()

        if status and stdout:
            data = fact.process(stdout)

        hostname_facts[hostname] = data

    log_name = click.style(name, bold=True)

    if args:
        log = 'Loaded fact {0}: {1}'.format(log_name, args)
    else:
        log = 'Loaded fact {0}'.format(log_name)

    if state.print_fact_info:
        logger.info(log)
    else:
        logger.debug(log)

    # Check we've not failed
    if not ignore_errors:
        state.fail_hosts(failed_hosts)

    # Assign the facts
    state.facts[fact_hash] = hostname_facts

    # Release the lock, return the data
    state.fact_locks[fact_hash].release()
    return state.facts[fact_hash]


def get_fact(state, hostname, name):
    '''
    Wrapper around ``get_facts`` returning facts for one host or a function
    that does.
    '''

    # Expecting a function to return
    if callable(FACTS[name].command):
        def wrapper(*args):
            fact_data = get_facts(state, name, args=args)

            return fact_data.get(hostname)
        return wrapper

    # Expecting the fact as a return value
    else:
        # Get the fact
        fact_data = get_facts(state, name)

        return fact_data.get(hostname)
