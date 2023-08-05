# coding:utf-8
from distutils.core import setup
import os

setup(
    name         = 'cheat-zh',
    version      = '0.0.1',
    author       = 'Tacey Wong',
    author_email = 'xinyong.wang@qq.com',
    license      = 'GPL3',
    description  = 'cheat-zh基于cheat v2.2.3制作，添加中文支持.'
                   '支持交互式地创建和查看命令行作弊条,'
                   '它被设计用于帮助那些频繁使用命令行，'
                   '却还没频繁到记住它们的×nix系统管理员。',
    url          = 'https://github.com/taceywong/cheat',
    packages     = [
        'cheat',
        'cheat.cheatsheets',
        'cheat.test',
    ],
    package_data = {
        'cheat.cheatsheets': [f for f in os.listdir('cheat/cheatsheets') if '.' not in f]
    },
    scripts          = ['bin/cheat'],
    install_requires = [
        'pygments >= 1.6.0',
    ]
)
