#!/bin/env python3

import os
import sys
import logging
import gpsd
import maidenhead as mh

#requires: pip3 install gpsd-py3 maidenhead

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywsjtx
import pywsjtx.extra.simple_server

# Simple software for linux using gpsd to update wsjtx.


IP_ADDRESS = '224.1.1.1'
PORT = 5007
UPDAE_TXT = False

logging.basicConfig(level=logging.DEBUG)


def get_grid(packet):
    lat, lon = packet.position()

    gridsq = mh.to_maiden(lat,lon)
    return gridsq.upper()



wsjtx_id = None
gps_grid = ""

s = pywsjtx.extra.simple_server.SimpleServer(IP_ADDRESS,PORT)

print("Starting wsjt-x message server")

gpsd.connect()
while True:

    (pkt, addr_port) = s.rx_packet()
    if (pkt != None):
        the_packet = pywsjtx.WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
        if wsjtx_id is None and (type(the_packet) == pywsjtx.HeartBeatPacket):
            # we have an instance of WSJTX
            print("wsjtx detected, id is {}".format(the_packet.wsjtx_id))
            print("starting gps monitoring")
            wsjtx_id = the_packet.wsjtx_id
            # start up the GPS reader
            packet = gpsd.get_current()
            gps_grid = get_grid(packet)
        if type(the_packet) == pywsjtx.StatusPacket:
            if gps_grid != "" and the_packet.de_grid != gps_grid:
                print("Sending Grid Change to wsjtx-x, old grid:{} new grid: {}".format(the_packet.de_grid, gps_grid))
                grid_change_packet = pywsjtx.LocationChangePacket.Builder(wsjtx_id, "GRID:"+gps_grid)
                logging.debug(pywsjtx.PacketUtil.hexdump(grid_change_packet))
                s.send_packet(the_packet.addr_port, grid_change_packet)
                # for fun, change the TX5 message to our grid square, so we don't have to call CQ again
                # this only works if the length of the free text message is less than 13 characters.
                if UPDATE_TXT and  len(the_packet.de_call <= 5):
                    free_text_packet = pywsjtx.FreeTextPacket.Builder(wsjtx_id,"73 {} {}".format(the_packet.de_call, the_packet[0:4]),False)
                    s.send_packet(addr_port, free_text_packet)

        print(the_packet)
