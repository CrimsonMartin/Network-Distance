To run, sudo ./runstuff.sh
this automatically sends the output to the file output.txt

to run distMeasure.py, they need to be run with sudo privledges and using python3
	sudo python3 distMeasure.py
similarly, geoDistance needs to be run in the same way.
	sudo python3 geoDistance.py

when run normally, both of them print to std out, and are fairly self explanatory as to what they're doing.

Direct distance is computed by the distance between me(whoever's running the program) and the target server, while indirect distance is the distance between Cleveland and the target server.


1) how you will match ICMP responses with the probes you are sending out (list all ways you could think of in your report and use the one that you found to work for you) 

the one that worked for me, and I ended up using, is just match the body I sent to the body of the message recieved. Meaning, check that the string "measurement for class project. questions to student ..." was a substring in the packet that was returned. 
Through experimentation, I learned that the normal returned packet for an error was the 28 byte header that was on the packet I sent out, plus another 28 byte UDP header for the return, plus 520 bytes of the original 1472 byte payload. Since I knew that the message string would be returned, I matched that to the packet recieved.
Other ways that would have worked could be matching the duplicate header to the message that I sent, or by checking that the source ip of the packet recieved was indeed from the server I sent a message to originally.

2) list all possible reasons you can think of for not getting the answer when probing an arbitrary host
The packet got lost either in transmit or on reply, the server wasn't responding for whatever reason, any of the routers on the path to the target were malfunctioning.

