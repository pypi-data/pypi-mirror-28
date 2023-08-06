This is a simple property like decorator. It's name is what it does. The decorated
getter is called only once and the value returned at first call is then returned
in all the subsequent calls.

### Usage

```
from random import randint
from readonlyonce_property import readonlyonce_property

class OneShotRandom(object):
    @readonlyonce_property
    def val(self)
        return randint(0, 100)

myrand = OneShotRandom()

# You should get the same value 

print(myrand.val)
print(myrand.val)
print(myrand.val)
print(myrand.val)
```
