import os

def check_sshpass_installed():
    return True if os.system("which sshpass > /dev/null")==0 else False


def get_real_bin():
    this_dir, this_filename = os.path.split(__file__)
    bin_path = os.path.join(this_dir, "bin", "gotossh")
    return bin_path

def init():
    os.system("cp %s /usr/local/bin"%(get_real_bin()))
    os.system("chmod a+x /usr/local/bin/gotossh")
    os.system('/bin/bash; eval "$(register-python-argcomplete /usr/local/bin/gotossh)"')
    if not check_sshpass_installed():
        print "you'd better installl sshpass"

def edit():
    os.system("vim ~/.goto.cfg")
