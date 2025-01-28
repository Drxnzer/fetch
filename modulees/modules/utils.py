import os
import sys
import json
import base64
import random
import hashlib
import binascii

import requests
import psutil
import ctypes
import hmac
import fade

from colorama import Fore, Style


from modules.ui import Logger, Colors

def split_data(data: str, delimiter: str) -> list:

    try:
        return data.split(delimiter)
    
    except Exception:
        return None


def sort_email(email: str) -> list:

    for delimiter in [":", "|"]:

        if delimiter in email:
            return split_data(email, delimiter)

    return None


def get_formatted_proxy(proxy: str) -> dict:

    try:
        if '@' in proxy or len(proxy.split(':')) == 2:
            formatted_proxy = proxy

        else:
            parts = proxy.split(':')

            if '.' in parts[0]:
                formatted_proxy = ':'.join(parts[2:]) + '@' + ':'.join(parts[:2])

            else:
                formatted_proxy = ':'.join(parts[:2]) + '@' + ':'.join(parts[2:])
        
        return {
            'http': f'http://{formatted_proxy}',
            'https': f'http://{formatted_proxy}'
        }
    
    except:
        return None



def setup_name() -> str:

    return ' '.join([''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 10))) for _ in range(2)])




