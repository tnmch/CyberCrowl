
# CyberCrowl Scan v.1.5


CyberCrowl is a python Web path scanner tool.
[![asciicast](https://asciinema.org/a/vd2s3AMNt0FMqD9ZO1C7uDAWb.png)](https://asciinema.org/a/vd2s3AMNt0FMqD9ZO1C7uDAWb)

```
    [+] AUTOR:        TnMch
    [+] GITHUB:       https://github.com/tnmch
    [+] TWITTER:      https://twitter.com/tnmch_
```

Operating Systems supported
---------------------------
- Windows XP/7/8/10
- GNU/Linux (This tools now is part of blackarch : https://www.blackarch.org/webapp.html)
- MacOSX


License
-------
GNU General Public License, version 3


Usage
-----

```
  CyberCrowl [-h] [-v] [-w WORDLIST] url
```

positional arguments:

```
  url            specific target url, like domain.com
```
optional arguments:

```
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -w WORDLIST    specific path to wordlist file
  -d DELAY       add delay between requests
```

Example
-------

web site scan with internal wordlist
```
  cybercrowl -u www.domain.com
```
web site scan with external wordlist
  ```
  cybercrowl -u www.domain.com -w wordlist.txt
  ```


# Install


(as root)

```
  git clone https://github.com/tnmch/CyberCrowl.git
  cd CyberCrowl/
  pip install -r requirements.txt
  python cybercrowl.py -h
```

note: tested with python 2.7.6 

Version
-------
@ Version v1.1 : 
- fixed bugs
- add work with subdomain

@ Version v1.2 :
- Added delay option for avoiding blacklisting

@ Version v1.4 :
- Fix url redirect issue & add some features  

@ Version v1.5 :
- Support User agent randomization
- HTTP proxy support (Ex : burpsuite proxy)
- Support different HTTP protocol authentication (Basic | Digest | NTLM) 
- Auto update option

Contribution
-------

- Your contributions and suggestions are heartily♥ welcome. (✿◕‿◕)
