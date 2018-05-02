import pexpect
import sys

'''
usage: python N6K_power_warning.py str1 str2
the real value of str1 and str2 should be: '0x78 : 0x3142', '0x81 : 0x2780',
using '0x78 : 0xf602' and '0x81 : 0xae00' in testing environment.
'''

if len(sys.argv) < 2:
    str1 = '0x78 : 0xf602'
    str2 = '0x81 : 0xae00'
else:
    str1 = sys.argv[1]
    str2 = sys.argv[2]

#save log file
child = pexpect.spawn('ssh root@10.75.40.3', maxread=16000)
fout = file('power_warning.log', 'w')

child.logfile = fout

child.expect('password:')
child.sendline('rootroot')
child.expect('#')

child.sendline('telnet 10.124.39.9')
child.expect('login:')
child.sendline('admin')
child.expect('Password:')
child.sendline('cisco!123')
child.expect('#')
child.sendline('ter leng 0')

child.expect('#')
child.sendline('show clock')
child.expect('#')
child.sendline('show klm internal i2c info device 17 1')
child.expect('#')
child.sendline('show klm internal i2c info device 17 2')
child.expect('#')
child.sendline('show klm internal i2c info device 17 3')

child.expect('#')
child.sendline('exit')
child.expect('$')
child.sendline('exit')

fout.close()

err1 = False
err2 = False

#check key message and output
fout = open('power_warning.log', 'r')
for line in fout.readlines():
    if line.find(str1) != -1:
        err1 = True
    if line.find(str2) != -1:
        err2 = True
    if line.find('UTC') <> -1:
        time1 = line

if err1 and err2:
    print 'find fan error' + ' at ' + time1.strip() + '.'

fout.close()

