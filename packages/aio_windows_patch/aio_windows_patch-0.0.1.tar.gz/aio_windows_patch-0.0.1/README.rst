aio_windows_patch
===============================

* version: 0.0.1
* status: dev
* author: hsz
* email: hsz1273327@gmail.com

Desc
--------------------------------

The python version so far has poorly supported windows. One of the most troubling things is
 `loop.add_signal_handler` can not deal with the signal on windows.

This project is asyncio's patch which can deal with problem ,It's from https://codereview.appspot.com/119990043/.

One day python will fix this problem. Then I will delete this program.


keywords:asyncio,patch


Feature
----------------------

* loop.add_signal_handler can deal with the signal on windows

Example
-------------------------------

.. code:: python

    import aio_windows_patch as asyncio

    ....

Install
--------------------------------

- ``python -m pip install aio_windows_patch``




