import time, math, datetime

class Logger:

    ALIGN_TAG = True
    SHOW_DATE = True

    TAG_ERROR = 'ERROR'
    TAG_WARN  = 'WARN'
    TAG_INFO  = 'INFO'
    TAG_DEBUG = 'DEBUG'
    TAG_TRACE = 'TRACE'

    BRACES_TAG = ('[',']')

    ARGS_MODE = 'arg[{}]:{}'

    DATE_FORMAT = '%Y %b %d %H:%M:%S'

    LOG_FILE   = None
    TO_CONSOLE = True
    CALLBACK   = None    


    def error (message, *args, **kwargs):
        Logger.__log(Logger.TAG_ERROR, message, *args, **kwargs)


    def warn (message, *args, **kwargs):
        Logger.__log(Logger.TAG_WARN, message, *args, **kwargs)


    def info (message, *args, **kwargs):
        Logger.__log(Logger.TAG_INFO, message, *args, **kwargs)


    def debug (message, *args, **kwargs):
        Logger.__log(Logger.TAG_DEBUG, message, *args, **kwargs)


    def trace (message, *args, **kwargs):
        Logger.__log(Logger.TAG_TRACE, message, *args, **kwargs)


    def __log (level, message, *args, **kwargs):
        display = []
        display.append(Logger.__format_date())
        display.append(Logger.BRACES_TAG[0] + Logger.__align_tag(level) + Logger.BRACES_TAG[1])
        display.append(message)
        
        arguments = []

        for key, arg in enumerate(args):
            arguments.append(Logger.__arg(key, arg))

        for key, arg in kwargs.items():
            arguments.append(Logger.__arg(key, arg))

        message = Logger.__display(display, arguments)

        if Logger.TO_CONSOLE:
            print(message)

        if Logger.LOG_FILE != None:

            if isinstance(Logger.LOG_FILE, str):
                with open(Logger.LOG_FILE, 'a') as f:
                    f.write(message)
            else:
                Logger.LOG_FILE.write(message)

        if Logger.CALLBACK != None and callable(Logger.CALLBACK):
            Logger.CALLBACK(message)


    def __align_tag (tag):
        if not Logger.ALIGN_TAG: return tag

        maxlen = max(map(len, [Logger.TAG_ERROR, Logger.TAG_WARN, Logger.TAG_INFO, Logger.TAG_DEBUG, Logger.TAG_TRACE]))
        curlen = len(tag)
        diflen = maxlen - curlen

        return (' ' * math.ceil(diflen / 2)) + tag + (' ' * int(diflen / 2))

    def __format_date ():
        if not Logger.SHOW_DATE: return None

        return time.strftime(Logger.DATE_FORMAT)

    def __arg (key, arg):
        return Logger.ARGS_MODE.format(key,arg)

    
    def __display (display, arguments):
        message = []
        message.append(' '.join(display))
        if arguments:
            for arg in arguments:
                message.append(arg)
            message.append('-' * len(message[0]))

        return '\n'.join(message)

