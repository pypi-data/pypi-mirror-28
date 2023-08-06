# Duckietown world-wide swarm client

This is an experimental swarm client t


## Installation

Install [IPFS](https://ipfs.io/docs/install/).
    
Install this package by using:

    $ pip install --user -U duckietown_swarm
    
## Run

In one terminal, start IPFS by using:

    $ ipfs daemon --enable-pubsub-experiment

In another terminal, run using:

    $ dt-swarm
    
Now put any (log) file in the directory `~/shared-logs`.

These files will be shared with the worldwide swarm. 
  