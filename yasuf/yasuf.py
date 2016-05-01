import re
import atexit
import logging
import time
from threading import Thread

from slackclient import SlackClient 

from .utils import _redirect_output, YasufRuntimeException


_handlers = {}
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Yasuf:
    def __init__(self, token, channel='#general', username='Yasuf', debug=False):
        self.sc = SlackClient(token)
        self.channel = channel
        self.username = username
        self.start_time = None
        if debug:
            logger.setLevel(logging.DEBUG)

    def run_async(self):
        """ Creates a thread that monitors Slack messages and returns """

        atexit.register(self._say_bye)
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.start()

    def run(self):
        """ Monitors new Slack messages and responds to them """

        logger.info('Starting Yasuf')
        self.sc.rtm_connect()
        self._synchronize_time()
        for message in self._get_message():
            if message.get('type') == 'message' and 'text' in message:
                for trigger, fun in _handlers.items():
                    match = trigger.match(message['text'])
                    if match:
                        self._send_message('Executing {} with '\
                                           'arguments {}:'.format(fun.__name__,
                                                                  match.groups()))
                        self._handle_trigger(trigger, fun, match)

    def _handle_trigger(self, trigger, fun, match):
        def handle(trigger, fun, match):
            try:
                stdout, ret_val = fun.execute(match.groups())
            except YasufRuntimeException as e:
                output = 'Encountered an exception: {}'.format(e)
            else:
                output = ''
                if fun.capture_stdout:
                    output = '\n'.join(stdout.readlines())
                if fun.capture_return:
                    output += '\n'.join(['Return value:', str(ret_val)])
            self._send_message(output)
        t = Thread(target=handle, args=(trigger, fun, match))
        t.start()

    def _get_message(self):
        """ Yields new messages from Slack real time messaging system.
            Only messages newer than start_time are yielded. (see
            _synchronize_time) """

        while True:
            message = self.sc.rtm_read()
            if message and float(message[0].get('ts', 0)) > self.start_time:
                logger.debug('Yielding message "{0}"'.format(message))
                yield message[0]
            time.sleep(.1)

    def _send_message(self, text, channel=None, **kwargs):
        """ Sends a message to Slack. Channel defaults to Yasuf's default
            channel. Any extra keyword arguments are passed to Slack api_call. """

        logger.info('Sending message: {}'.format(text))
        response = self.sc.api_call('chat.postMessage', text=text,
                                    channel=channel or self.channel,
                                    username=self.username, **kwargs)
        return response

    def _synchronize_time(self):
        """ Sends a message and records channel local time. rtm_read seems
            to resend old messages when first connecting. We want to avoid
            reacting to those. """

        logger.info('Synchronizing time')
        response = self._send_message('Hello!')
        if not response['ok']:
            raise Exception(response['error'])
        else:
            self.start_time = float(response['ts'])
        logger.debug('Time synchronized at {0}'.format(self.start_time))

    def _say_bye(self):
        """ Notify user that Yasuf is quiting. """

        self._send_message("Yasuf is exiting!")
        print("Yasuf is exiting!")

    class handle():
        def __init__(self, trigger, channel=None, types=None, capture_return=True,
                     capture_stdout=True):
            self.regexp = re.compile(trigger)
            self.types = types
            self.capture_return = capture_return
            self.capture_stdout = capture_stdout

        def __call__(self, f):
            self.fun = _redirect_output(f)
            self.__name__ = f.__name__
            self.__doc__ = f.__doc__

            logger.debug('Adding trigger "{0}" for function "{1}"'.format(self.regexp.pattern,
                                                                          self.__name__))
            _handlers[self.regexp] = self

            return f

        def execute(self, groups):
            if self.types is not None:
                assert len(self.types) == len(groups)
                params = [t(g) for t, g in zip(self.types, groups)]
            else:
                params = groups
            logger.debug('Executing "{0}" with params "{1}"'.format(self.__name__,
                                                                    params))
            return self.fun(*params)

@Yasuf.handle('help ?([a-zA-Z0-9_-]+)?', capture_return=False)
def print_help(function=None):
    """ Default handler for help command:
        * "help" prints out a list of all handled functions
        * "help <function name>" prints out doc text of a function """

    if function is None:
        for trigger, handler in _handlers.items():
            if handler.__name__ == 'print_help':
                continue
            print('{} triggers {}'.format(trigger.pattern, handler.__name__))
    else:
        for trigger, handler in _handlers.items():
            if handler.__name__ == function:
                if handler.__doc__:
                    print('Doc text for function {}:'.format(function))
                    print(handler.__doc__)
                else:
                    print('No doc text for function {}'.format(function))
                break
        else:
            print('No such function.')
