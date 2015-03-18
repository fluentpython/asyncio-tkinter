==========================
Using asyncio with Tkinter
==========================

The ``tkapp.py`` and ``tkapp2.py`` examples in this folder demonstrate:

- using an alternative ``asyncio.BaseEventLoop`` subclass on top of the Tkinter event loop;
- leveraging futures and `yield from` to escape *callback hell*;
- applying the ``asyncio`` abstractions to GUI programming instead of network programming;

The code is adapted from Dino Viehland's talk `Using futures for async GUI programming in Python 3.3 <http://lanyrd.com/2013/pycon/scdywd/>`_ presented at PyCon US 2013. Dino's example used Tulip because Python 3.4 was under development therefore ``asyncio`` was not available in the standard library.

Luciano Ramalho updated this code to run with Python 3.4 with help and encouragement from Guido van Rossum. See `relevant thread <https://groups.google.com/d/msg/python-tulip/TaSVW-pjWro/QO07gF9dreEJ>`_ in the ``python-tulip`` group.
