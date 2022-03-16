# ez-iMZ
Exploit for CVE-2022-XXXXX
# Requirements
// Script Requirements (Python)

Ask the user what they want to do:
1. Post Authenticated RCE (With credentials)
2. CSRF to RCE (No Credentials)

Post Authenticated RCE:

Enter the victim IP address:

Enter the victim router web page port (default is 80):

Enter the username for the router login:

Enter the password for the router login:

Enter the LHOST for the reverse shell:

Do you want to start a netcat listener? (yes/no): 

// If user enters no, do not execute netcat listener portion of workflow

Enter the LPORT for the reverse shell:

Workflow Post Authenticated RCE:

Python script will take variables and modify the template post request

--> python script changes the Host header to victim ip address

--> python script changes the Origin header to http://victimip:port (if user hits enter instead of giving a port, then origin is changed to http://victimip 

--> python script changes the Referer header to http://victimip:port (if user hits enter instead of giving a port, then origin is changed to http://victimip 

--> python script changes the json command ip field to LHOST variable

--> python script changes the json command port to LPORT variable

--> python script takes the username and password variable and appends it with a colon (example root:root or admin:admin) and encodes it to base64

--> python script takes base64 value and changes existing Authorization header b64 value with new value

--> python script starts netcat listener

--> python script then sends the new POST request using curl, or http.requests or whatever

CSRF to RCE:

Enter the victim IP address:

Enter the victim port (default is 80):

Do you want to start a netcat listener? (yes/no):

Enter the LHOST for the reverse shell:

Enter the LPORT for the reverse shell:

Do you want to host the CSRF poc? (yes/no):

Enter the port to host the CSRF poc on: 

// If user says no, start netcat listener only

// If user says yes, start netcat listener and run python -m http.server [user variable port]

Workflow CSRF to RCE:

--> python script changes the poc.html template code victim IP web address. If user chooses default, then the poc.html code changes the host only.

--> python script changes the poc.html template code LHOST default value in reverse shell one liner

--> python script changes the poc.html template code LPORT default value in reverse shell one liner

--> python script starts netcat listener only OR if CSRF poc variable user input = yes then

--> python script starts netcat listener AND runs python server to host poc.html
