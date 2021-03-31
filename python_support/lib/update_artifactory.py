""" Update artifactory
"""
import os
import datetime as dt
from glob import glob

now = dt.datetime.now()
ago = now-dt.timedelta(days=25)

bigdata = os.environ['TEST_BIGDATA']
files_to_update = []

for root, dirs, files in os.walk(bigdata):
    for fname in files:
        path = os.path.abspath(os.path.join(root, fname))
        st = os.stat(path)    
        mod_time = dt.datetime.fromtimestamp(st.st_mtime)
        if mod_time > ago:
            print(mod_time, path)
            files_to_update.append(path)
print('')
jfrog_cmd = ['jfrog rt u ' + \
              line + ' ' + \
              line.replace(bigdata, '') for line in files_to_update]
for line in jfrog_cmd:
    print(line)
