#!D:\Tools\Python36-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'winbrew==1.2.1','console_scripts','brew'
__requires__ = 'winbrew==1.2.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('winbrew==1.2.1', 'console_scripts', 'brew')()
    )
