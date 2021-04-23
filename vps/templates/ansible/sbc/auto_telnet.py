# auto_telnet.py - remote control via telnet
# comando de testing:
# python2 auto_telnet.py -h 192.168.0.20 -c 'show activity-log' sbcadmin
# Cisco toma \n para la ejecucion de comandos
# Audiocodes toma \r, tener en consideracion en playbooks de Ansible que usan esta libreria
# por otro lado prompt AUDIOCODES = '> ' y CISCO = '>|#'

import os, sys, string, telnetlib
from getpass import getpass

class AutoTelnet:
    def __init__(self, user_list, cmd_list, **kw):
        self.host = kw.get('host', 'localhost')
        self.timeout = kw.get('timeout', 600)
        #self.command_prompt = kw.get('command_prompt', "M800B> ") # on prem SBC
        self.command_prompt = kw.get('command_prompt', "Mediant VE SBC# ") # Cloud SBC cambia prompt
        self.passwd = {}
        for user in user_list:
            self.passwd[user] = getpass("Enter user '%s' password: " % user)
        self.telnet = telnetlib.Telnet(  )
        for user in user_list:
            self.telnet.open(self.host)
            ok = self.action(user, cmd_list)
            if not ok:
                print "Unable to process:", user
            self.telnet.close(  )

    def action(self, user, cmd_list):
        t = self.telnet
        t.write("\n")
        login_prompt = "Username: "
        response = t.read_until(login_prompt, 5)
        if string.count(response, login_prompt):
            print response
        else:
            print('error user!')
            return 0
        t.write("%s\r" % user)
        password_prompt = "Password: "
        response = t.read_until(password_prompt, 3)
        if string.count(response, password_prompt):
            print response
        else:
            print('error password prompt!' + str(response))
            return 0
        t.write("%s\r" % self.passwd[user])
        response = t.read_until(self.command_prompt, 5)
        if not string.count(response, self.command_prompt):
            print('error command prompt!')
            return 0
        for cmd in cmd_list:
            t.write("%s\r" % cmd)
            response = t.read_until(self.command_prompt, self.timeout)
            if not string.count(response, self.command_prompt):
                return 0
                print('error commands!')
            print response
        return 1

if __name__ == '__main__':
    basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    logname = os.environ.get("LOGNAME", os.environ.get("USERNAME"))
    host = 'localhost'
    import getopt
    optlist, user_list = getopt.getopt(sys.argv[1:], 'c:f:h:')
    usage = """
usage: %s [-h host] [-f cmdfile] [-c "command"] user1 user2 ...
    -c  command
    -f  command file
    -h  host  (default: '%s')

Example:  %s -c "echo $HOME" %s
""" % (basename, host, basename, logname)
    if len(sys.argv) < 2:
        print usage
        sys.exit(1)
    cmd_list = []
    for opt, optarg in optlist:
        if opt == '-f':
            for r in open(optarg).readlines(  ):
                if string.rstrip(r):
                    cmd_list.append(r)
        elif opt == '-c':
            command = optarg
            if command[0] == '"' and command[-1] == '"':
                command = command[1:-1]
            cmd_list.append(command)
        elif opt == '-h':
            host = optarg
    autoTelnet = AutoTelnet(user_list, cmd_list, host=host)