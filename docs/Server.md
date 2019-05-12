# Server

The server is designed to run on a Raspberry Pi. Pi is used as a Zigbee coordinator node, and is the central node of this project.
Using the raspberry pi allows to have an embedded system.

## Architecture

### Components

- Active connection
- Sniffer Zigbee CC2531
- Raspberry Pi 3

### Ports

- 4001 : Used for administration

## How it works

### Normal working
Any input from the sniffer are send to the server software.


Once processed data looks like this:
```source::destination::pan_id::encryption::radius::zbee_counter::frame_counter::device::sensor::value::hours::minutes::litteral_day::month```

### Administration

Given that the server has to be configured we have implemented an adminisration tool. To avoid data compromissions, all inputs from the client are encrypted. Thus, if a misformatized is sent, server may rise an alert.

#### Format

Commands are base64 encoded and then crypted using AES. 
`CMD::<COMMAND NAME>::<VALUE>`



#### Push a new model

To deploy a new model, 


#### Change mode
