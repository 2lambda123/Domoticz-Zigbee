#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673 & pipiche38
#
"""
    Module: tuya.py

    Description: Tuya specific

"""

import Domoticz

from datetime import datetime, timedelta
import time

from Classes.LoggingManagement import LoggingManagement
from Modules.tools import updSQN, get_and_inc_SQN, is_ack_tobe_disabled, build_fcf, checkAndStoreAttributeValue
from Modules.domoMaj import MajDomoDevice
from Modules.tuyaTools import (tuya_cmd, store_tuya_attribute, get_tuya_attribute)
from Modules.tuyaSiren import tuya_siren_response
from Modules.tuyaTRV import tuya_eTRV_response, TUYA_eTRV_MODEL
from Modules.zigateConsts import ZIGATE_EP
from Modules.basicOutputs import write_attribute,raw_APS_request

# Tuya TRV Commands
# https://medium.com/@dzegarra/zigbee2mqtt-how-to-add-support-for-a-new-tuya-based-device-part-2-5492707e882d

# Cluster 0xef00
# Commands 
#   Direction: Coordinator -> Device 0x00 SetPoint 
#   Direction: Device -> Coordinator 0x01 
#   Direction: Device -> Coordinator 0x02 Setpoint command response

TUYA_MANUF_CODE = '1002'

#   "_TZE200_i48qyn9s" : tuyaReadRawAPS ,

TS011F_MANUF_NAME = ("_TZ3000_wamqdr3f", )
TS0041_MANUF_NAME = ("_TZ3000_xkwalgne", "_TZ3000_peszejy7", "_TZ3000_8kzqqzu4",  "_TZ3000_tk3s5tyg")


# TS0601 
TUYA_ENERGY_MANUFACTURER = ( '_TZE200_fsb6zw01', '_TZE200_byzdayie', )
TUYA_SMARTAIR_MANUFACTURER = ( '_TZE200_8ygsuhe1', )

TUYA_SIREN_MANUFACTURER =  ( '_TZE200_d0yu2xgi', '_TYST11_d0yu2xgi' ,)
TUYA_SIREN_MODEL        =  ( 'TS0601', '0yu2xgi', )

TUYA_DIMMER_MANUFACTURER = ( '_TZE200_dfxkcots', )
TUYA_SWITCH_MANUFACTURER = ( '_TZE200_7tdtqgwv', "_TYST11_zivfvd7h", '_TZE200_oisqyl4o', '_TZE200_amp6tsvy',)
TUYA_2GANGS_SWITCH_MANUFACTURER = ('_TZE200_g1ib5ldv',)
TUYA_3GANGS_SWITCH_MANUFACTURER = ( 'TZE200_oisqyl4o', )

TUYA_CURTAIN_MAUFACTURER = ( "_TZE200_cowvfni3", "_TZE200_wmcdj3aq", "_TZE200_fzo2pocs", "_TZE200_nogaemzt", "_TZE200_5zbp6j0u", \
                            "_TZE200_fdtjuw7u", "_TZE200_bqcqqjpb", "_TZE200_zpzndjez", "_TYST11_cowvfni3", "_TYST11_wmcdj3aq", \
                            "_TYST11_fzo2pocs", "_TYST11_nogaemzt", "_TYST11_5zbp6j0u", "_TYST11_fdtjuw7u", "_TYST11_bqcqqjpb", "_TYST11_zpzndjez", \
                            '_TZE200_rddyvrci', '_TZE200_nkoabg8w', '_TZE200_xuzcvlku', '_TZE200_4vobcgd3', '_TZE200_pk0sfzvr', '_TYST11_xu1rkty3', '_TZE200_zah67ekd', )

TUYA_CURTAIN_MODEL =  ( "owvfni3", "mcdj3aq", "zo2pocs", "ogaemzt", "zbp6j0u", "dtjuw7u", "qcqqjpb", "pzndjez", )

TUYA_THERMOSTAT_MANUFACTURER = ( '_TZE200_aoclfnxz', '_TYST11_zuhszj9s', '_TYST11_jeaxp72v', )
TUYA_eTRV1_MANUFACTURER = ( '_TZE200_kfvq6avy', '_TZE200_ckud7u2l', '_TYST11_KGbxAXL2', '_TYST11_ckud7u2l', )

