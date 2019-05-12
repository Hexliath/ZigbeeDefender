# REAL FRAME

|src | dst | pan_id | encryption_status | radius | zbee_counter | frame_counter | payload |
|-----|:----:|:----:|:----:|:----:|:----:|:----:|----:|
| 00:13:a2:00:41:4f:36:cd | 00:13:a2:00:41:4f:37:55 | 0x0000b0fb | 1 | 30 | 159 | 88623 | 00004198800041c666a4 |

- src : known
- dst : known
- pan_id : identical for all the network
- encryption_status :  always 1
- zbee_counter :  unique and incremental
- frame_counter : unique and incremental
- payload :   

00004198800041c666a4
| device_nb | temp | lum |
|:---|:---:|----:|
| 0000 | 41988000 | 41c666a4 |
| 4 first bits unique and  | 8 bits for temp | 8 bits for lum |
identified with src | has to be approximately linear | between 0 and 65535 |

- date : mounth, day, hours, minutes.

# What can be used to simulate attacks

- src not known by the coordinator
- pan_id different
- encryption_status at 0
- radius has to be the same for all the network
- zbee_counter : unique by src
- frame_counter : unique by src
- payload : device_nb unkown, abnormal temperature or luminosity

# Improvent:

- Adding seconds, and analyse sending frequency
- model en temps réel
  