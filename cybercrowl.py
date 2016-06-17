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


import httplib
import sys
import platform
import argparse

from libs.colorama import Fore, Back, Style
from libs import FileUtils
from urlparse import urlparse

__version__ = '1.0'
__description__ = '''\
  ___________________________________________

  CyberCrowl scan | v.''' + __version__ + '''
  Author: Chamli Mohamed
  Github: https://github.com/chamli
  ___________________________________________
'''


#fix url
def fix_url(url):
    parsed = urlparse(url, scheme='http')
    if url.startswith('www.'):
        return url
    if parsed.netloc:
        if not parsed.netloc.startswith('www.'):
            parsed = parsed._replace(netloc='www.' + parsed.netloc)
    elif not parsed.path.startswith('www.'):
        parsed = parsed._replace(path='www.' + parsed.path)
    return str(parsed.netloc)

#print banner
def header():
    MAYOR_VERSION = 1
    MINOR_VERSION = 0
    REVISION = 0
    VERSION = {
        "MAYOR_VERSION": MAYOR_VERSION,
        "MINOR_VERSION": MINOR_VERSION,
        "REVISION": REVISION
    }

    PROGRAM_BANNER = open(FileUtils.buildPath("banner.txt")).read().format(**VERSION)
    message = Style.BRIGHT + Fore.MAGENTA + PROGRAM_BANNER + Style.RESET_ALL
    write(message)
    
#check url work
def checkUrl(url):
    try:
        conn = httplib.HTTPConnection(url)
        conn.request("GET", "/")
        ress = conn.getresponse()
        code = ress.status
        if (code == 200):
            return True
        return False
    except:
        return False

#read url
def read(list,url):

    #fix url
    url = fix_url(url)

    #check url work
    if not checkUrl(url):
        message = "Check url please !! "
        message = "\n\n" + Fore.YELLOW + "[-]" + Style.RESET_ALL + Style.BRIGHT + Back.RED + message
        message += Style.RESET_ALL
        exit(write(message))
    
    #print Target
    message = Style.BRIGHT + Fore.YELLOW
    message += '\nTarget: {0}\n'.format(Fore.CYAN + url + Fore.YELLOW)
    message += Style.RESET_ALL
    write(message)

    #after check ,start scan
    crowl(list,url)
    
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

#crawl directory
def crowl(dirs, url):
    count = 0
    logfile = open(url+"_logs.txt", "w")

    for d in dirs:

        d = d.replace("\n", "")
        d = "/%s" % (d)

        res = ""
        save = 0

        conn = httplib.HTTPConnection(url)
        conn.request("GET", d)
        ress = conn.getresponse()
        response = ress.status

        #size
        try:
            size = int(ress.getheader('content-length'))
        except (KeyError, ValueError):
            size = len(ress.body)
        finally:
            f_size = FileUtils.sizeHuman(size)

        #check reponse
        if (response == 200 or response == 302 or response == 304):
          res = "[+] %s - %s : HTTP %s Found" % (url+d,f_size,response)
          res = Fore.GREEN + res + Style.RESET_ALL
          save = 1
          count +=1
        if (response == 401):
          res = "[-] %s - %s : HTTP %s : Unauthorized" % (url+d,f_size,response)
          res = message = Fore.YELLOW + res + Style.RESET_ALL
        if (response == 403):
          res = "[-] %s - %s : HTTP %s : Needs authorization" % (url+d,f_size,response)
          res = Fore.BLUE + res + Style.RESET_ALL
        if (response == 404):
          res = "[-] %s - %s : HTTP %s : Not Found" % (url+d,f_size,response)

        #print result
        if response != "":
          print res

        #save founded url log
        if save == 1:
            found = url+d
            logfile.writelines(found + "\n")
      
    print "\n\n[+]Found : %s directory" % (count)
    logfile.close()
      
    
def main():

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

    parser.add_argument('url', help='specific target url, like domain.com')

    parser.add_argument('-w', help='specific path to wordlist file',
                        nargs=1, dest='wordlist', required=False)

    args = parser.parse_args()

    # args strings
    domain = args.url
    wlist = args.wordlist
    if wlist: wlist = wlist[0]

    #print banner
    header()

    #check args
    if domain:
        if wlist:
            list = open(wlist,"r")
        else:
            list = open("list.txt", "r")
    else:
        exit('error arguments: use cybercrowl -h to help')
    # read
    read(list,domain)
    
    #close
    list.close()


if __name__ == '__main__':
  main()
