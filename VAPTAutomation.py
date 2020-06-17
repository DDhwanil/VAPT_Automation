import threading
import Queue
import commands
import sys
import webbrowser
import os
import time
import subprocess
localtime = time.asctime( time.localtime(time.time()) )

fil = str(localtime.replace(' ','_'))
full_fil = fil+'_Report.html'
f = open(full_fil,'w')
message = """<html>
<head><title>Automated Report</title></head>
<body><h1><i>Output</i></h1><br>"""
messageend="""
</body>
</html>"""


myCmd = "kill $(ps -aux | grep '[j]ava -Xmx1984m -jar /usr/share/zaproxy/zap-2.9.0.jar -daemon' | awk '{print $2}')"
os.system(myCmd)
mycmd = "zap-cli -v --zap-path /usr/share/zaproxy/zap.sh start"
os.system(myCmd)

# thread class to run a command
class ExampleThread(threading.Thread):
    def __init__(self, cmd, queue):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.queue = queue

    def run(self):
        # execute the command, queue the result
        (status, output) = commands.getstatusoutput(self.cmd)
        #(status, output) = os.popen('nmap -sV localhost').readlines()
        self.queue.put((self.cmd, output, status))

# queue where results are placed
result_queue = Queue.Queue()

if len(sys.argv)<3:
    print "Usage:  python script.py ip/url 127.0.0.1 or www.google.com"
    sys.exit(1)

# define the commands to be run in parallel, run them
if sys.argv[1] in "ip":
    print('scanning IP')
    cmds = ['perl ./git/enum4linux/enum4linux.pl '+sys.argv[2], './git/testssl.sh/testssl.sh '+sys.argv[2]+' 443'
    , './git/testssl.sh/testssl.sh '+sys.argv[2]+' 3389' , './git/testssl.sh/testssl.sh '+sys.argv[2]+' 8443'
    , 'sslscan '+sys.argv[2]+':443', 'sslscan '+sys.argv[2]+':3389', 'sslscan '+sys.argv[2]+':8443'
    , 'ike-scan '+sys.argv[2]
    , 'showmount -e '+sys.argv[2]
    , 'rpcinfo -p '+sys.argv[2]
    , 'nmblookup -A '+sys.argv[2]
    , 'smbclient -L //'+sys.argv[2]
    , 'rpcclient --no-pass -U "" '+sys.argv[2]
    , 'nbtscan '+sys.argv[2]
    , 'snmpwalk -c public -v1 '+sys.argv[2]+' 1'
    , 'rusers -al '+sys.argv[2]
    , 'finger '+sys.argv[2]
    , 'python3 /root/git/odat/odat.py sidguesser -s '+sys.argv[2]+' -p 1521 --sids-file ./git/odat/sids.txt'
    , 'host -t a '+sys.argv[2]
    , 'host -t mx '+sys.argv[2]
    , 'perl ./git/snmpenum/snmpenum.pl '+sys.argv[2]+' public ./git/snmpenum/windows.txt'
    , 'perl ./git/snmpenum/snmpenum.pl '+sys.argv[2]+' public ./git/snmpenum/linux.txt'
    , 'perl ./git/snmpenum/snmpenum.pl '+sys.argv[2]+' public ./git/snmpenum/cisco.txt'
    , 'snmpwalk -c public '+sys.argv[2]+' -v 2c'
    , 'python3 /git/smbmap/smbmap.py -H '+sys.argv[2]
    , 'python3 /git/smbmap/smbmap.py -u root -p toor -d workgroup -H '+sys.argv[2]
    , 'python3 /git/smbmap/smbmap.py -u administrator -p password -d workgroup -H '+sys.argv[2]
    , 'python3 /git/smbmap/smbmap.py -u admin -p admin -d workgroup -H '+sys.argv[2]
    , 'nmap -T2 -vvv -sV -sC -p- --script all -oA '+sys.argv[2]+fil+' '+sys.argv[2]
    , 'masscan -p1-65535 '+sys.argv[2]' --banners --rate 100']
if sys.argv[1] in "url":
    print('scanning url')
    cmds = ['nikto --url '+sys.argv[2]
    ,'wpscan --url '+sys.argv[2]
    ,'wpscan.rb --url http://'+sys.argv[2]+' --enumerate vp'
    ,'wpscan.rb --url https://'+sys.argv[2]+' --enumerate vp'
    ,'wpscan.rb --url http://'+sys.argv[2]+' --enumerate vt'
    ,'wpscan.rb --url https://'+sys.argv[2]+' --enumerate vt'
    , './git/gobuster/gobuster dir -u '+sys.argv[2]+' -k -w ./git/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt'
    , 'dig '+sys.argv[2]
    , 'curl -i -X OPTIONS http://'+sys.argv[2], 'curl -v -X http://'+sys.argv[2]
    , 'zap-cli -v --zap-path /usr/share/zaproxy/zap.ss quick-scan --spider -r -s all http://'+sys.argv[2]
    , 'zap-cli -v --zap-path /usr/share/zaproxy/zap.ss quick-scan --spider -r -s all https://'+sys.argv[2]
    ]

for cmd in cmds:
    thread = ExampleThread(cmd, result_queue)
    thread.start()

# print results as we get them
while threading.active_count() > 1 or not result_queue.empty():
    while not result_queue.empty():
        (cmd, output, status) = result_queue.get()
        print('%s:' % cmd)
        print(output)
        message = message + '<b><h2>' + ('%s:' %cmd) + '</b></h2>' + '<br>'
        output = output.replace('\n','<br>')
        #lene = len(ouput)
        #for i in range(lene):
         #   print(output[i])
          #  message = message + output[i] + "<br>"

	message = message + '<br>' + output + '<br>' + ('='*60) + '<br><br><br><br><br>'
        print('='*60)
    time.sleep(1)
sage = message + messageend

f.write(message)
f.close()
#Change path to reflect file location

filename = 'file:///'+os.getcwd()+'/' + full_fil
webbrowser.open_new_tab(filename)
sys.exit()
