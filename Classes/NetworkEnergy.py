#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673 & pipiche38
#
"""
    Module: NetworkEnergy.py

    Description: Network Energy/Interferences 

"""
"""
    self.EnergyLevel[ nwkid ]
                            ['Status'] ( 'Completed' /* table is completd (all entries collected */
                                         'WaitResponse' /* Waiting for response */
                                         'WaitResponse2' /* Waiting for response */
                                         'ScanRequired' /* A scan is required to get more entries */
                                         'ScanRequired2' /* A scan is required to get more entries */
                            ['Channels'][ Num ] /* Energy Level by Channel for corresponding nwkid
"""


import datetime
from time import time
import os.path
import json

import Domoticz
from Modules.output import sendZigateCmd, maskChannel
from Classes.AdminWidgets import AdminWidgets

CHANNELS = [ '11','15','19','20','25','26']

class NetworkEnergy():

    def __init__( self, PluginConf, ZigateComm, ListOfDevices, Devices, HardwareID):

        self.pluginconf = PluginConf
        self.ZigateComm = ZigateComm
        self.ListOfDevices = ListOfDevices
        self.Devices = Devices
        self.HardwareID = HardwareID

        self.EnergyLevel = None
        self.ScanInProgress = False
        self.nwkidInQueue = []
        self.ticks = 0

    def logging( self, logType, message):

        self.debugNetworkEnergy = self.pluginconf.pluginConf['debugNetworkEnergy']
        if logType == 'Debug' and self.debugNetworkEnergy:
            Domoticz.Log( message)
        elif logType == 'Log':
            Domoticz.Log( message )
        elif logType == 'Status':
            Domoticz.Status( message)
        return


    def _initNwkEnrgy( self, root='0000', target='0000', channels=0):

        def isRouter( nwkid ):
            router = False
            if nwkid == '0000': 
                router = True
            else:
                if 'LogicalType' in self.ListOfDevices[nwkid]:
                    if self.ListOfDevices[nwkid]['LogicalType'] == 'Router':
                        router = True
                if 'DeviceType' in self.ListOfDevices[nwkid]:
                    if self.ListOfDevices[nwkid]['DeviceType'] == 'FFD':
                        router = True
                if 'MacCapa' in self.ListOfDevices[nwkid]:
                    if self.ListOfDevices[nwkid]['MacCapa'] == '8e':
                        router = True
            return router


        self.logging( 'Debug', "_initNwkEnrgy - root: %s target: %s, channels: %s" %(root, target, channels))
        if self.EnergyLevel:
            del self.EnergyLevel

        self.EnergyLevel = {}
        
        if target == root == '0000':
            lstdev = list(self.ListOfDevices)
            if '0000' not in lstdev:
                lstdev.append( '0000' )
            for r in lstdev:
                if isRouter( r ):
                    self.EnergyLevel[ r ] = {}
                    for nwkid in self.ListOfDevices:
                        if nwkid == '0000': continue
                        if nwkid == r: continue
                        if not isRouter( nwkid ):
                            continue
                        self._initNwkEnrgyRecord( r, nwkid , channels)
        elif target == '0000':
            # We do a full scan
            self.EnergyLevel[root] = {}
            for nwkid in self.ListOfDevices:
                if nwkid == '0000': continue
                if not isRouter( nwkid ):
                    continue
                self._initNwkEnrgyRecord( root, nwkid , channels)
        else:
            # We target only this target
            if target in self.ListOfDevices:
                if isRouter( target ):
                    self._initNwkEnrgyRecord( root, target, channels )
        return


    def _initNwkEnrgyRecord( self, root, nwkid, channels):

        self.logging( 'Debug', "_initNwkEnrgyRecord %s <-> %s" %(root, nwkid))

        if nwkid not in self.EnergyLevel[root]:
            self.EnergyLevel[ root ][ nwkid ] = {}
        self.EnergyLevel[ root ][ nwkid ][ 'Status' ]  = 'ScanRequired'
        self.EnergyLevel[ root ][ nwkid ][ 'Tx' ]  =  None
        self.EnergyLevel[ root ][ nwkid ][ 'Failure' ]  = None
        self.EnergyLevel[ root ][ nwkid ][ 'Channels' ]  = {}
        for i in channels:
            self.EnergyLevel[ root ][ nwkid ][ 'Channels' ][ i ]  = None

    def prettyPrintNwkEnrgy( self ):

        for r in self.EnergyLevel:
            for i in self.EnergyLevel[ r ]:
                Domoticz.Log("%s <-> %s : %s" %(r, i, self.EnergyLevel[r][i]['Status']))
                if self.EnergyLevel[i]['Status'] == 'Completed':
                    Domoticz.Log("---> Tx: %s" %(self.EnergyLevel[r][i]['Tx']))
                    Domoticz.Log("---> Failure: %s" %(self.EnergyLevel[r][i]['Failure']))
                    for c in self.EnergyLevel[r][i]['Channels']:
                        Domoticz.Log("---> %s: %s" %(c, self.EnergyLevel[r][i]['Channels'][c]))
        self.logging( 'Debug', "")

    def NwkScanReq(self, root, target, channels):

        # Scan Duration
        scanDuration = 0x02 #
        scanCount = 1

        mask = maskChannel( channels )
        datas = target + "%08.x" %(mask) + "%02.x" %(scanDuration) + "%02.x" %(scanCount)  + "00" + root
    
        if len(self.nwkidInQueue) == 0:
            self.logging( 'Debug', "NwkScanReq - request a scan on channels %s for duration %s an count %s" \
                %( channels, scanDuration, scanCount))
            self.logging( 'Debug', "NwkScan - %s %s" %("004A", datas))
            self.nwkidInQueue.append( ( root, target) )
            sendZigateCmd(self, "004A", datas )
            self.EnergyLevel[ root ][ target ]['Status'] = 'WaitResponse'
            self.ticks = 0


    def start_scan( self, root=None, target=None, channels=None):

        self.logging( 'Debug', "start_scan")
        if self.ScanInProgress:
            Domoticz.Log("a Scan is already in progress")
            return
        self.ScanInProgress = True

        if root is None:
            # We will do a full cross-scan
            root = '0000'
        if target is None:
            # Target will be all Routers
            target = '0000'
        if channels is None:
            # All channels
            channels = CHANNELS
        self._initNwkEnrgy( root, target, channels)
        self._next_scan()

    def do_scan(self, root=None, target=None, channels=None):

        if self.ScanInProgress:
            self._next_scan()

    def _next_scan( self ):

        self.logging( 'Debug', "_next_scan")
        self.ticks += 1
        allRootCompleted = True
        self.logging( 'Debug', "_next_scan - To be scan: %s" %list(self.EnergyLevel))
        for r in self.EnergyLevel:
            waitResponse = False
            breakfromabove = False
            self.logging( 'Debug', "_next_scan - %s against %s" %(r, list(self.EnergyLevel[ r ])))
            for i in self.EnergyLevel[ r ]:
                self.logging( 'Debug', "--> _next_scan - %s <-> %s %s" %(r,i,self.EnergyLevel[ r ][ i ]['Status']))
                if self.EnergyLevel[ r ][ i ]['Status'] == 'Completed':
                    continue
                elif self.EnergyLevel[ r ][ i ]['Status'] == 'TimedOut':
                    continue
                elif self.EnergyLevel[ r ][ i ]['Status'] == 'WaitResponse':
                    waitResponse = True
                    allRootCompleted = False
                    if self.ticks > 2:
                        self.logging( 'Debug', "--> _next_scan - %s <-> %s %s --> TimedOut" %(r,i,self.EnergyLevel[ r ][ i ]['Status']))
                        self.EnergyLevel[ r ][ i ]['Status'] = 'TimedOut'
                        if len(self.nwkidInQueue) > 0:
                            root, entry = self.nwkidInQueue.pop()
                            if r != root and i != entry:
                                Domoticz.Error("Mismatch %s versus %s" %(i, entry))
                    continue
                elif self.EnergyLevel[ r ][ i ]['Status'] == 'ScanRequired':
                    _channels = []
                    for c in self.EnergyLevel[ r ][ i ]['Channels']:
                        _channels.append( c )
                    self.NwkScanReq( r, i, _channels)
                    breakfromabove = True
                    allRootCompleted = False
                    break
            else:
                if not waitResponse:
                    self.logging( 'Debug', "----> %s <-> %s Fully Completed" %(r,i))
                    continue
            self.logging( 'Debug', "----> allRootCompleted: %s, breakfromabove: %s, waitResponse: %s" %(allRootCompleted, breakfromabove, waitResponse))
            if breakfromabove:
                break
        else:
            self.logging( 'Debug', "--> allRootCompleted: %s, breakfromabove: %s, waitResponse: %s" %(allRootCompleted, breakfromabove, waitResponse))
            if allRootCompleted:
                self.logging( 'Debug', "--> All scan completed")
                self.finish_scan()
        self.logging( 'Debug', "allRootCompleted: %s, breakfromabove: %s, waitResponse: %s" %(allRootCompleted, breakfromabove, waitResponse))


    def finish_scan( self ):

        self.logging( 'Debug', "Finish_scan")
        self.ScanInProgress = False

        stamp = int(time())
        storeEnergy = {}
        storeEnergy[stamp] = []
        for r in self.EnergyLevel:
            Domoticz.Status("Network Energy Level Report: %s" %r)
            Domoticz.Status("-----------------------------------------------")
            Domoticz.Status("%6s <- %5s %6s %8s %4s %4s %4s %4s %4s %4s" %('router', 'nwkid', 'Tx', 'Failure', '11','15','19','20','25','26'))
            for nwkid in self.EnergyLevel[ r ]:
                entry = {}
                entry['_NwkId'] = nwkid
                if 'ZDeviceName' in self.ListOfDevices[nwkid]:
                    if self.ListOfDevices[nwkid]['ZDeviceName'] != {}:
                        entry['ZDeviceName'] = self.ListOfDevices[nwkid]['ZDeviceName']
                    else:
                        entry['ZDeviceName'] = nwkid
                if self.EnergyLevel[ r ][nwkid]['Status'] != 'Completed':
                    entry['Tx'] = 0
                    entry['Failure'] = 0
                    entry['Channels'] = []
                    toprint = "%6s <- %5s %6s %8s" %(r, nwkid, self.EnergyLevel[ r ][ nwkid ][ 'Tx' ], self.EnergyLevel[ r ][ nwkid ][ 'Failure' ])
                    for c in CHANNELS:
                        channels = {}
                        channels['Channel'] = c
                        channels['Level'] = 0
                        entry['Channels'].append( channels )
                        toprint += " %4s" %0
                else:
                    entry['Tx'] = self.EnergyLevel[ r ][ nwkid ][ 'Tx' ]
                    entry['Failure'] = self.EnergyLevel[ r ][ nwkid ][ 'Failure' ]
                    entry['Channels'] = []
    
                    toprint = "%6s <- %5s %6s %8s" %(r, nwkid, self.EnergyLevel[ r ][ nwkid ][ 'Tx' ], self.EnergyLevel[ r ][ nwkid ][ 'Failure' ])
                    for c in self.EnergyLevel[ r ][ nwkid ]['Channels']:
                        channels = {}
                        if c not in CHANNELS:
                            continue
                        channels['Channel'] = c
                        channels['Level'] = self.EnergyLevel[ r ][ nwkid ]['Channels'][ c ]
                        entry['Channels'].append( channels )
                        toprint += " %4s" %self.EnergyLevel[ r ][ nwkid ]['Channels'][ c ]
                if r == '0000':
                    storeEnergy[stamp].append( entry )
                Domoticz.Status(toprint)

        self.logging( 'Debug', "Network Energly Level Report: %s" %storeEnergy)

        _filename = self.pluginconf.pluginConf['pluginReports'] + 'NetworkEnergy-' + '%02d' %self.HardwareID + '.json'
        if os.path.isdir( self.pluginconf.pluginConf['pluginReports'] ):
            with open( _filename, 'at') as json_file:
                json_file.write('\n')
                json.dump( storeEnergy, json_file)
        else:
            Domoticz.Error("Unable to get access to directory %s, please check PluginConf.txt" %(self.pluginconf.pluginConf['pluginReports']))

        return


    def NwkScanResponse(self, MsgData):

        MsgSequenceNumber=MsgData[0:2]
        MsgDataStatus=MsgData[2:4]
        MsgTotalTransmission=MsgData[4:8]
        MsgTransmissionFailures=MsgData[8:12]
        MsgScannedChannel=MsgData[12:20]
        MsgScannedChannelListCount=MsgData[20:22]
        MsgChannelListInterference=MsgData[22:len(MsgData)]

        #Decode the Channel mask received
        CHANNELS = { 11: 0x00000800, 12: 0x00001000, 13: 0x00002000, 14: 0x00004000,
                15: 0x00008000, 16: 0x00010000, 17: 0x00020000, 18: 0x00040000,
                19: 0x00080000, 20: 0x00100000, 21: 0x00200000, 22: 0x00400000,
                23: 0x00800000, 24: 0x01000000, 25: 0x02000000, 26: 0x04000000 }

        if MsgDataStatus != '00':
            Domoticz.Error("NwkScanResponse - Status: %s with Data: %s" %(MsgDataStatus, MsgData))

        if len(self.nwkidInQueue) > 0:
            root, entry = self.nwkidInQueue.pop()
        else:
            Domoticz.Error("NwkScanResponse - unexpected message %s" %MsgData)
            return

        channelList = []
        for channel in CHANNELS:
            if int(MsgScannedChannel,16) & CHANNELS[channel]:
                channelList.append( channel )

        channelListInterferences = []
        idx = 0
        while idx < len(MsgChannelListInterference):
            channelListInterferences.append( "%X" %(int(MsgChannelListInterference[idx:idx+2],16)))
            idx += 2

        self.logging( 'Debug', "NwkScanResponse - SQN: %s, Tx: %s , Failures: %s , Status: %s) " \
                %(MsgSequenceNumber, int(MsgTotalTransmission,16), int(MsgTransmissionFailures,16), MsgDataStatus) )

        self.EnergyLevel[ root ][ entry ][ 'Tx' ]  =   int(MsgTotalTransmission,16)
        self.EnergyLevel[ root ][ entry ][ 'Failure' ]  =  int(MsgTransmissionFailures,16)

        for chan, inter in zip( channelList, channelListInterferences ):
            if chan in CHANNELS:
                self.EnergyLevel[ root ][ entry ]['Channels'][ str(chan) ] = int(inter,16)
                self.logging( 'Debug', "     %s <- %s Channel: %s Interference: : %s " %(root, entry, chan, int(inter,16)))

        self.EnergyLevel[ root ][ entry ]['Status'] = 'Completed'
        return

