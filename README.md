# ipc-test
This is a test repo for verifying the behavior of IPC mechanisms (both on linux hosts and in a k8s cluster).

It includes source code for example producer/consumers of Unix domain sockets, as well as dockerfiles for producing container images.

Example kubernetes configuration files have been added to simplify testing.  

## Examples
Example clients are controlled in their respective directories:
* c: Example of producer/consumer communications using mq.
* python: Example of producer/consumer communications using Unix Domain Socket. 
  * Note: This requires a shared volume mount between the producer and consumer.
