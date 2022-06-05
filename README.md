# :fire: ZigbeeDefender
[![CircleCI](https://circleci.com/gh/Hexliath/ZigbeeDefender.svg?style=svg&circle-token=b903dee6add5e184a1e665aa69691c805ffdcdea)](https://circleci.com/gh/Hexliath/ZigbeeDefender)


Zigbee Defender is the result of a research project from ISEN engineering school.
The project aim is to protect a Zigbee home infrastructure using Deep Learning.

The central node (named coordinator) analyses the traffic and detects intrusion (or malicious attemps) and alerts the network owner. 

First of all,  Zigbee Defender has to learn the classic behavior of the targeted network. All data from nodes are collected and a dataset is created. This is the **TRAINING** mode. It has to be run for several day (At least one week).

When the dataset is consistent, a model is trained with the dataset that has been divided in three parts :
- Training set
- Test set
- Verification set


If the model is created, and functionnal (tests are successful), it can be pushed with client software to the central node.

Finally, once the new model is deployed, the mode can be switched to **ENGAGED**. The network is now secured, and any suspicious action will be reported to the owner.

## Install - not working

Clone the project on your host computer.

### Configuration

- password
- database

### Server

#### On the Pi
Run the Raspberry Pi with raspbian installed.

Take note of the IP adrress
Make the opt folder readable

#### On your local computer

`cd ZigbeeDefender`  
`scp server pi@<pi_address>:/opt/`

Then connect to the pi over ssh :  
`ssh pi@<pi_address>`

Install the server and all the requirements :  
`./setup`  

Update the configuration :  
`vim config.ini`


And start the service :  
```sudo systemctl enable zigbeedefender_server && sudo systemctl start zigbeedefender_server ```


### Client


### Devices

Flash arduino



## Documentation 

[`Server.md`](docs/Server.md) : Server architecture and presentation  
[`Client.md`](docs/Client.md) : Client presentation
