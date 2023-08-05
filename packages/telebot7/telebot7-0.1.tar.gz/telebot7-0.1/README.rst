================================================================
Framework for extract data from vk.com (russian social network).
================================================================

This is a Python wrapper for Telegram Bot API.

Quickstart
==========

Install
-------

.. code:: bash

    pip install telebot7

Usage
-----

.. code:: python

    >>> from telebot7 import TeleBot
    >>> from telebot7.long_polling import get_updates
    >>>
    >>> token = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
    >>> tele_bot = TeleBot(token)
    >>>
    >>> print(tele_bot.getMe())
    >>>
    >>> def on_updates(updates):
    ...    print(updates)
    ...
    >>> get_updates(tele_bot, on_updates, timeout=10)

See https://core.telegram.org/bots/api for detailed API guide.
