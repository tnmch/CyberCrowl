==========================
CyberCrowl Scan v.1.0
==========================

CyberCrowl is a python Web path scanner tool.

![CyberCrowl]()

Operating Systems supported
---------------------------
- Windows XP/7/8/10
- GNU/Linux
- MacOSX

License
-------
Copyright (C) Chamli Mohamed (mohamed.chamli@esprit.tn)

License: GNU General Public License, version 3


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
  python setup.py install
```

note: tested with python 2.7.6 
