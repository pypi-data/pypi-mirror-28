import logging
import graypy
import requests
import time
import sys
import traceback
from r7insight import R7InsightHandler

def log(name='', level=logging.INFO, keys=[]):
    def decorator(function):
        def wrapper(param):
            log = dict()
            error = dict()
            start_time = time.time()
            try:
                # Init logger
                graylog = {'host': param.get('loghub',None),'port': param.get('logport',None)}
                r7insight_token = param.get('r7insight_token',None)
                logger = logging.getLogger(name)
                logger.setLevel(level)
                # Log Init
                handler = logging.StreamHandler()
                if (graylog.get("host",None) != None and graylog.get("port",None) != None):
                    handler = graypy.GELFHandler(graylog["host"], graylog["port"])
                elif r7insight_token != None:
                    handler = R7InsightHandler(r7insight_token, "us")

                logger.addHandler(handler)
                res = function(param)
                log = {"function":function.__name__,"result":res}
                return res
            except requests.exceptions.HTTPError as err:
                error = {"error": {"description": str(err), "response": err.response.json()}}
            except Exception as err:
                error = {"error": {"description": str(err)}}
            finally:
                log = {"function":function.__name__, "elapsed_time": str(round(time.time() - start_time,2))}
                extra = {}
                for key in keys:
                    if param.get(key,None) != None:
                        extra[key] = param[key]

                if not error:
                    logger.info(log,extra=extra)
                else:
                    stack = traceback.format_stack()
                    error['stack_trace'] = stack
                    error['args'] = param
                    log.update(error)
                    logger.error(log,extra=extra)
                    return error
        return wrapper
    return decorator
