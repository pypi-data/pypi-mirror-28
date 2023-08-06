Baymax, a simple telegram bot framework on top of Python asyncio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Work in progress

Requirements
~~~~~~~~~~~~

-  Python 3.6 or higher

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install baymax

Basic usage example
~~~~~~~~~~~~~~~~~~~

.. code:: python

    from baymax.bot import Bot

    bot = Bot('token')

    @bot.on('/start')
    async def start_handler(message):
        await bot.reply(message, 'Welcome!')

    bot.run()

Middleware example
~~~~~~~~~~~~~~~~~~

.. code:: python

    @bot.middleware
    async def message_logging_middleware(raw_update):
        bot.logger.info('New update received: %s', raw_update['update_id'])

..

    NOTE: All middleware functions should be coroutines for now, even if
    they do not have asynchronous actions.

Reply keyboard markup example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from baymax.markups import KeyboardButton, ReplyKeyboardMarkup

    @bot.on('/rate')
    async def rate_handler(message):
        await bot.reply(message, 'Rate me', reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton('⭐️'),
                    KeyboardButton('⭐️⭐️'),
                    KeyboardButton('⭐️⭐️⭐️')
                ]
            ], resize_keyboard=True, one_time_keyboard=True))

..

    NOTE: Reply markup API / objects will be changing, they are far from
    good now.


