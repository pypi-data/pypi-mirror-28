import sys
from setuptools import setup

if sys.version_info < (3, 5):
    raise Exception("Python 3.5 or higher is required. Your version is %s." % sys.version)

__version__ = ""
exec(open('efb_wechat_slave/__version__.py').read())

long_description = open('README.rst').read()

setup(
    name='efb-wechat-slave',
    namespace_package=['efb_wechat_slave'],
    version=__version__,
    description='WeChat Slave Channel for EH Forwarder Bot, based on WeChat Web API.',
    long_description=long_description,
    author='Eana Hufwe',
    author_email='ilove@1a23.com',
    url='https://github.com/blueset/efb-telegram-master',
    license='GPLv3',
    download_url='',
    keywords=['ehforwarderbot', 'EH Forwarder Bot', 'EH Forwarder Bot Slave Channel',
              'wechat', 'weixin', 'chatbot'],
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
        "itchat",
        "python-magic",
        "pillow",
        "pyqrcode",
        "xmltodict",
        "PyYaml"
    ],
    entry_points={
        'ehforwarderbot.slave': 'blueset.wechat = efb_wechat_slave.WeChatChannel'
    }
)
