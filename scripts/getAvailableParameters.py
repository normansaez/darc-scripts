from subprocess import Popen, PIPE
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

for host in ["gns","gas"]:
    cmd = "ssh %s sudo rm -fr $ACSDATA/tmp/*" % host
    sts, out, err = _execute_cmd(cmd)
    
    print "sts ---------------------------------------------------------------"
    print sts
    print "err ---------------------------------------------------------------"
    print err
    print "out ---------------------------------------------------------------"
    print out
    print "-------------------------------------------------------------------"

