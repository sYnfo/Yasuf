from setuptools import setup, find_packages

setup(
    name='Yasuf',
    description='Simple framwork for executing python functions via Slack',
    url='https://github.com/sYnfo/Yasuf',
    version='0.5-dev',
    author='Matej Stuchlik',
    author_email='matej.stuchlik@gmail.com',
    packages=find_packages(),
    install_requires=[
        'slackclient',
    ]
)
