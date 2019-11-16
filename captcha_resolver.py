#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2018, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://etuannv.com"

import requests
from time import sleep
import re
import logging
from captcha_solver import CaptchaSolver
# pip3 install captcha-solver


class CaptchaResolver():
    _api_key = ''
    def __init__(self, api_key):
        self._api_key = api_key
    
    def resolveNormalCaptcha(self, image_path, retry=5):
        if not self._api_key:
            logging.info("No 2captcha API key")
            return None
            
        while retry > 0:
            try:
                raw_data = open(image_path, 'rb').read()
                logging.info("Resolving captcha...")
                solver = CaptchaSolver('2captcha', api_key=self._api_key)
                captcha_code = solver.solve_captcha(raw_data)
                logging.info('Captcha code is:{}'.format(captcha_code))
                
                return captcha_code
            except print(0):
                pass
        return None
        
    
    def resolveRecaptcha(self, datakey, current_url, retry=5):
        if not self._api_key:
            logging.info("No 2captcha API key")
            return None

        while retry > 0:
            retry -=1
            try:
                site_key = datakey  # site-key, read the 2captcha docs on how to get this
                
                captcha_id = requests.post("https://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(self._api_key, site_key, current_url))
                
                captcha_id = captcha_id.text.split('|')[1]
                # then we parse gresponse from 2captcha response
                recaptcha_answer = requests.get("https://2captcha.com/res.php?key={}&action=get&id={}".format(self._api_key, captcha_id)).text
                logging.info("solving ref captcha...")
                
                while 'CAPCHA_NOT_READY' in recaptcha_answer:
                    sleep(5)
                    recaptcha_answer = requests.get("https://2captcha.com/res.php?key={}&action=get&id={}".format(self._api_key, captcha_id)).text
                # print(recaptcha_answer)
                recaptcha_answer = recaptcha_answer.split('|')[1]
                return recaptcha_answer
            except Exception as ex:
                logging.info("Error while resolve captcha. Retry ...")
                logging.info(ex)
                sleep(3)
        
        return None