import socket
import time

#   michael folz maf152
#
#   based on python-traceroute.py, found on
#   https://gist.github.com/jcjones/0f3f11a785a833e0a216
#   which is written by jcjones

#MTY size, in this case 1500 bytes
MTU = 1500
#global variables for easy changing of stuff
target_file = 'targets.txt'
#TTL that gets sent on outgoing packets
ttl = 30
#attempts we make without getting response
max_tries = 5
#timeout in seconds
max_timeout = 1
#port we're sedning stuff too
destination_portnum = 33434
#sticks this guy onto the packets we send
messageHeader = "measurement for class project. questions to student maf152@case.edu or professor mxr136@case.edu"

def main():
    global target_file
    # targets stores the list of stuff we're testing
    targets = open(target_file, 'r')
    for line in targets:
        #measure the hops and stuff
        destination_host_name = line.split()[0]
        measure_hops(destination_host_name)
        #line break to make it look purty
        print ()
    targets.close()

#returns the bytes that we want our testing message to be
def make_message():
    global messageHeader
    global MTU
    #28 bytes for the header of a UDP packet
    messagePayload = 'a' * (MTU - len(messageHeader) - 28)
    return bytes (messageHeader + messagePayload, 'ascii')

#convert from end time and start time to the total rtt time (ms)
def time_in_ms (end_time, start_time):
    return 1000 * (end_time - start_time)

#defines if it's a valid return packet
#checks if our message header is somewhere within the packet
def is_invalid_response(response):
    global messageHeader
    if messageHeader in response:
        return False
    else:
        return True


#measure the hops to get to target_host_name
def measure_hops(destination_host_name):
    #import global variables since python has weird scoping
    global ttl
    global max_tries
    global max_timeout
    global destination_portnum
    import time
    global messageHeader

    destination_ip = socket.gethostbyname(destination_host_name)
    print("dest hostname: %s    dest ip: %s" % (destination_host_name, destination_ip))

    message = make_message()

    #create sender socket using udp protocol and a ttl of 50- assuming this is high enough to reach wherever we're going
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    #create the listener socket for the response
    listener = socket.socket(socket.AF_INET, socket.SOCK_RAW,  socket.IPPROTO_ICMP)
    #wait max_timeout for a response(in seconds)
    listener.settimeout(max_timeout)
    finished = False
    tries = 0

    while (not finished and tries < max_tries):
        print("try: %d" % (tries), end = '\r')
        #rtt timer - do this last right before we send the packet for maximum accuracy
        start_time = time.time()

        sender.sendto(message, (destination_ip, destination_portnum))

        try:

            data = listener.recv(1500)

            end_time = time.time()
            finished = True

        except socket.error:
            tries += 1


    sender.close()
    listener.close()


    if not finished:
        print ("%s no response recieved" % (destination_host_name))
        return


    #check that it's the right response packet
    if is_invalid_response(str(data)):
        print("unknown response recieved")
        return

    #get info about the response
    icmp_type = ord(data[20:21])
    icmp_code = ord(data[21:22])
    response_ttl = ord(data[36:37])

    hops = ttl - response_ttl
    time = time_in_ms(end_time, start_time)

    print("hops: %d" % hops)
    print("time(ms): %d" % time)
    #strip return header and get the length of the rest of the packet (udp -> 20 + 8 = 28)
    global MTU
    print("message returned: %d/%d bytes" %(len(data), MTU))

#calls main function
if __name__ == "__main__":
    main()
