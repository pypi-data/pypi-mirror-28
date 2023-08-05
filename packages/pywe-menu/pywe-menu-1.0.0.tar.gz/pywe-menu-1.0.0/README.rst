=========
pywe-menu
=========

Wechat Menu Module for Python.

Sandbox
=======

* https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

Installation
============

::

    pip install pywe-menu


Usage
=====

::

    from pywe_menu import Menu, add_conditional, create_menu, del_conditional, del_menu, delete_menu, delete_conditional, get_current_selfmenu_info, get_menu, try_match


Method
======

::

    class Menu(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(Menu, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def create_menu(self, menus, appid=None, secret=None, token=None, storage=None):

    def get_menu(self, appid=None, secret=None, token=None, storage=None):

    def delete_menu(self, appid=None, secret=None, token=None, storage=None):

    def add_conditional(self, menus, appid=None, secret=None, token=None, storage=None):

    def del_conditional(self, menuid, appid=None, secret=None, token=None, storage=None):

    def try_match(self, user_id, appid=None, secret=None, token=None, storage=None):

    def get_current_selfmenu_info(self, appid=None, secret=None, token=None, storage=None):

