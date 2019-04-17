### Prerequisites

What things you need to install the software and how to install them

1) clone the git https://github.com/animtel/TutAPI.git
2) go to the folder
3) make this commands:
```
pip3 install -r requirements.txt
python startup.py
```

### Can be some troubles

When you will be installing packages, you can see some exception with pycrypto lib, for fix it, need to go throw the steps

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
