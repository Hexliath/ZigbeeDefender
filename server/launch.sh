#!/bin/bash

if [ -c /dev/ttyAMA0 ]
then
sudo whsniff -c 11 |\
sudo tshark -l -o zbee_nwk.seclevel:"AES-128 Encryption, 32-bit Integrity Protection" \
-o "uat:zigbee_pc_keys:\"\x22ZigBeeAlliance09\x22\",\"Normal\",\"Foo\"" \
-Y zbee_zcl -T fields -e zbee_nwk.src64 -e zbee_nwk.dst64 -e wpan.dst_pan \
-e zbee_nwk.security -e zbee_nwk.radius -e zbee_aps.counter -e zbee.sec.counter \
-e data -E separator="/s" -E occurrence="l" -i - | \
python utils/data_preprocessing.py - | python __init__.py -

else  
   echo "Sniffer not found. (/dev/ttyAMA0)"
fi



