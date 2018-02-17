"""
Use setup tools to setup recho as a standard python package
"""
import os
from setuptools import find_packages, setup

# Get the long description from the README file
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="recho",
    author='Levi Noecker',
    author_email='levi.noecker@gmail.com',
    url='https://github.com/levi-rs/recho',
    keywords='reddit slack bot slackbot recho chat chatbot',
    description='repost Reddit activity from a user to Slack in near-realtime',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    use_scm_version={'root': '.', 'relative_to': __file__},
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configparser==3.5.0',
        'praw>=5.3.0',
        'raven',
        'slacker==0.9.30',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            'recho=recho.cli:main',
        ]
    },
)
