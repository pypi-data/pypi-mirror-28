from setuptools import setup, find_packages
from seaborn.games.git_commands import *

TAB = '\n\t\t'
PREFIX = 'seaborn.games.git_commands:'
entry = TAB[1:]+'[console_scripts]' + TAB + \
        'seaborn_install=seaborn.games.git_commands:seaborn_install' + TAB + \
        'seaborn_uninstall=seaborn.games.git_commands:seaborn_uninstall'
for k in FUNCS.keys():
    entry += TAB + 'seaborn_'+k+'='+PREFIX+'seaborn_'+k
    entry += TAB + 'iter_'+k+'='+PREFIX+'iter_'+k

setup(
    name='seaborn-games',
    version='0.0.1',
    description='SeabornGames installs all of the SeabornGames repositories',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/File',
    download_url='https://github.com/SeabornGames/Games/tarball/download',
    keywords=[],
    install_requires=[
    ],
    extras_require={
    },
    packages=['seaborn', 'seaborn.games'],
    # '['seaborn'] + ['seaborn.' + i
    #                         for i in find_packages(where='./seaborn')],
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    entry_points=entry
#   '''
#       [console_scripts]
#       seatest=seaborn.games.test_all:main
#       seaborn_status=seaborn.games.git_commands:seaborn_status
#       seaborn_commit=seaborn.games.git_commands:seaborn_commit
#       seaborn_push=seaborn.games.git_commands:seaborn_push
#       seaborn_pull=seaborn.games.git_commands:seaborn_pull
#   '''
)
