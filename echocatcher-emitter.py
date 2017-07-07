import socket
import iota
import time
import sys


def main():
    if len(sys.argv)<6:
        print "Usage: echocatcher-emitter.py <hostname> <start-port> <IRI-api> <timeout> <sleep-time>"
        exit(-1)

    #host to broadcast:
    host = sys.argv[1]
    port_start = int(sys.argv[2])
    port_range = 10
    port = port_start

    #window to wait for responses:
    timeout = float(sys.argv[4]) * 60 * 1000
    time_between_broadcasts = float(sys.argv[5]) * 60
    echo_mwm = 16
    iri_api = sys.argv[3]
    i = iota.Iota(iri_api)

    print "EchoCatcher emitter started."
    while True:
        #listen on current port
        server_address = ('0.0.0.0', port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(server_address)

        #prepare echo transaction
        ping_address = 'udp://' + host + ':' + str(port)
        ping_address_trytes = iota.TryteString.from_string(ping_address)
        tx = \
            iota.ProposedTransaction(
                address=iota.Address(ping_address_trytes),
                tag=iota.Tag(b'ECHOCATCHER'),
                value=0
            )
        # send transaction
        print "sending echo transaction:", ping_address,"..."
        i.send_transfer(3,transfers=[tx],min_weight_magnitude=echo_mwm)
        print "echo sent."
        count = 0
        start = time.time()
        while time.time() < start + timeout:
            #listen to responses for X time
            try:
                sock.settimeout((start + timeout - time.time()) / 1000)
                data, server = sock.recvfrom(1024)
                # measure response times
                print 'received "%s"' % data,'after %d seconds' % (time.time() - start)
                count+=1
            except:
                if count == 0:
                    print "no response"
                break

        #increment port to eliminate delayed echos
        sock.close()
        port += 1
        if port >= port_start + port_range:
            port = port_start

        print "sleeping..."
        time.sleep(time_between_broadcasts)



if __name__ == "__main__":
    main()