# https://github.com/zigpy/zigpy/discussions/653#discussioncomment-314395
TUYA_eTRV1_MANUFACTURER = ( '_TYST11_zivfvd7h', '_TZE200_zivfvd7h', '_TYST11_kfvq6avy', '_TZE200_kfvq6avy', '_TYST11_jeaxp72v',)
TUYA_eTRV2_MANUFACTURER = ( '_TZE200_ckud7u2l', '_TYST11_ckud7u2l' ,)
TUYA_eTRV3_MANUFACTURER = ( '_TZE200_c88teujp', '_TYST11_KGbxAXL2', '_TYST11_zuhszj9s', )
TUYA_eTRV_MANUFACTURER =  ( '_TYST11_2dpplnsn', '_TZE200_wlosfena', '_TZE200_fhn3negr', '_TZE200_qc4fpmcn', )
TUYA_eTRV_MODEL =         ( 'TS0601', 'TS0601-eTRV', 'TS0601-eTRV1', 'TS0601-eTRV2', 'TS0601-eTRV3', 'TS0601-thermostat', 'uhszj9s', 'GbxAXL2', '88teujp', \
                             'kud7u2l', 'eaxp72v', 'fvq6avy', 'ivfvd7h',)

TUYA_TS0601_MODEL_NAME = TUYA_eTRV_MODEL + TUYA_CURTAIN_MODEL + TUYA_SIREN_MODEL
TUYA_MANUFACTURER_NAME = ( TUYA_ENERGY_MANUFACTURER + TS011F_MANUF_NAME + TS0041_MANUF_NAME + 
                            TUYA_SIREN_MANUFACTURER +  
                            TUYA_DIMMER_MANUFACTURER + TUYA_SWITCH_MANUFACTURER + TUYA_2GANGS_SWITCH_MANUFACTURER + TUYA_3GANGS_SWITCH_MANUFACTURER +
                            TUYA_CURTAIN_MAUFACTURER +  
                            TUYA_THERMOSTAT_MANUFACTURER + 
                            TUYA_eTRV1_MANUFACTURER + TUYA_eTRV2_MANUFACTURER + TUYA_eTRV3_MANUFACTURER + TUYA_eTRV_MANUFACTURER +
                            TUYA_SMARTAIR_MANUFACTURER )

def tuya_registration(self, nwkid, device_reset=False):
    
    self.log.logging( "Tuya", 'Debug', "tuya_registration - Nwkid: %s" %nwkid)
    # (1) 3 x Write Attribute Cluster 0x0000 - Attribute 0xffde  - DT 0x20  - Value: 0x13
    #  It looks like for Lidl Watering switch the Value is 0x0d ( 13 in decimal )
    EPout = '01'
    write_attribute( self, nwkid, ZIGATE_EP, EPout, '0000', '0000', '00', 'ffde', '20', '13', ackIsDisabled = False)

    # (3) Cmd 0x03 on Cluster 0xef00  (Cluster Specific)
    if device_reset:
        payload = '11' + get_and_inc_SQN( self, nwkid ) + '03'
        raw_APS_request( self, nwkid, EPout, 'ef00', '0104', payload, zigate_ep=ZIGATE_EP, ackIsDisabled = is_ack_tobe_disabled(self, nwkid))

def pollingTuya( self, key ):
    """
    This fonction is call if enabled to perform any Manufacturer specific polling action
    The frequency is defined in the pollingSchneider parameter (in number of seconds)
    """

    #if  ( self.busy or self.ZigateComm.loadTransmit() > MAX_LOAD_ZIGATE):
    #    return True

    return False

def callbackDeviceAwake_Tuya(self, NwkId, EndPoint, cluster):
    """
    This is fonction is call when receiving a message from a Manufacturer battery based device.
    The function is called after processing the readCluster part
    """
    Domoticz.Log("callbackDeviceAwake_Tuya - Nwkid: %s, EndPoint: %s cluster: %s" \
            %(NwkId, EndPoint, cluster))

    return

