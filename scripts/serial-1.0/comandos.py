from subprocess import Popen, PIPE
from time import sleep

def _execute_cmd(cmd):
    ''' 
    Execute a command.
    The command is received by parameter as string.
    
    returns codestatus, stdout, stderr
    return int, str, str
    '''
    process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
    sts = process.wait()
    out = process.stdout.read().strip()
    err = process.stderr.read().strip()
    return sts, out, err

cmd1 = "./send_receive /dev/ttyUSB0 a"
cmd2 = "./send_receive /dev/ttyUSB0 50\n"
cmd3 = "./send_receive /dev/ttyUSB0 e"
cmd4 = "./send_receive /dev/ttyUSB0 200"
cmd5 = "./send_receive /dev/ttyUSB0 7"

timeout = 3
print "about to execute ... %s\n" % cmd1
sts,out,err = _execute_cmd(cmd1)
print out
sleep(timeout)
print "about to execute ... %s\n" % cmd2
sts,out,err = _execute_cmd(cmd2)
print out
sleep(timeout)
print "about to execute ... %s\n" % cmd3
sts,out,err = _execute_cmd(cmd3)
print out
sleep(timeout)
print "about to execute ... %s\n" % cmd4
sts,out,err = _execute_cmd(cmd4)
print out
sleep(timeout)
print "about to execute ... %s\n" % cmd5
sts,out,err = _execute_cmd(cmd5)
print out

