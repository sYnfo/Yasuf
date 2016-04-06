[![Build Status](https://travis-ci.org/sYnfo/Yasuf.svg?branch=master)](https://travis-ci.org/sYnfo/Yasuf)

# Yasuf — Yet Another Slack, Ummm, Framework
Very simple way of controlling your Python application via Slack.

Yasuf consists of a single, simple decorator that allows you to execute the decorated function via Slack and get it's output back, without modifying the function in any way.

Let's say you have a function `say_hello` that takes a single integer argument, prints out "Hello!" that many times and returns string describing how many times it has done so:

```
def say_hello(count):
    for i in range(count):
        print("Hello!")
    return "I've just said Hello! {} times!".format(count)
```

Controlling this function is as simple as decorating it with the `yasuf.handle` decorator:

```
from yasuf import Yasuf

yasuf = Yasuf('slack-token', channel='#general')
```

The first argument is your token which you can get [here](https://api.slack.com/docs/oauth-test-tokens) and `channel` specifies the default channel Yasuf will be listening to.

```
@yasuf.handle('Say hello ([0-9]+) times!', types=[int])
def say_hello(count):
    (...)
```

The first argument of `handle` specifies the regexp that the function should respond to, where each capture group corresponds to one argument of the decorated function and `types` is a list of functions that will be applied to the captured arguments to convert them from string to whatever the decorated function expects.

Now you can run (or run_async).

```
yasuf.run()
```

From now on whenever you type `Say hello 3 times!` Yasuf will response with a couple hellos. Or you can ask Yasuf what he knows with the built-in function 'help'.

## Installation
```python3 -m pip install --user yasuf```
