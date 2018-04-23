To run, for geoDistance to work, the file GeoLite2-City.mmdb needs to be in the current directory. If there isn't one on hand, download it from https://dev.maxmind.com/geoip/geoip2/geolite2/

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
Another way would be matching the sequence number of the packet to the sequence number that we sent out.


2) list all possible reasons you can think of for not getting the answer when probing an arbitrary host
The packet got lost either in transmit or on reply, the server wasn't responding for whatever reason, any of the routers on the path to the target were malfunctioning.


3) produce the scatterplot of the results
This is included as scatterplot.png.
As we can see in the scatterplot, there is a rough correlation between the distance to the target and the RTT. However, this is a very loose correlation- we would need a very large amount of data before I would be ok with pulling any kind of correlation out of it.
There's simply too much variation in the data to be a strong correlation.

To get this data, to try and get accurate results,I took the conglomorate of multiple trials at different times throughout the day to various websites. I ran the trial, pooled the results, and graphed them.
 I assume the fact that the same website responded differently at different times was due to the DNS resolver sending me to different ip addresses, but I'm not really sure why this was the case.
