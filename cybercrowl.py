#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
# ----------------------------------------------------------------------
# @author Chamli Mohamed 14|06|2016

import os
import sys
import platform
import argparse
import requests
import time
from fake_useragent import UserAgent
from requests_ntlm import HttpNtlmAuth
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from libs.colorama import Fore, Back, Style
from libs import FileUtils
from libs.tldextract import *

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if platform.system() == 'Windows':
    from libs.colorama.win32 import *

__version__ = '1.5'
__description__ = '''\
  ___________________________________________

  CyberCrowl scan | v.''' + __version__ + '''
  Author: Chamli Mohamed
  Github: https://github.com/chamli
  ___________________________________________
'''


# print banner
def header():
    MAYOR_VERSION = 1
    MINOR_VERSION = 5
    REVISION = 0
    VERSION = {
        "MAYOR_VERSION": MAYOR_VERSION,
        "MINOR_VERSION": MINOR_VERSION,
        "REVISION": REVISION
    }

    PROGRAM_BANNER = open(FileUtils.buildPath("banner.txt")).read().format(**VERSION)
    message = Style.BRIGHT + Fore.MAGENTA + PROGRAM_BANNER + Style.RESET_ALL
    write(message)

#ask_change_url
def yes_no(answer):
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    while True:
        choice = answer.lower()
        if choice in yes:
            return True
        elif choice in no:
            return False

def write(string):
    if platform.system() == 'Windows':
        sys.stdout.write(string)
        sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()
    else:
        sys.stdout.write(string + '\n')
    sys.stdout.flush()
    sys.stdout.flush()

# check url work
def checkUrl(url):

    # check
    try:
        ress1 = requests.head(url , allow_redirects=True)

        if url != ress1.url:
            return "Maybe you should use ;"+ress1.url
        else:
            ress = requests.get(url)
            code = ress.status_code
            if (code == 200):
                return True
            else:
               return False
    except requests.exceptions.ConnectionError:
        return "Try a different url please"
    except requests.exceptions.MissingSchema:
        return "Try a different url please"
    except:
        return False

# read url
def read(url):

    ret = checkUrl(url)
    url_ok = False
    if "Maybe" in str(ret):
        w = "Would you like to change url to "+ ret.rsplit(';', 1)[1] + " (y/n) : "
        choice = raw_input(w)
        res = yes_no(choice)
        if res:
            url_ok = True
            url = ret.rsplit(';', 1)[1]
    if ret != True and url_ok != True:
        message = "Check url (ex: https://github.com) " + (ret if "Try" in str(ret) else "" )
        message = "\n\n" + Fore.YELLOW + "[-]" + Style.RESET_ALL + Style.BRIGHT + Back.RED + message
        message += Style.RESET_ALL
        exit(write(message))

    # print Target
    message = Style.BRIGHT + Fore.YELLOW
    message += '\nTarget: {0}\n'.format(Fore.CYAN + url + Fore.YELLOW)
    message += Style.RESET_ALL
    write(message)
    
    return url


