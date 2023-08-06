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

```sh
virtualenv testenv --python=$(which python3)
source testenv/bin/activate

pip3 install psp
python3 -c "import psp; psp.redln('a red line');"
```

## With virtualenv

```sh
virtualenv localenv --python=$(which python3)
##--unzip-setuptools --always-copy --never-download --no-setuptools
source localenv/bin/activate

cd psp
pip3 install . --upgrade
#pip3 install --no-binary --no-compile .
#--editable --ignore-installed
```

#### end
