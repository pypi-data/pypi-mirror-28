A argument parsing module that also can run commands.

Note the argc.get key is the string but only if the argument started with an "-"
if it started with "--" then you can use it by added and "-" in front of the string
```py
argc().get("s") # - short
argc().get("-long") # -- long
```

## Changelog
2.0.2 - Bugfixes

2.0.1 - Fixed detectType for python2

2.0.0 - Added tests working way better now

1.1.3 - stupid dots

1.1.2 - removed / in as an arguement

1.1.1 - Some more bugfixes!

1.1.0 - Thought so. and python2 support

1.0.2 - Confusion

1.0.1 - Bugfix

1.0.0 - Release


### Example 1
```py
from argc import argc

if __name__ import "__main__":
    # for python 2 do as it does not support charectar conversion
    # args = argc(sys.argv, False)
    args = argc() # uses sys.argv by default
    args.add("version", 10.0, True) # the true means that it will exit when the command is done
    args.add("func", lambda: 100**10, True) # real time calculations and running of functions
    args.add("func_2", functionname) # or just a function
    args.add("help", [
        "It also supports lists for multi-line prints",
        "With support for {}".format("functions"),
        lambda: 10-9**10,
        "So yeah... Awsome"
    ], True)

    args.run() # checks and runs arguments (can stop program)

    args.get("-config_name", True) # get config if by default it will return Value but
    # add True it will return True/False
```

### Example 2
```py
# example program that takes some arguments
# run as ${python} test.py ${args}

import random
from argc import argc

__version__ = "1.0.0"
__author__ = "Monty python"
__package__ = "STRING RING"
 __help__ = [
    "Usage: ",
    "   import STRING_RING as sr",
    "   tone = 10",
    "   sr.RING(tone)",
    "Author: {}".format(__author__),
    "Name: %(__package__)s"
]


# arguments are case sensetive but the -- and - is stripped
# so you only need the names. but that also means that -hallo,  --hallo and /hallo 
# all triggers the hello command
# option

if __name__ == "__main__":
    args = argc() # uses sys.argv by default
    args.add("help", __help__, True) # exits on help
    args.add("version", __version__,  True)
    # supports functions (prints return value)
    args.add("func", lambda: random.randint(0, 10**10), True)
    # checks and runs commands
    args.run() 

    # code after .run
    
    # Use .get for config
    if args.get("useL"):
        print("Using L")
    else:
        print("am not using L")

    # and for custom config using long
    print(args.get("-config", False)) # Use raw data returns None if it does not exist 
```