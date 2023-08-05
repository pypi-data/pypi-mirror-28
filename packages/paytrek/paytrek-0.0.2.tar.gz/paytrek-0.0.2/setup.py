from setuptools import setup

setup(
    name='paytrek',
    package=['paytrek'],
    version='0.0.2',
    description='Python client library for Paytrek API',
    author='Erkan Ay',
    author_email='erkanaycom@gmail.com',
    url='https://github.com/paytrek/paytrek-python-client',
    keywords=['paytrek', 'client', 'payment', 'gateway'],
    install_requires=[
        "requests",
    ],
    classifiers=[],
)
