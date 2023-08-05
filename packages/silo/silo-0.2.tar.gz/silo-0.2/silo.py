#!/usr/bin/env python3.6
import os
import datetime
import inspect
import json
import sys
import syslog
import time
import functools
import uuid


################################################################################
# Processors
################################################################################

__syslog_codes = {
      0: 'LOG_KERN',     1: 'LOG_PID',        2: 'LOG_CRIT',     3: 'LOG_ERR',
      4: 'LOG_WARNING',  5: 'LOG_NOTICE',     6: 'LOG_INFO',     7: 'LOG_DEBUG',
      8: 'LOG_USER',    16: 'LOG_NOWAIT',    24: 'LOG_DAEMON',  32: 'LOG_PERROR',
     40: 'LOG_SYSLOG',  48: 'LOG_LPR',       56: 'LOG_NEWS',    64: 'LOG_UUCP',
     72: 'LOG_CRON',    80: 'LOG_AUTHPRIV', 128: 'LOG_LOCAL0', 136: 'LOG_LOCAL1',
    144: 'LOG_LOCAL2', 152: 'LOG_LOCAL3',   160: 'LOG_LOCAL4', 168: 'LOG_LOCAL5',
    176: 'LOG_LOCAL6', 184: 'LOG_LOCAL7'
}


def __silo_simple_format(msg):
    ''' Turns structured log messages into a simple text format
    '''
    assert isinstance(msg, dict), 'simple_format requires <dict> messages'
    ts = msg['timestamp']['iso'][:19]
    level = __syslog_codes.get(msg['level'], '')[4:] or msg['level']
    if 'audit' in msg:
        func = msg['audit'].get('function', None)
        callid = msg['audit'].get('callid', None)
        level = f'AUDIT {func} {callid}'
    fn, line = msg['context']['filename'], msg['context']['line']
    fn = os.path.split(fn)[-1] if os.path.exists(fn) else fn
    args = list(map(str, msg['args']))
    args += [f'{k}={v}' for k, v in msg['kwargs'].items()]
    return f'{ts} {level} ({fn}:{line}) ' + ', '.join(args)


def __silo_json_format(msg):
    ''' Converts log messages to JSON
    '''
    assert isinstance(msg, dict), 'json_format requires <dict> messages'
    return json.dumps(msg)


################################################################################
# Destinations
################################################################################

def __silo_stderr(msg):
    ''' Sends formated messages, i.e. strings, to stderr
    '''
    assert isinstance(msg, str), 'stderr requires log messages as text'
    print(msg, file=sys.stderr)


def __silo_syslog(msg):
    ''' Formats and logs messages in one step to syslog
    '''
    args = list(map(str, msg['args']))
    args += [f'{k}={v}' for k, v in msg['kwargs'].items()]
    filename, line = msg['context']['filename'], msg['context']['line']
    filename = os.path.split(filename)[-1] if os.path.exists(filename) else filename
    syslog.syslog(msg['level'], f'({filename}:{line}) ' + ', '.join(args))


################################################################################
# Internals
################################################################################

def __setup():
    chains = [
        [
            globals().get(step)
            for step in map(lambda s: f'__silo_{s}', os.environ.get(chain, '').split(':'))
            if step in globals()
        ]
        for chain in [name for name in os.environ if name.upper().startswith('SILO_')]
    ] or [ [__silo_simple_format, __silo_stderr] ]

    def output(msg):
        for chain in chains:
            cpy = msg
            for step in chain:
                new = step(cpy)
                if new:
                    cpy = new

    return output


__output = __setup()


def __log(level, *args, **kwargs):
    frame = inspect.stack()[2]
    __output({
        'level': level,
        'timestamp': {
            'iso': datetime.datetime.utcnow().isoformat()+'+00:00',
            'unix': time.time()
        },
        'context': {
            'function': frame.function,
            'filename': frame.filename,
            'line': frame.lineno
        },
        'args': args,
        'kwargs': kwargs,
    })


def __audit(function, callid, *args, **kwargs):
    frame = inspect.stack()[2]
    __output({
        'audit': {
            'function': function.__name__,
            'filename': inspect.getfile(function),
            'callid': callid
        },
        'level': syslog.LOG_NOTICE,
        'timestamp': {
            'iso': datetime.datetime.utcnow().isoformat()+'+00:00',
            'unix': time.time()
        },
        'context': {
            'function': frame.function,
            'filename': frame.filename,
            'line': frame.lineno
        },
        'args': args,
        'kwargs': kwargs,
    })


################################################################################
# Public API
# ------------------------------------------------------------------------------
#
# - Audit decorator factory
# - Low overhead debug function
# - Log-level shims
#
################################################################################

def audit(func):
    ''' Decorator that logs function entry and exit
    '''
    signature = inspect.signature(func)
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        callid = uuid.uuid4().hex[:8]
        __audit(func, callid, bound)
        res = func(*args, **kwargs)
        __audit(func, callid, result=res)
        return res
    return _wrapper


def emergency(*args, **kwargs):
    __log(syslog.LOG_EMERG, *args, **kwargs)


def alert(*args, **kwargs):
    __log(syslog.LOG_ALERT, *args, **kwargs)


def critical(*args, **kwargs):
    __log(syslog.LOG_CRIT, *args, **kwargs)


def error(*args, **kwargs):
    __log(syslog.LOG_ERR, *args, **kwargs)


def warning(*args, **kwargs):
    __log(syslog.LOG_WARNING, *args, **kwargs)


def notice(*args, **kwargs):
    __log(syslog.LOG_NOTICE, *args, **kwargs)


def info(*args, **kwargs):
    __log(syslog.LOG_INFO, *args, **kwargs)


# Low overhead debug function
if os.environ.get('DEBUG', False):
    def debug(*args, **kwargs):
        __log(syslog.LOG_DEBUG, *args, **kwargs)
else:
    def debug(*args, **kwargs):
        pass


################################################################################
# Helper to check silo configuration
################################################################################

if __name__ == '__main__':
    print('Debugging', 'enabled' if bool(os.environ.get('DEBUG', False)) else 'disabled')
    print()
    for chain in filter(lambda n: n.upper().startswith('SILO_'), os.environ):
        print(chain, os.environ.get(chain))

    emergency('silo test message')
    alert('silo test message')
    critical('silo test message')
    error('silo test message')
    warning('silo test message')
    notice('silo test message')
    info('silo test message')
    debug('silo test message')

    @audit
    def login(username, password):
        # do smart stuff here...
        return False

    try:
        login('duckie', 'secret')
    finally:
        info('done')