def tuyaReadRawAPS(self, Devices, NwkId, srcEp, ClusterID, dstNWKID, dstEP, MsgPayload):

    if NwkId not in self.ListOfDevices:
        return
    if ClusterID != 'ef00':
        return
    if 'Model' not in self.ListOfDevices[NwkId]:
        return
    _ModelName = self.ListOfDevices[NwkId]['Model']

    if len(MsgPayload) < 6:
        self.log.logging( "Tuya", 'Debug2', "tuyaReadRawAPS - MsgPayload %s too short" %(MsgPayload),NwkId )
        return

    fcf = MsgPayload[0:2] # uint8
    sqn = MsgPayload[2:4] # uint8
    updSQN( self, NwkId, sqn)

    cmd = MsgPayload[4:6] # uint8

    # Send a Default Response ( why might check the FCF eventually )
    if self.FirmwareVersion and int(self.FirmwareVersion,16) < 0x031e:
        tuya_send_default_response( self, NwkId, srcEp , sqn, cmd, fcf)

    # https://developer.tuya.com/en/docs/iot/tuuya-zigbee-door-lock-docking-access-standard?id=K9ik5898uzqrk    
    
    if cmd == '01': # TY_DATA_RESPONE
        status = MsgPayload[6:8]   #uint8
        transid = MsgPayload[8:10] # uint8
        dp = int(MsgPayload[10:12],16)
        datatype = int(MsgPayload[12:14],16)
        fn = MsgPayload[14:16]
        len_data = MsgPayload[16:18]
        data = MsgPayload[18:]
        self.log.logging( "Tuya", 'Debug2', "tuyaReadRawAPS - command %s MsgPayload %s/ Data: %s" %(cmd, MsgPayload, MsgPayload[6:]),NwkId )
        tuya_response( self,Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data )

    elif cmd == '02': # TY_DATA_REPORT
        status = MsgPayload[6:8]   #uint8
        transid = MsgPayload[8:10] # uint8
        dp = int(MsgPayload[10:12],16)
        datatype = int(MsgPayload[12:14],16)
        fn = MsgPayload[14:16]
        len_data = MsgPayload[16:18]
        data = MsgPayload[18:]
        self.log.logging( "Tuya", 'Debug2', "tuyaReadRawAPS - command %s MsgPayload %s/ Data: %s" %(cmd, MsgPayload, MsgPayload[6:]),NwkId )
        tuya_response( self,Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data )

    elif cmd == '11': # MCU_VERSION_RSP ( Return version or actively report version )
        #Model: TS0601-switch UNMANAGED Nwkid: 92d9/01 fcf: 09 sqn: 6c cmd: 11 data: 02f840
        try:
            transid = MsgPayload[6:10]  # uint16
            version = MsgPayload[10:12] # int8
            store_tuya_attribute( self, NwkId, 'TUYA_MCU_VERSION_RSP', version )
        except:
            Domoticz.Error("tuyaReadRawAPS - MCU_VERSION_RSP error on Payload: %s" %MsgPayload)
        
    elif cmd == '23': # TUYA_REPORT_LOG
        pass

    elif cmd == '24': # Time Synchronisation
        send_timesynchronisation( self, NwkId, srcEp, ClusterID, dstNWKID, dstEP, MsgPayload[6:])

    else:
        self.log.logging( "Tuya", 'Log', "tuyaReadRawAPS - Model: %s UNMANAGED Nwkid: %s/%s fcf: %s sqn: %s cmd: %s data: %s" %(
            _ModelName, NwkId, srcEp, fcf, sqn, cmd, MsgPayload[6:]),NwkId )

