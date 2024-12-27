import os
from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            log_message = (
                f"[{datetime.now()}] Function '{old_function.__name__}' was called with "
                f"args: {args}, kwargs: {kwargs}. Returned: {result}\n"
            )
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
            return result

        return new_function

    return __logger
