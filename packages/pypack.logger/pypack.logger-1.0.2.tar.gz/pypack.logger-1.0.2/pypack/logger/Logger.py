import time, math, datetime, traceback, sys, os, inspect

class Logger:

    ALIGN_TAG = True
    SHOW_DATE = True

    TAG_ERROR = 'ERROR'
    TAG_WARN  = 'WARN'
    TAG_INFO  = 'INFO'
    TAG_DEBUG = 'DEBUG'
    TAG_TRACE = 'TRACE'

    TRACE_SEP = ('=','-','^')

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


    def trace (exception):
        if not isinstance(exception, Exception): raise TypeError('Trace must be an exception')
        

        print(Logger.TRACE_SEP[0] * len(str(exception)))
        print(str(exception))

                    
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # print(Logger.TRACE_SEP[1] * len(str(exception)))
        # print(exc_type,'at',fname,':',exc_tb.tb_lineno,'->',row)
        
        print(Logger.TRACE_SEP[1] * len(str(exception)))
        traceback.print_exc()
        
        print(Logger.TRACE_SEP[2] * len(str(exception)))

    def __trace(tb):
        # print(Logger.TRACE_SEP[1] * len(str(exception)))
        print(tb)
        print('source', inspect.getsourcefile(tb))
        print('line', inspect.getsourcelines(tb))
        
        # print('*'*80)
        # print(tb.exc_type,'at',tb.fname,':',tb.exc_tb.tb_lineno,'->','')

    def __log (level, message, *args, **kwargs):
        display = []
        display.append(Logger.__format_date())
        display.append(Logger.__align_tag(level))
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

        return ' ' * diflen + Logger.BRACES_TAG[0] + tag + Logger.BRACES_TAG[1]

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

