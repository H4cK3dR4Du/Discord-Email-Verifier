import os, sys, json, time, random, string, ctypes, logging
import threading
import concurrent.futures
import json

try:
    import httpx
    import requests
    import colorama
    import pystyle
    import datetime
    import hotmailbox
except ModuleNotFoundError:
    os.system("pip install httpx")
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install hotmailbox.py")

from colorama import Fore, Style
from tls_client import Session
from random import choice
from json import dumps
from pystyle import System, Colors, Colorate, Write
from concurrent import futures
from threading import Lock
from data.solver import Solver

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

solved = 0
failed = 0
errors = 0
verified = 0
total = 0
output_lock = threading.Lock()
print_lock = threading.Lock()
proxy_lock = Lock()
proxies = []
bad_proxies = []
good_proxies = []
lock_proxies = []
config = json.loads(open('config.json', 'r').read())

def proxx():
    if config["proxy_scraper"] == "y":
        with open(f"proxies.txt", "w", encoding='utf-8') as f:
            f.write("")
        def save_proxies(proxies):
            with open("proxies.txt", "w") as file:
                file.write("\n".join(proxies))

        def get_proxies():
            with open('proxies.txt', 'r', encoding='utf-8') as f:
                proxies = f.read().splitlines()
            if not proxies:
                proxy_log = {}
            else:
                proxy = random.choice(proxies)
                proxy_log = {
                    "http://": f"http://{proxy}", "https://": f"http://{proxy}"
                }
            try:
                url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
                response = httpx.get(url, proxies=proxy_log, timeout=60)

                if response.status_code == 200:
                    proxies = response.text.splitlines()
                    save_proxies(proxies)
                else:
                    time.sleep(1)
                    get_proxies()
            except httpx.ProxyError:
                get_proxies()
            except httpx.ReadError:
                get_proxies()
            except httpx.ConnectTimeout:
                get_proxies()
            except httpx.ReadTimeout:
                get_proxies()
            except httpx.ConnectError:
                get_proxies()
            except httpx.ProtocolError:
                get_proxies()

        def check_proxies_file():
            file_path = "proxies.txt"
            if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                get_proxies()

        check_proxies_file()
    else:
        pass

proxx()

def get_time_rn():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

start_time = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'[ RaduEV Tool ] ~ Discord : https://discord.gg/Un63v2truD | github.com/H4cK3dR4Du')

