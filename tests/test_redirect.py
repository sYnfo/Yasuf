from yasuf.yasuf import _redirect_output

def say_hey():
    print("Hey!")
    return "What's up!"

def test_redirect():
    redirected_f = _redirect_output(say_hey)
    output = redirected_f()
    assert output[0].readlines() == ["Hey!\n"]
    assert output[1] == "What's up!"
