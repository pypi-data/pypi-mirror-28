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
                le_token = param.get('le_token',None)
                logger = logging.getLogger(name)
                logger.setLevel(level)
                # Log Init
                handler = logging.StreamHandler()
                if (graylog.get("host",None) != None and graylog.get("port",None) != None and graylog.get("host",None) != "" and graylog.get("port",None) != ""):
                    handler = graypy.GELFHandler(graylog["host"], graylog["port"])
                elif le_token != None:
                    handler = R7InsightHandler(le_token, "us")

                logger.addHandler(handler)
                res = function(param)
                log = {"function":name,"result":res}
                return res
            except requests.exceptions.HTTPError as err:
                error = {"error": {"description": str(err), "response": err.response.json()}}
            except Exception as err:
                error = {"error": {"description": str(err)}}
            finally:
                log = {"function":name, "elapsed_time": str(round(time.time() - start_time,2))}
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
