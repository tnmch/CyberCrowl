==========================
CyberCrowl Scan v.1.0
==========================

CyberCrowl is a python Web path scanner tool.

![CyberCrowl](https://raw.githubusercontent.com/chamli/CyberCrowl/master/cybercrowl.png)

```
    [+] AUTOR:        Chamli Mohamed
    [+] EMAIL:        mohamed.chamli@esprit.tn
    [+] GITHUB:       https://github.com/chamli
    [+] TWITTER:      https://twitter.com/chamli_mohamed
    [+] FACEBOOK:     https://fb.com/TnMcH
```

Operating Systems supported
---------------------------
- Windows XP/7/8/10
- GNU/Linux
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
  cybercrowl www.domain.com
```
web site scan with external wordlist
  ```
  cybercrowl www.domain.com -w wordlist.txt
  ```

=======
Install
=======

(as root)

```
  git clone https://github.com/chamli/CyberCrowl.git
  cd CyberCrowl/
  pip install tldextract
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

Contribution
-------

- Your contributions and suggestions are heartily♥ welcome. (✿◕‿◕)
