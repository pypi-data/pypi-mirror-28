# sig2cli
*Turn function signatures into Command Line Interfaces*

Just define a function signature as the entry point of your program instead of writing a lot of verbose argparse code.

## Example
```python
import sig2cli

def hi(name, times=1, enthusiast=False):
    """Say hi!
    Arguments
        name:       person to greet
        times:      how many times to greet
        enthusiast: add an exclamation mark
    """
    for _ in range(times):
        print('Hi {}{}'.format(name, '!' if enthusiast else ''))

if __name__ == "__main__":
    sig2cli.run(hi)
```
The command line interface is automatically created from the signature and the docstring.
```
$ python my_script.py -h
usage: sig2cli.py [-h] -n NAME [-t TIMES] [-e]

Say hi!

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  person to greet
  -t TIMES, --times TIMES
                        how many times to greet (default: 1)
  -e, --enthusiast      add an exclamation mark at the end (default: False)

$ python my_script.py --name John -t 2 -e
Hi John!
Hi John!
```

## Installation

Install it with pip:
```
pip install sig2cli
```

# Description

The command line description is taken from the docstring of the method, with the following conventions:
* the description is everything that precedes the string "Arg" (so Arguments, Args) that starts the argument list.
* each argument should be in the format <argname> : [argtype] <argumentdescription>

Types are inferred from default arguments, or taken from the docstring if specified.
Allowed types are "str", "int", "float", "bool".
It supports short args (the first letter of each argument) only if they are all different and no argument starts with "h" (reserved for help)
Default bool arguments are registered as flags.

