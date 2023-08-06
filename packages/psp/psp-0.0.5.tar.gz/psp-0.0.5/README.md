# psp

python simple (color) printing - simple barebones wrappers for 256-color stdout.

## goals

* intended use is for stdout logging
* as few bells and whistles as possible
* as few characters as possible while still being intuitive (easy to learn, memorize)
* Avoid escapes where possible. Eg `print` --> `println`
* I know, typing `\n` isn't that hard, but this way you can do a `python -c` from
almost any scripting language and get the same results

## notes

* methods always return to "normal" text at the end. This is almost always what
 I want in the case of debugging. Too much formatting and it quickly loses its
 utility.

## usage

**pip3**:

```sh
pip3 install psp
python3 -c "import psp; psp.bluln('a blu line');"
```

**virtualenv**:

```sh
virtualenv testenv --python=$(which python3)
source testenv/bin/activate
pip3 install psp
python3 -c "import psp; psp.redln('a red line');"
deactivate
```

**Python**:

```py
#!/usr/bin/env python3
import sys
import psp

COLORS = [ 'nrm', 'wht', 'aqu', 'pur', 'blu', 'ylw', 'grn', 'red' ]
for c in COLORS:
    eval( 'psp.%sln("a %s line")' % (c, c) )

SENTENCE = 'Each word in this line has its own color'
for i, s in enumerate(SENTENCE.split(' ')):
    eval( 'psp.%s("%s ")' % ( COLORS[i % len(COLORS)], s) )

print('\n\n')
sys.exit(0)
```

## todo

* automatically set bold/italic/underline with single char modifiers
* test edge cases


#### end
