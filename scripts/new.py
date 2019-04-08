# -*- coding: utf-8 -*-
#!/usr/bin/env python


import sys, os
import time
import datetime

#reload(sys)
#sys.setdefaultencoding('utf-8')

if len(sys.argv) != 2:
    sys.stderr.write(u"Error: 参数异常!")
    exit(1)


name = sys.argv[1]

if os.path.exists('markdown/%s.md' % name):
    sys.stderr.write(u"文件已经存在!\n")
    sys.stderr.write(u"将要打开!\n")

    time.sleep(1)
    os.system('vim markdown/%s.md' % name)
    
    exit(1)
    


with open('markdown/%s.md' % name, 'w') as f:
    f.write('title: \n')
    f.write('date: %s\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    f.write('---\n\n')



os.system('vim markdown/%s.md' % name)
    



