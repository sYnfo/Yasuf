from yasuf.utils import _redirect_output, YasufRuntimeException

def test_redirect():
    def say_hey():
        print("Hey!")
        return "What's up!"

    redirected_f = _redirect_output(say_hey)
    output = redirected_f()
    assert output[0].readlines() == ["Hey!\n"]
    assert output[1] == "What's up!"

def test_redirect_exception():
    def raise_exception():
        raise Exception('Test Exception')

    redirected_f = _redirect_output(raise_exception)
    try:
        output = redirected_f()
    except YasufRuntimeException as e:
        assert e.message == "Exception('Test Exception',)"