def tuya_response( self,Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data ):

    self.log.logging( "Tuya", 'Debug', "tuya_response - Model: %s Nwkid: %s/%s dp: %02x dt: %02x data: %s"
        %(_ModelName, NwkId, srcEp, dp, datatype, data),NwkId )

    if _ModelName in ('TS0601-switch', 'TS0601-2Gangs-switch', 'TS0601-2Gangs-switch'):
        tuya_switch_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName == 'TS0601-SmartAir':
        tuya_smartair_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName == 'TS0601-curtain':
        tuya_smartair_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)
        
    elif _ModelName in ( 'TS0601-thermostat' ):
        tuya_eTRV_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName in ( TUYA_eTRV_MODEL ):
        tuya_eTRV_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName == 'TS0601-sirene':
        tuya_siren_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName == 'TS0601-dimmer':
        tuya_dimmer_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    elif _ModelName == 'TS0601-Energy':
        tuya_energy_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data)

    else:
        attribute_name = 'UnknowDp_0x%02x_Dt_0x%02x' %(dp,datatype)
        store_tuya_attribute( self, NwkId, attribute_name, data ) 
        self.log.logging( "Tuya", 'Log', "tuya_response - Model: %s UNMANAGED Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )

def send_timesynchronisation( self, NwkId, srcEp, ClusterID, dstNWKID, dstEP, serial_number):
    
    #Request: cmd: 0x24  Data: 0x0008
    #0008 60 0d 80 29600d8e39
    if NwkId not in self.ListOfDevices:
        return 
    sqn = get_and_inc_SQN( self, NwkId )

    field1 = '0d'
    field2 = '80'
    field3 = '29'

    EPOCTime = datetime(1970,1,1)
    now = datetime.utcnow()
    UTCTime_in_sec = int((now  - EPOCTime).total_seconds())
    LOCALtime_in_sec = int((utc_to_local( now )  - EPOCTime).total_seconds())

    utctime = "%08x" %UTCTime_in_sec
    localtime = "%08x" %LOCALtime_in_sec
    self.log.logging( "Tuya", 'Debug', "send_timesynchronisation - %s/%s UTC: %s Local: %s" %(
        NwkId, srcEp, UTCTime_in_sec, LOCALtime_in_sec ))

    payload = '11' + sqn + '24' + serial_number + utctime + localtime
    raw_APS_request( self, NwkId, srcEp, 'ef00', '0104', payload, zigate_ep=ZIGATE_EP, ackIsDisabled = is_ack_tobe_disabled(self, NwkId))
    self.log.logging( "Tuya", 'Debug', "send_timesynchronisation - %s/%s " %(NwkId, srcEp ))

def utc_to_local(dt):
    # https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib
    import time
    if time.localtime().tm_isdst:
        return dt - timedelta(seconds = time.altzone)
    else:
        return dt - timedelta(seconds = time.timezone)

def tuya_send_default_response( self, Nwkid, srcEp , sqn, cmd, orig_fcf):
    if Nwkid not in self.ListOfDevices:
        return 
    
    orig_fcf = int(orig_fcf,16)
    frame_type = '%02x' %(0b00000011 & orig_fcf)
    manuf_spec = '%02x' %(( 0b00000100 & orig_fcf ) >> 2)
    direction =  '%02x' %(not (( 0b00001000 & orig_fcf ) >> 3))
    disabled_default =  '%02x' %(( 0b00010000 & orig_fcf ) >> 4)

    if disabled_default == '01':
        return

    fcf = build_fcf( '00', manuf_spec, direction, disabled_default )

    payload = fcf + sqn + '0b' 
    if manuf_spec == '01':
        payload += TUYA_MANUF_CODE[2:4] + TUYA_MANUF_CODE[0:2]
    payload += cmd + '00'
    raw_APS_request( self, Nwkid, srcEp, 'ef00', '0104', payload, zigate_ep=ZIGATE_EP, highpriority=True, ackIsDisabled = is_ack_tobe_disabled(self, Nwkid))
    self.log.logging( "Tuya", 'Debug', "tuya_send_default_response - %s/%s fcf: 0x%s ManufSpec: 0x%s Direction: 0x%s DisableDefault: 0x%s" %(
        Nwkid, srcEp, fcf, manuf_spec, direction, disabled_default ))

# Tuya TS0601 - Switch 1, 2, 3 Gangs
def tuya_switch_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data):
    if dp == 0x01:
        # Switch 1 ( Right in case of 2gangs)
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x01 Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)
        MajDomoDevice(self, Devices, NwkId, '01', '0006', data)

    elif dp == 0x02:
        # Switch 2  (Left in case of 2 Gangs)
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x02 Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)
        MajDomoDevice(self, Devices, NwkId, '02', '0006', data)

    elif dp == 0x03:
        # Switch 3
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x03 Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)
        MajDomoDevice(self, Devices, NwkId, '03', '0006', data)

    elif dp == 0x0d:
        # All switches
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x03 Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)
        MajDomoDevice(self, Devices, NwkId, '01', '0006', data)
        MajDomoDevice(self, Devices, NwkId, '02', '0006', data)
        MajDomoDevice(self, Devices, NwkId, '03', '0006', data)

    elif dp == 0x0e: # Relay Status
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x0e Nwkid: %s/%s decodeDP: %04x data: %s"
             %(NwkId, srcEp, dp, data), NwkId)
        store_tuya_attribute( self, NwkId, 'RelayStatus', int(data,16) ) 

    elif dp == 0x0f: # Light Indicator
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Dp 0x0f Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)
        store_tuya_attribute( self, NwkId, 'LightIndicator', int(data,16) ) 
        

    else:
        attribute_name = 'UnknowDp_0x%02x_Dt_0x%02x' %(dp,datatype)
        store_tuya_attribute( self, NwkId, attribute_name, data ) 
        self.log.logging( "Tuya", 'Debug', "tuya_switch_response - Unknown attribut Nwkid: %s/%s decodeDP: %04x data: %s"
            %(NwkId, srcEp, dp, data), NwkId)

    #  Decode8002 - NwkId: b1ed Ep: 01 Cluster: ef00 GlobalCommand: False Command: 01 Data: 004c 0101 0001 00
    #  raw_APS_request - ackIsDisabled: False Addr: b1ed Ep: 01 Cluster: ef00 ProfileId: 0104 Payload: 006b0b0100
    #  tuya_send_default_response - b1ed/01 fcf: 0x00 ManufSpec: 0x00 Direction: 0x00 DisableDefault: 0x00
    #  tuya_response - Model: TS0601-2Gangs-switch Nwkid: b1ed/01 dp: 01 data: 00
    #  tuya_switch_response - Dp 0x01 Nwkid: b1ed/01 decodeDP: 0001 data: 00

    #  Decode8002 - NwkId: b1ed Ep: 01 Cluster: ef00 GlobalCommand: False Command: 01 Data: 004d 0201 0001 00
    #  raw_APS_request - ackIsDisabled: False Addr: b1ed Ep: 01 Cluster: ef00 ProfileId: 0104 Payload: 006c0b0100
    #  tuya_send_default_response - b1ed/01 fcf: 0x00 ManufSpec: 0x00 Direction: 0x00 DisableDefault: 0x00
    #  tuya_response - Model: TS0601-2Gangs-switch Nwkid: b1ed/01 dp: 02 data: 00
    #  tuya_switch_response - Dp 0x02 Nwkid: b1ed/01 decodeDP: 0002 data: 00

