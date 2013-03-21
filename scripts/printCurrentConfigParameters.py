from optparse import OptionParser
from subprocess import Popen, PIPE

def _execute_cmd(cmd):
    '''
    Execute a command.
    The command is received by parameter as string.

    returns codestatus, stdout, stderr
    return int, str, str
    '''
    print cmd
    process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
    sts = process.wait()
    out = process.stdout.read().strip()
    err = process.stderr.read().strip()
    return sts, out, err
###################################################################
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-p','--prefix',dest = 'camera',type='str',help ='',default="main")
    (options,argv) = parser.parse_args()
    cmd = "darcmagic labels --print=1 --prefix=%s" % options.camera
    sts,out,err = _execute_cmd(cmd)
    params = eval(out)
    for param in params:
        print param
        if param == 'E' or param == 'gainE':
            pass
        else:
            cmd = "darcmagic get %s --prefix=%s" % (param, options.camera)
            sts,out,err = _execute_cmd(cmd)
            print out
            print
