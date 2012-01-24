#!/usr/bin/python
# backs up xfile.xxx to backup/xfile_iii.xxx
import sys, os, shutil

backupdir = 'backup/'
msg = ''

try:
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = raw_input('Please enter filename: ')

    name, ext = os.path.splitext(os.path.basename(filename))
    i = 0
    while True:
        target = ''.join([os.path.join(backupdir, name),'_%03d%s'%(i, ext)])
        if os.path.exists(target):
            i += 1
        else:
            shutil.copy2(filename, target)
            msg = ' '.join(('copied',filename,'to',target))
            break
        
except:
    raw_input('some error occured. action aborted.')
else:
    print msg
