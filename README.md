# echoCatcher

## Emitter
attaches an ECHOCATCHER transaction to the tangle & listens to respones from other nodes.

```
Usage: python echocatcher-emitter.py <hostname> <start-port> <IRI-api> <timeout> <sleep-time>
Example: echocatcher-emitter.py www.google.com 5000 http://localhost:14265 2 10
```
will send a request to ping udp://www.google.com:5000 and listen for 2 minutes, then it sill sleep 10 minutes & request a ping to port 5001 ...


## Client
listens to ECHOCATCHER transactions and answers by pinging the requested host which the node's contact info.

```
Usage: python echocatcher-client.py <slack-username/contact-info>
```
uses zmq messaging, so IRI needs to run with `ZMQ_ENABLED = true` in `.ini` config file.

---

## Installation
`sudo pip install zmq`

`sudo pip install pyota`