# crawl directory
def crowl(dirs, url, args):

    # args strings
    domain = args.url
    wlist = args.wordlist
    delay = args.delay
    random_agent = args.randomAgent
    auth_type = args.authType.lower() if args.authType is not None else ""
    auth_cred = "".join(args.authCred).rsplit(':') if args.authCred is not None else ""
    proxy = "".join(args.proxy)

    # init count valid url
    count = 0

    # get domain
    extracted = tldextract.extract(url)
    domain = "{}.{}".format(extracted.domain, extracted.suffix)

    if not os.path.exists("reports"):
        os.makedirs("reports")
    logfile = open("reports/" + domain + "_logs.txt", "w+")

    # init user agent
    if random_agent == True:
        ua = UserAgent()
     
    # init default user agent    
    headers = { 'User-Agent':  'CyberCrowl' }
    
    # init default proxy 
    proxies = {"http": proxy,"https": proxy}
    
    for dir in dirs:

        dir = dir.replace("\n", "")
        dir = "%s" % (dir)

        res = ""
        save = 0
        f_url  = url + "/" + dir
        
        # add cookie header
        
        if random_agent == True:
            headers = { 'User-Agent':  ua.random }
                        
        
        # make request with different type of authentication
        if auth_type == "basic":
            try:
                ress = requests.get(f_url, headers=headers ,auth=HTTPBasicAuth(auth_cred[0], auth_cred[1]),allow_redirects=False, proxies=proxies, verify=False)
            except requests.exceptions.ProxyError:
                exit(write("Check your proxy please! "))
                
        elif auth_type == "digest":
            try:
                ress = requests.get(f_url, headers=headers ,auth=HTTPDigestAuth(auth_cred[0], auth_cred[1]),allow_redirects=False, proxies=proxies, verify=False)
            except requests.exceptions.ProxyError:
                exit(write("Check your proxy please! "))
                
        elif auth_type == "ntlm":
            try:
                ress = requests.get(f_url, headers=headers ,auth=HttpNtlmAuth(auth_cred[0], auth_cred[1]),allow_redirects=False, proxies=proxies, verify=False)
            except requests.exceptions.ProxyError:
                exit(write("Check your proxy please! "))

        else:
            try:
                ress = requests.get(f_url, headers=headers ,allow_redirects=False, proxies=proxies, verify=False)
            except requests.exceptions.ProxyError:
                exit(write("Check your proxy please! "))
                
        response = ress.status_code

        # size
        try:
            if (ress.headers['content-length'] is not None):
                size = int(ress.headers['content-length'])
            else:
                size = 0 
                
        except (KeyError, ValueError, TypeError):
            size = len(ress.content)
        finally:
            f_size = FileUtils.sizeHuman(size)

        # check reponse
        if (response == 200 or response == 302 or response == 304):
            res = "[+] %s - %s : HTTP %s Found" % (f_url, f_size, response)
            res = Fore.GREEN + res + Style.RESET_ALL
            save = 1
            count += 1
        elif (response == 401):
            res = "[-] %s - %s : HTTP %s : Unauthorized" % (f_url, f_size, response)
            res = message = Fore.YELLOW + res + Style.RESET_ALL
        elif (response == 403):
            res = "[-] %s - %s : HTTP %s : Needs authorization" % (f_url, f_size, response)
            res = Fore.BLUE + res + Style.RESET_ALL
        elif (response == 404):
            res = "[-] %s - %s : HTTP %s : Not Found" % (f_url, f_size, response)
        elif (response == 405):
            res = "[-] %s - %s : HTTP %s : Method Not Allowed" % (f_url, f_size, response)
        elif (response == 406):
            res = "[-] %s - %s : HTTP %s : Not Acceptable" % (f_url, f_size, response)
        else :
            res = "[-] %s - %s : HTTP %s : Unknown response" % (f_url, f_size, response)


        # print result
        if response != "":
            write(res)

        # save founded url log
        if save == 1:
            found = url + dir
            logfile.writelines(found + "\n")

        if delay > 0:
            time.sleep(float(delay))
            print "Sleeping for %s seconds" % str(delay)

    write("\n\n[+]Found : %s directory" % (count))
    logfile.close()


def main():

    try:
        global list
        parser = argparse.ArgumentParser(
            version=__version__,
            formatter_class=argparse.RawTextHelpFormatter,
            prog='CyberCrowl',
            description=__description__,
            epilog='''\
        EXAMPLE:
        web site scan with internal wordlist
          cybercrowl www.domain.com
        web site scan with external wordlist
          cybercrowl www.domain.com -w wordlist.txt
                    ''')

        parser.add_argument('url', help='specific target url, like domain.com', type=str)

        parser.add_argument('-w', help='specific path to wordlist file',
                            nargs=1, dest='wordlist', type=str, required=False)

        parser.add_argument('-d', help='add delay between requests',
                            nargs=1, dest='delay', type=float, default=0)
                            
        parser.add_argument('--random-agent', dest="randomAgent", 
                             help='Use randomly selected HTTP User-Agent header value',
                             action='store_true')
        
        parser.add_argument("--auth-type", dest="authType", 
                            nargs='?', type=str, help="HTTP authentication type ""(Basic, Digest or NTLM)", required=False)
                            
        parser.add_argument("--auth-cred", dest="authCred",
                            nargs=1, type=str, help="HTTP authentication credentials ""(name:password)", required=False)
                            
        parser.add_argument("--proxy", dest="proxy",
                            nargs=1, type=str, help="Use a proxy to connect to the target URL", required=False)


        args = parser.parse_args()
        
        required_together = ('authType','authCred')

        # args.authType will be None if authType is not provided
        if any([getattr(args,x) for x in required_together]):
            if not all([getattr(args,x) for x in required_together]):
                exit(write("Cannot supply --auth-type without --auth-cred"))
                

        # args strings
        domain = args.url
        wlist = args.wordlist
        
        if wlist:
            wlist = wlist[0]

        # print banner
        header()

        # check args
        if domain:
            if wlist:
                list = open(wlist, "r")
            else:
                list = open("list.txt", "r")
        else:
            exit(write('error arguments: use cybercrowl -h to help'))

        # read
        url = read(domain)
        
        # After check ,start scan
        crowl(list, url, args)
    
        # close
        list.close()

    except KeyboardInterrupt:

        print '[!] Ctrl + C detected\n[!] Exiting'
        sys.exit(0)

    except EOFError:

        print '[!] Ctrl + D detected\n[!] Exiting'
        sys.exit(0)


if __name__ == '__main__':
    main()
