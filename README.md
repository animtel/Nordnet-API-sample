### Prerequisites

First of all you need to download and install python 3.5 or older version

https://www.python.org/downloads/

And update your pip
```
python -m pip install --upgrade pip
```

After - reboot your computer and go to the next steps

What things you need to install the software and how to install them

1) clone the git https://github.com/animtel/TutAPI.git
2) set up your's creds to the settings.json
3) go to the folder
4) make this commands:
```
pip install -r requirements.txt
python startup.py
```

### Can be some troubles

When you will be installing packages, you can see some exception with pycrypto lib, for fix it, need to go by steps

1) Go to the path, sometimes path in different machines is different, but it will be same with it
`C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build`

2) Run this
```
vcvarsamd64_x86.bat
vcvarsx86_amd64.bat
set CL=-FI"%VCToolsInstallDir%\include\stdint.h"
```
3) install pycrypto again
```
pip install pycrypto
```

All info about solution this bug, i give from this issue https://github.com/dlitz/pycrypto/issues/218#issuecomment-437498355

OR

The Crypto package has known troubles when running on python 3.5 when it comes to finding the right internal modules.
If the pycrypto is installed using pip the package Crypto can on some occasions yield an error like "missing package" or
similar.
```
ImportError: No module named Crypto.Cipher'
```
In order to solve this problem simply re-install the package with easy_install
```
pip uninstall pycrypto
easy_install pycrypto
```

## Also about bugs

You can see some bug with ModuleNotFoundError: No module named 'winrandom'

1) For solve it, need to go to
```
C:\Program Files (x86)\Python37-32\Lib\site-packages\Crypto\Random\OSRNG
```
Or same path and change
```
import winrandom
```
to
```
from . import winrandom
```

## Links with information about NordetAPI

https://api.test.nordnet.se/next/2/api-docs/docs/feeds - info about socket subscriptions with api

https://api.test.nordnet.se/api-docs/index.html - info about endpoints of API

https://api.test.nordnet.se/ - nordnet wiki

# Keywords
* Python 3.7
* Nordnet
* Nordnet-API
* Crypto.Cipher import PKCS1_v1_5
* Crypto.PublicKey
