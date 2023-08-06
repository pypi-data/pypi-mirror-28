
# ed25519-python

python binding for [Warchant/ed25519](https://github.com/Warchant/ed25519)

# Need to build

- cmake
- gcc
- g++


# How to install

```
git clone https://github.com/MizukiSonoko/ed25519-python.git
cd ed25519-python
git submodule update --init --recursive
python setup.py develop
```

# Sample
   
```python
from ed25519_python import ed25519
pub, pri = ed25519.generate()
message = b"c0a5cca43b8aa79eb50e3464bc839dd6fd414fae0ddf928ca23dcebf8a8b8dd0"
ed25519.sign(message, pub, pri)
```