def update_title():
    global solved, errors, verified, total
    current_time = time.time()
    elapsed_time = current_time - start_time
    v_per_minute = verified / (elapsed_time / 60)
    v_per_hour = verified / (elapsed_time / 3600)
    v_per_day = verified / (elapsed_time / 86400)
    elapsed_days = int(elapsed_time // 86400)
    elapsed_hours = int((elapsed_time % 86400) // 3600)
    elapsed_minutes = int((elapsed_time % 3600) // 60)
    elapsed_seconds = int(elapsed_time % 60)
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ RaduEV Tool ] ~ Email Verified : {verified} ~ Errors : {errors} @ Speed : {int(v_per_minute)}/min | Elapsed : {elapsed_days}d {elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s | Success Rate : {round(verified/total*100,2)}% | discord.gg/Un63v2truD')

def email_verifier(token):
    global solved, errors, verified, total
    session = Session(
        client_identifier='chrome_112'
    )

    proxy = choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    if ":" in proxy and len(proxy.split(":")) == 4:
        ip, port, user, pw = proxy.split(":")
        proxy_string = f"http://{user}:{pw}@{ip}:{port}"
    else:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es",
        "Authorization": token,
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://discord.com/channels/@me",
        "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVzIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMTYuMC4xOTM4LjU0IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIyMjM1MiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

    key = config["hotmailbox-key"]
    user = hotmailbox.User(key)
    emails = user.purchase("HOTMAIL", 1)
    time_rn = get_time_rn()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({orange}${gray}) {pretty}Purchased {gray}| {yellow}{emails[0].email}:{emails[0].password}")
    
    payload = {
        "email": emails[0].email,
        "password": emails[0].password
    }
    
    r = session.patch(f'https://discord.com/api/v9/users/@me', headers=headers, json=payload)
    time_rn = get_time_rn()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({cyan}*{gray}) {pretty}Success {gray}| {green}Sent Email Verification Code")
    time.sleep(5)
    email = hotmailbox.Email(emails[0].email, emails[0].password)
    link = email.discord()
    random_number = random.randint(1, 100)
    file_name = f"data/email_codes({random_number}).txt"     
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
                file.write(link)
    time.sleep(0.5)
    with open(file_name, 'r') as f:
        a = f.readlines()
        if a:
            time.sleep(1)
            new_link = a[0].strip()
            response = requests.get(new_link)
            time.sleep(0.5)
            redirected_url = response.url
            time.sleep(0.5)
            formatted_link = redirected_url.strip()
            token_email = formatted_link.split('token=')[1]
            time_rn = get_time_rn()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}#{gray}) {pretty}Verifying Email {gray}| {yellow}{token_email[:70]}******")
            
            headers.update({
                "Referer": "https://discord.com/verify"
            })

            payload = {
                "token": token_email
            }

            response_email = session.post('https://discord.com/api/v9/auth/verify', headers=headers, json=payload)
            if response_email.status_code == 200 or response.status_code == 201 or response.status_code == 204:
                r8 = session.post("https://discord.com/api/v9/auth/login", json={"email": emails[0].email, "password": emails[0].password}, proxy=f"http://{proxy}")
                token = r8.json()['token']
                verified += 1
                total += 1
                update_title()
                time_rn = get_time_rn()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Email Verified {gray}| ", end='')
                sys.stdout.flush()
                Write.Print(token[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
                name = "Results"
                if not os.path.exists(name):
                    os.mkdir(name)
                    with open(f"Results/ev_tokens.txt", "a", encoding="utf-8") as f:
                        f.write(f"{token} | Email : {emails[0].email} | Password : {emails[0].password}\n")
                    with open(f"Results/tokens.txt", "a", encoding="utf-8") as f2:
                        f2.write(token + "\n")
                else:
                    with open(f"Results/ev_tokens.txt", "a", encoding="utf-8") as f:
                        f.write(f"{token} | Email : {emails[0].email} | Password : {emails[0].password}\n")
                    with open(f"Results/tokens.txt", "a", encoding="utf-8") as f2:
                        f2.write(token + "\n")
            else:
                solver = Solver(
                    proxy="",
                    siteKey="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
                    siteUrl="discord.com"
                )
                captchaKey = solver.solveCaptcha2()
                payload.update({
                    "captcha_key": captchaKey
                })

                response_email2 = session.post('https://discord.com/api/v9/auth/verify', headers=headers, json=payload)
                if response_email2.status_code == 200 or response_email2.status_code == 201 or response_email2.status_code == 204:
                    r8 = session.post("https://discord.com/api/v9/auth/login", json={"email": emails[0].email, "password": emails[0].password}, proxy=f"http://{proxy}")
                    token = r8.json()['token']
                    verified += 1
                    total += 1
                    update_title()
                    time_rn = get_time_rn()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Email Verified {gray}| ", end='')
                    sys.stdout.flush()
                    Write.Print(token[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
                    name = "Results"
                    if not os.path.exists(name):
                        os.mkdir(name)
                        with open(f"Results/ev_tokens.txt", "a", encoding="utf-8") as f:
                            f.write(f"{token} | Email : {emails[0].email} | Password : {emails[0].password}\n")
                        with open(f"Results/tokens.txt", "a", encoding="utf-8") as f2:
                            f2.write(token + "\n")
                    else:
                        with open(f"Results/ev_tokens.txt", "a", encoding="utf-8") as f:
                            f.write(f"{token} | Email : {emails[0].email} | Password : {emails[0].password}\n")
                        with open(f"Results/tokens.txt", "a", encoding="utf-8") as f2:
                            f2.write(token + "\n")
                else:
                    errors += 1
                    total += 1
                    update_title()
    os.remove(file_name)

def process_token(token):
    try:
        result = email_verifier(token)
    except Exception as e:
        process_token(token)

with open('tokens.txt', 'r') as f:
    tokens = f.read().splitlines()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_token, tokens)