def tuya_switch_command( self, NwkId, onoff, gang=0x01):
     
    self.log.logging( "Tuya", 'Log', "tuya_switch_command - %s OpenClose: %s on gang: %s" %(NwkId, onoff, gang),NwkId )
    # determine which Endpoint
    if gang  not in  (0x01, 0x02, 0x03):
        self.log.logging( "Tuya", 'Error', "tuya_switch_command - Unexpected Gang: %s" %gang)
        return
    if onoff  not in ( '00', '01'):
        self.log.logging( "Tuya", 'Error', "tuya_switch_command - Unexpected OnOff: %s" %onoff)
        return

    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command 
    action = '%02x01' %gang # Data Type 0x01 - Bool
    data = onoff
    self.log.logging( "Tuya", 'Log', "tuya_switch_command - action: %s data: %s" %(action, data))
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)   


def tuya_switch_indicate_light(self, NwkId, light=0x01):
    # 0004 0f 04 0001 01 -- Indicate Switch ( On when On)
    # 0005 0f 04 0001 00 -- Indicate Off
    # 0006 0f 04 0001 02 -- Indicate Position (on when Off )
    self.log.logging( "Tuya", 'Debug', "tuya_switch_indicate_light - %s Light: %s" %(NwkId, light),NwkId )
    # determine which Endpoint
    if light  not in ( 0x00, 0x01, 0x02):
        self.log.logging( "Tuya", 'Error', "tuya_switch_indicate_light - Unexpected light: %s" %light)
        return

    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command 
    action = '0f04'
    data = '%02x' %light
    self.log.logging( "Tuya", 'Debug', "tuya_switch_indicate_light - action: %s data: %s" %(action, data))
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)  


def tuya_switch_relay_status( self, NwkId, gang=0x01, status=0xff):
    # 00070 e04 0001 02  -- Remember last status
    # 00080 e04 0001 01  -- On
    # 00090 e04 0001 00  -- Off
    self.log.logging( "Tuya", 'Debug', "tuya_switch_relay_status - %s Light: %s" %(NwkId, status),NwkId )
    # determine which Endpoint
    if status  not in ( 0x00, 0x01, 0x02, 0xff):
        self.log.logging( "Tuya", 'Error', "tuya_switch_relay_status - Unexpected light: %s" %status)
        return

    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command 
    action = '0e04'
    data = '%02x' %status
    self.log.logging( "Tuya", 'Debug', "tuya_switch_relay_status - action: %s data: %s" %(action, data))
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)   



