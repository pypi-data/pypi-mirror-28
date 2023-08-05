pypack.logger 1.0.0
===================

**pypack.logger** is logger for python3, simple to use and customize

Installation:
-------------

.. code-block:: sh

    pip install pypack.logger

Import and Example Usage:
-------------------------

.. code-block:: python3

    from pypack.logger import Logger

    >>> Logger.info('info message')
    2018 Jan 12 18:23:12 [ INFO] info message
        
    >>> Logger.info('info message', 1)
    2018 Jan 12 18:23:26 [ INFO] info message
    arg[0]:1
    -----------------------------------------

    >>> Logger.info('info message', 1, one='one')
    2018 Jan 12 18:24:08 [ INFO] info message
    arg[0]:1
    arg[one]:one
    -----------------------------------------




Method List:
------------

.. code-block:: python3

    Logger.error(message, *args, **kwargs)
    Logger.warn(message, *args, **kwargs)
    Logger.info(message, *args, **kwargs)
    Logger.debug(message, *args, **kwargs)
    Logger.trace(message, *args, **kwargs)


Customize Logs:
---------------

if you want to apply a custom settings to logger, edit those values

.. code-block:: python3

    # Align tag to largest Tag
    # Example: [ INFO] instad of  [INFO]
    Logger.ALIGN_TAG = True

    # Show date in log message
    Logger.SHOW_DATE = True

    # replace logging tag
    Logger.TAG_ERROR : str = 'ERROR'
    Logger.TAG_WARN  : str = 'WARN'
    Logger.TAG_INFO  : str = 'INFO'
    Logger.TAG_DEBUG : str = 'DEBUG'
    Logger.TAG_TRACE : str = 'TRACE'

    # replace tag braces
    Logger.BRACES_TAG : Tuple[str] = ('[', ']')

    # replace args display
    Logger.ARGS_MODE : str = 'arg[{}]:{}' # first is index, second is value

    # set date format
    # ISO compatible date format
    Logger.DATE_FORMAT : str = '%Y %b %d %H:%M:%S'

    # Show log to console
    Logger.TO_CONSOLE : bool = True

    # Append to log file
    Logger.LOG_FILE : Union(None, str, TextIO) = None

    # Custom callback after log
    Logger.CALLBACK : Callable = None

