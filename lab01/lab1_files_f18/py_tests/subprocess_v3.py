#
# jfs9 9/10/17  example to illustrate python subprocess 
#

import subprocess

# Use a python subprocess to execute some 'echo' commands...
cmd = 'echo "Hello There!" > /home/jfs9/py_tests_v2/test_file'
print subprocess.check_output(cmd, shell=True)


