import sys
from setuptools import setup

if sys.version_info < (3, 5):
    raise Exception("Python 3.5 or higher is required. Your version is %s." % sys.version)

__version__ = ""
exec(open('efb_fb_messenger_slave/__version__.py').read())

long_description = open('README.rst').read()

setup(
    name='efb-fb-messenger-slave',
    namespace_package=['efb_fb_messenger_slave'],
    version=__version__,
    description='Facebook Messenger Slave Channel for EH Forwarder Bot, based on ``fbchat``.',
    long_description=long_description,
    author='Eana Hufwe',
    author_email='ilove@1a23.com',
    url='https://github.com/blueset/efb-fb-messenger-slave',
    license='GPL v3',
    keywords=['ehforwarderbot', 'EH Forwarder Bot', 'EH Forwarder Bot Master Channel',
              'facebook messenger', 'messenger', 'chatbot'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities"
    ],
    install_requires=[
        "ehforwarderbot",
        "fbchat",
        "PyYaml",
        'requests',
        'emoji'
    ],
    entry_points={
        "console_scripts": ["efms-auth = efb_fb_messenger_slave.__main__:main"],
        "ehforwarderbot.slave": ["blueset.fbmessenger = efb_fb_messenger_slave:FBMessengerChannel"]
    }
)
