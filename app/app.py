#!/usr/bin/env python3

from loguru import logger
import os
import random
from time import time
# import click
import time
from urllib.request import urlretrieve
import urllib.error

from tenacity import retry, stop_after_delay, stop_after_attempt
from tenacity import retry, retry_if_exception_type
 
class AppPrefrence(object):
    def __init__(self, data_path = "") -> None:
        if "" == data_path:
            data_path = "data"
        self.app_data_path = data_path
        self.mirrors_lists = []
        self.append_mirror_url( "https://source.unsplash.com/random/")
        pass

    def make_sure(self):
        if not os.path.isdir( self.app_data_path):
            os.makedirs( self.app_data_path)
            logger.trace( "[io] mkdir {}".format( self.app_data_path))
        pass
    
    def append_mirror_url( self, mirror_url):
        self.mirrors_lists.append( mirror_url)

    def get_mirror_url( self, index = -1, pixel = "")->str:
        if index < 0:
            index = random.randrange(0, len(self.mirrors_lists))
        if "" == pixel:
            pixel = "3840x2160"
        return str(self.mirrors_lists[index]) + "/" + pixel

    @staticmethod
    def get_global():
        return glapp_refrence

glapp_refrence = AppPrefrence()

@retry(retry=retry_if_exception_type(urllib.error.URLError),stop=stop_after_attempt(7))
def download(url, localpath):
    logger.trace( "[NET] download from {}".format( url))
    urlretrieve( url, localpath)
    logger.trace( "[IO] save to {}".format( localpath))
    pass

def down_once( index = -1):
    download( AppPrefrence.get_global().get_mirror_url(index), 
        os.path.join( AppPrefrence.get_global().app_data_path, 
            str(int(time.time()*1000)) + ".jpg"))
    pass

def init_logger( default_level = "TRACE"):
    logger.remove(handler_id=None)
    logger.add( "logs/splash.log",
        level= default_level)
    logger.info( "")
    pass



if __name__ == '__main__':
    init_logger()
    glapp_refrence.make_sure()
    down_once()
    pass








            




