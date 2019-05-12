#!/bin/bash

cd /attack/server/others/
counter=0
randWait=$((120+RANDOM%6000))
randWait=1
randAttack=0
randNumberAttack=0
randZcounter=0
randFramecounter=0

RandWaitFunc () {
	randWait=$((120+RANDOM%6000))
}

RandAttackFunc () {
	randAttack=$(($RANDOM%6))
}

RandNumberAttack () {
	randNumberAttack=$((1+$RANDOM%30))
}
RandCounter () {
	randZcounter=$((1+RANDOM%1000))
	randFramecounter=$((randZcounter*2))
}

while true
do
	RandWaitFunc
	RandAttackFunc
	RandNumberAttack
	RandCounter
	echo $randWait
	sleep $randWait
	if [ $randAttack -eq 0 ]
	then
		python attack_generator.py --src -1 --encrypt 1 --zcounter_Inc 0 --fcounter_Inc 0 --date 04:19:10:12 --number $randNumberAttack | python __init__.py
		
	elif [ $randAttack -eq 1 ]
	then
		counter=0
		while [ $counter -ne $randNumberAttack ]
		do
			python attack_generator.py --src -1 --encrypt 1 --zcounter_Inc 1 --fcounter_Inc 1 --zcounter $randZcounter --fcounter $randFramecounter --date today | python __init__.py
			randZcounter=$((randZcounter+1))
			randFramecounter=$((randFramecounter+1))
			counter=$((counter+1))
		done
	elif [ $randAttack -eq 2 ]
	then
		python attack_generator.py --src 0xffffffffffffffff --encrypt 1 --zcounter_Inc 1 --fcounter_Inc 1 --date 04:19:18:05 --number $randNumberAttack | python __init__.py
	elif [ $randAttack -eq 3 ]
	then
		python attack_generator.py --src 0x91e6c1239b209dd2 --encrypt -1 --zcounter_Inc 1 --fcounter_Inc 0 --zcounter 412 --fcounter 428 --date 04:19:01:12 --number $randNumberAttack | python __init__.py
	elif [ $randAttack -eq 4 ]
	then
		python attack_generator.py --src 0x12afb1269b209d0e --encrypt 0 --zcounter_Inc 0 --fcounter_Inc 1 --zcounter 312 --fcounter 624 --date 04:20:5:18 --number $randNumberAttack | python __init__.py
	elif [ $randAttack -eq 5 ]
	then
		python attack_generator.py --src 0x12afb1269b209d0e --encrypt 0 --zcounter_Inc 1 --fcounter_Inc 1 ----zcounter $randZcounter --fcounter $randFramecounter --date 04:19:18:05 --number $randNumberAttack | python __init__.py
	elif [ $randAttack -eq 6 ]
	then
		counter=0
                while [ $counter -ne $randNumberAttack ]
                do
                        python attack_generator.py --src 0x41e6e1346b209cd4 --encrypt 0 --zcounter_Inc 1 --fcounter_Inc 1 --zcounter $randZcounter --fcounter $randFramecounter --date today | python __init__.py
                        randZcounter=$((randZcounter+1))
                        randFramecounter=$((randFramecounter+1))
                        counter=$((counter+1))
                done

	fi
	
done
