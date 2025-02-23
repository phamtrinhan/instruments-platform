from datetime import datetime
from grapebot import telegram
def tracker(logger):
    def inner(func):
        def wrapper(*args, **kwargs):
            date = ""
            if "date" in kwargs and kwargs["date"] is not None:
                date = kwargs["date"].strftime("%Y-%m-%d")
            context_info = "{module}::{func}::{date}".format(module=func.__module__, func=func.__name__, date=date)
            start_time = datetime.now()
            try:
                logger.info("{info} starts.".format(info=context_info))
                returned_value = func(*args, **kwargs)
                latency = (datetime.now() - start_time).microseconds / 1000
                logger.info("{info} completed time={latency}ms.".format(
                    info=context_info, latency=latency))
                return returned_value
            except Exception as e:
                latency = (datetime.now() - start_time).microseconds / 1000
                
                logger.error(
                    "{info} failed time={latency}ms with error: {error}.".format(info=context_info, latency=latency,
                                                                                error=str(e)))

        return wrapper

    return inner


from datetime import datetime

def main_tracker(logger):
    def inner(func):
        def wrapper(*args, **kwargs):
            date = ""
            if "date" in kwargs and kwargs["date"] is not None:
                date = kwargs["date"].strftime("%Y-%m-%d")
            context_info = "{module}::{func}::{date}".format(module=func.__module__, func=func.__name__, date=date)
            start_time = datetime.now()
            try:
                # logger.info("{info} starts.".format(info=context_info))
                returned_value = func(*args, **kwargs)
                latency = (datetime.now() - start_time).microseconds / 1000
                # logger.info("{info} completed time={latency}ms.".format(
                #     info=context_info, latency=latency))
                return returned_value
            except Exception as e:
                latency = (datetime.now() - start_time).microseconds / 1000
                telegram.send_message("❗️⚠️ ERROR ⚠️ ❗️")
                telegram.send_message(str(e))
                telegram.send_message("⚠️ ⚠️ ⚠️  TASK FAILED ⚠️ ⚠️ ⚠️ ")
                logger.error(
                        "{info} failed time={latency}ms with error: {error}.".format(info=context_info, latency=latency,
                                                                                     error=str(e)))
        
        return wrapper
    
    return inner

