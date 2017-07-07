import sys
import zmq
import iota
import socket

def main():
    if len(sys.argv)<2:
        print "Usage: echocatcher-client.py <slack-username/contact-info> [zmq-port (default 5556)]"
        exit(-1)

    #fill in contact info
    ping_msg = sys.argv[1]

    echo_catcher = "ECHOCATCHER"
    port = "5556"
    if len(sys.argv) > 2:
        port = sys.argv[2]
        int(port)

    # Socket to talk to server
    context = zmq.Context()
    socketZ = context.socket(zmq.SUB)
    socketZ.connect("tcp://localhost:%s" % port)

    # Subscribe to topic
    topicfilter = "tx"
    socketZ.setsockopt(zmq.SUBSCRIBE, topicfilter)

    # Create a UDP socket to send ping
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    # Process updates
    total_value = 0
    while True:
        string = socketZ.recv()
        topic, hash, address, value, tag, timestamp,currentIndex, lastIndex, bundle, trunk, branch = string.split()
        if echo_catcher in tag:
            print "found an ECHOCATCHER message:"
            print "Sending ping to:"
            message = iota.TryteString(address).as_string()
            print message
            try:
                message = message.replace('udp://','')
                ip,port = message.split(':')
                server_address = (ip, int(port))
                sent = sock.sendto(ping_msg+":"+str(port), server_address)
            except:
                print "error parsing:",message


if __name__ == "__main__":
    main()