# Tuya TS0601 - Curtain
def tuya_curtain_response( self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data):
    # dp 0x01 closing -- Data can be 00 , 01, 02 - Opening, Stopped, Closing
    # dp 0x02 Percent control - Percent control 
    # db 0x03 and data '00000000'  - Percent state when arrived at position (report)
    # dp 0x05 and data - direction state 
    # dp 0x07 and data 00, 01 - Opening, Closing
    # dp 0x69 and data '00000028'

    # 000104ef00010102 94fd 02 00000970020000 0202 0004 00000004

    self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - Nwkid: %s/%s dp: %s data: %s" %(NwkId, srcEp, dp, data),NwkId )

    if dp == 0x01: # Open / Closing / Stopped
        self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - Open/Close/Stopped action Nwkid: %s/%s  %s" %(NwkId, srcEp, data),NwkId )
        store_tuya_attribute( self, NwkId, 'Action', data ) 

    elif dp == 0x02:
        # Percent Control
        self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - Percentage Control action Nwkid: %s/%s  %s" %(NwkId, srcEp, data),NwkId )
        store_tuya_attribute( self, NwkId, 'PercentControl', data ) 

    elif dp in ( 0x03, 0x07):
        # Curtain Percentage
        # We need to translate percentage into Analog value between 0 - 255
        level = ( ( int( data, 16)) * 255) // 100
        slevel = '%02x' %level
        self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - Curtain Percentage Nwkid: %s/%s Level %s -> %s" %(NwkId, srcEp, data, level),NwkId )
        store_tuya_attribute( self, NwkId, 'PercentState', data ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0008', slevel)

    elif dp == 0x05:
        self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - Direction state Nwkid: %s/%s Action %s" %(NwkId, srcEp, data),NwkId )
        store_tuya_attribute( self, NwkId, 'DirectionState', data ) 

    elif dp in (0x67, 0x69):  
        level = ( (int( data, 16)) * 255) // 100
        slevel = '%02x' %level
        self.log.logging( "Tuya", 'Debug', "tuya_curtain_response - ?????? Nwkid: %s/%s data %s --> %s" %(NwkId, srcEp, data, level),NwkId )
        MajDomoDevice(self, Devices, NwkId, srcEp, '0008', slevel)
        store_tuya_attribute( self, NwkId, 'dp_%s' %dp, data ) 

    else:
        attribute_name = 'UnknowDp_0x%02x_Dt_0x%02x' %(dp,datatype)
        store_tuya_attribute( self, NwkId, attribute_name, data ) 

def tuya_curtain_openclose( self, NwkId , openclose):
    self.log.logging( "Tuya", 'Debug', "tuya_curtain_openclose - %s OpenClose: %s" %(NwkId, openclose),NwkId )
    # determine which Endpoint
    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command
    action = '0101'
    data = openclose
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)

def tuya_curtain_stop( self, NwkId):
    pass

def tuya_curtain_lvl(self, NwkId, percent):
    self.log.logging( "Tuya", 'Debug', "tuya_curtain_lvl - %s percent: %s" %(NwkId, percent),NwkId )

    level = percent
    # determine which Endpoint
    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command
    action = '0202'
    data = '%08x' %level
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)


#### Tuya Smart Dimmer Switch
def tuya_dimmer_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data):
    #             cmd | status | transId | dp | DataType | fn | len | Data
    #Dim Down:     01     00        01     02      02      00    04   00000334
    #Dim Up:       01     00        01     02      02      00    04   0000005a
    #Switch Off:   01     00        01     01      01      00    01   00
    #Dim Up  :     01     00        01     01      01      00    01   01

    if dp == 0x01: # Switch On/Off
        MajDomoDevice(self, Devices, NwkId, srcEp, '0006', data)
        self.log.logging( "Tuya", 'Debug', "tuya_dimmer_response - Nwkid: %s/%s On/Off %s" %(NwkId, srcEp, data),NwkId )

    elif dp == 0x02: #Dim Down/Up
        # As MajDomoDevice expect a value between 0 and 255, and Tuya dimmer is on a scale from 0 - 1000.
        analogValue = int(data,16) / 10   # This give from 1 to 100
        level = int( (analogValue * 255 ) / 100 )

        self.log.logging( "Tuya", 'Debug', "tuya_dimmer_response - Nwkid: %s/%s Dim up/dow %s %s" %(NwkId, srcEp, int(data,16), level),NwkId )
        MajDomoDevice(self, Devices, NwkId, srcEp, '0008', '%02x' %level)
    else:
        attribute_name = 'UnknowDp_0x%02x_Dt_0x%02x' %(dp,datatype)
        store_tuya_attribute( self, NwkId, attribute_name, data ) 

