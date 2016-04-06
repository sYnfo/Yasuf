import mock

from yasuf import Yasuf
from yasuf.yasuf import _handlers

y = Yasuf('test')
y.sc.api_call = mock.Mock()

@y.handle('test')
def say_hey():
    print("Hey!")
    return "What's up!"

def test_handle():
    assert len(_handlers) == 2
    patterns = [r.pattern for r in _handlers]
    assert 'test' in patterns

def test_default_channel():
    assert y.channel == '#general'
    y._send_message('test')
    y.sc.api_call.assert_called_once_with('chat.postMessage', text='test',
                                          channel='#general', username='Yasuf')
    y._send_message('test', channel='#test')
    y.sc.api_call.assert_called_with('chat.postMessage', text='test',
                                     channel='#test', username='Yasuf')
