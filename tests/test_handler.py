from yasuf import Yasuf
from yasuf.yasuf import _handlers

y = Yasuf('test')

@y.handle('test')
def say_hey():
    print("Hey!")
    return "What's up!"

def test_handle():
    assert len(_handlers) == 2
    handler = _handlers.items()[0]
    assert len(handler) == 2
    regexp = handler[0]
    assert regexp.pattern == 'test'