def tuya_dimmer_onoff( self, NwkId, srcEp, OnOff ):

    self.log.logging( "Tuya", 'Debug', "tuya_dimmer_onoff - %s OnOff: %s" %(NwkId, OnOff),NwkId ) 
    # determine which Endpoint
    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command
    action = '0101'
    data = OnOff
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)

def tuya_dimmer_dimmer( self, NwkId, srcEp, percent ):
    self.log.logging( "Tuya", 'Debug', "tuya_dimmer_dimmer - %s percent: %s" %(NwkId, percent),NwkId )

    level = percent * 10
    # determine which Endpoint
    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command
    action = '0202'
    data = '%08x' %level
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)

#### Tuya Blitzwolf Plug TS0121

def tuya_plug_led_indicator_mode( self, nwkid, mode ):
    # 0x0006 / 0x80001
    # Indicator LED off: 0x00
    # Indicator switch On/Off: 0x01
    # Indicate swicth location: 0x02

    write_attribute( self, nwkid, ZIGATE_EP, '01', '0006', '0000', '01', '8001', '30', mode, ackIsDisabled = True)


# Tuya Smart Cover Switch

def tuya_window_cover_calibration( self, nwkid, start_stop):

    # (0x0102) | Write Attributes (0x02) | 0xf001 | 8-Bit (0x30) | 0 (0x00) | Start Calibration
    # (0x0102) | Write Attributes (0x02) | 0xf001 | 8-Bit (0x30) | 1 (0x01) | End Calibration
    write_attribute( self, nwkid, ZIGATE_EP, '01', '0102', '0000', '00', 'f001', '30', start_stop, ackIsDisabled = True)

def tuya_window_cover_motor_reversal( self, nwkid, mode):

    # (0x0102) | Write Attributes (0x02) | 0xf002 | 8-Bit (0x30) | 0 (0x00) | Off
    # (0x0102) | Write Attributes (0x02) | 0xf002 | 8-Bit (0x30) | 1 (0x01) | On
    write_attribute( self, nwkid, ZIGATE_EP, '01', '0102', '0000', '00', 'f002', '30', mode, ackIsDisabled = True)


def tuya_window_cover_command( self, nwkid, mode ):

    # (0x0006) | Write Attributes (0x02) | 0x8001 | 8-Bit (0x30) | 0 (0x00) | Light Mode 1
    # (0x0006) | Write Attributes (0x02) | 0x8001 | 8-Bit (0x30) | 1 (0x01) | Light Mode 2
    # (0x0006) | Write Attributes (0x02) | 0x8001 | 8-Bit (0x30) | 2 (0x02) | Light Mode 3

    write_attribute( self, nwkid, ZIGATE_EP, '01', '0006', '0000', '00', '8001', '30', mode, ackIsDisabled = True)

def tuya_smartair_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data):

    #             cmd | status | transId | dp | DataType | fn | len | Data
    #              01     00        00     12     02        00   04    00000101   257   --- Temperature
    #              01     00        00     13     02        00   04    0000018d   397   --- Humidity  Confirmed
    #              01     00        01     16     02        00   04    00000002     2   --- 0.002 ppm Formaldéhyde détécté
    #              01     00        01     15     02        00   04    00000001     1   --- VOC 0.1 ppm - Confirmed
    #              01     00        01     02     02        00   04    00000172   370   --- CO2 - Confirmed

    # The device is flooding data every seconds. This could have the impact to flow the Domoticz database/
    if 'AcquisitionFrequency' in self.ListOfDevices[NwkId]['Param'] and self.ListOfDevices[NwkId]['Param']['AcquisitionFrequency'] > 0:
        previous_ts = get_tuya_attribute( self, NwkId, 'TimeStamp_%s' %dp)
        if  previous_ts and ( previous_ts + self.ListOfDevices[NwkId]['Param']['AcquisitionFrequency']) > time.time():
            return
        store_tuya_attribute( self, NwkId, 'TimeStamp_%s' %dp, time.time() ) 

    #Temp/Humi/CarbonDioxyde/CH20/Voc
    if dp == 0x02: # CO2 ppm
        co2_Attribute = '0005'
        co2_ppm = int(data,16)
        store_tuya_attribute( self, NwkId, 'CO2 ppm', co2_ppm, ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0402', co2_ppm ,Attribute_ = co2_Attribute)

    elif dp == 0x12: # Temperature
        temp = int(data,16) / 10
        store_tuya_attribute( self, NwkId, 'Temp', temp ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0402', temp)

    elif dp == 0x13: # Humidity %
        humi = int(data,16) // 10
        store_tuya_attribute( self, NwkId, 'Humi', humi ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0405', humi)

    elif dp == 0x15: # VOC ppm
        voc_Attribute = '0003'
        voc_ppm = int(data,16) / 10
        store_tuya_attribute( self, NwkId, 'VOC ppm', voc_ppm ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0402', voc_ppm, Attribute_ = voc_Attribute)

    elif dp == 0x16: # Formaldéhyde ppm ( Méthanal / CH2O_ppm)
        ch2O_Attribute = '0004'
        CH2O_ppm = int(data,16) / 100
        store_tuya_attribute( self, NwkId, 'CH2O ppm', CH2O_ppm ) 
        MajDomoDevice(self, Devices, NwkId, srcEp, '0402', CH2O_ppm, Attribute_ = ch2O_Attribute)

# Tuya Smart Energy DIN Rail
def tuya_energy_response(self, Devices, _ModelName, NwkId, srcEp, ClusterID, dstNWKID, dstEP, dp, datatype, data):

    if dp == 0x01: # State ???
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s State Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )
        store_tuya_attribute( self, NwkId, 'State', data ) 
        MajDomoDevice(self, Devices, NwkId, '01', '0006', data)
        
    elif dp == 0x11: # Total Energy / 1000
        analogValue = int(data,16) / 1000 
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s Energy Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )
        MajDomoDevice(self, Devices, NwkId, '01', '0702', str(analogValue), Attribute_= '0000')
        checkAndStoreAttributeValue( self, NwkId, '01', '0702', '0000', analogValue )  # Store int
        store_tuya_attribute( self, NwkId, 'Energy', str(analogValue) ) 

    elif dp == 0x12: # Current (Ampere) / 1000
        analogValue = int(data,16) / 1000 
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s Current Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )
        MajDomoDevice(self, Devices, NwkId, '01', '0b04', str(analogValue), Attribute_ = '0508')
        store_tuya_attribute( self, NwkId, 'Current', str(analogValue) ) 

    elif dp == 0x13: #Power / 10
        analogValue = int(data,16) / 10 
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s Power Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )
        checkAndStoreAttributeValue( self, NwkId, '01', '0702', '0400', str(analogValue) )
        MajDomoDevice(self, Devices, NwkId, '01', '0702', str(analogValue))
        store_tuya_attribute( self, NwkId, 'InstantPower', str(analogValue) )  # Store str

    elif dp == 0x14: # Voltage / 10
        analogValue = int(data,16) / 10 
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s Voltage Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )
        MajDomoDevice(self, Devices, NwkId, '01', '0001', str(analogValue))
        store_tuya_attribute( self, NwkId, 'Voltage', str(analogValue) ) 

    else:
        self.log.logging( "Tuya", 'Log', "tuya_energy_response - Model: %s Unknow Nwkid: %s/%s dp: %02x data type: %s data: %s" %(
            _ModelName, NwkId, srcEp,  dp, datatype, data),NwkId )


def tuya_energy_onoff( self, NwkId, OnOff ):
    
    self.log.logging( "Tuya", 'Debug', "tuya_energy_onoff - %s OnOff: %s" %(NwkId, OnOff),NwkId ) 
    # determine which Endpoint
    EPout = '01'
    sqn = get_and_inc_SQN( self, NwkId )
    cluster_frame = '11'
    cmd = '00' # Command
    action = '0101'
    data = OnOff
    tuya_cmd( self, NwkId, EPout, cluster_frame, sqn, cmd, action, data)