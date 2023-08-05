C_Network          = {
                       'DNS'     : '192.168.1.1', 
                       'Gateway' : '192.168.1.1',
                       'Netmask' : '255.255.255.0',
                     }

C_WifiPasswords    =  { 
                        ''         : ('**PWD**' ),
                       
#                       'HotSpot1' : ('**PWD**' ),
#                       'HotSpot2' : ('**PWD**' ),
                      }

C_MQTTCredentials  =  { 
                        '192.168.1.99'  : (None,   None     ),
#                        '192.168.1.98' : ('esp', '*******' ),
                      }

C_DeviceDescriptor =  { 
                       # Target      : (Config,      AP, IP Address,      Broker,         Description                             ),

                         'SimpleIO'  : ('SimpleIO',  '', '192.168.1.100', '192.168.1.99', 'Blink and rotary encoder'              ),
                         'SimpleIO2' : ('SimpleIO2', '', '192.168.1.101', '192.168.1.99', 'Digital I/O and single-wire temp'      ),
                                                     
                         'Dimmer'    : ('Dimmer',    '', '192.168.1.102', '192.168.1.99', 'Dimmer with PWM'                       ),
                         'Neo'       : ('Neo',       '', '192.168.1.103', '192.168.1.99', 'NeoPixel'                              ),
                         'Baro'      : ('Baro',      '', '192.168.1.104', '192.168.1.99', 'Barometer, radar and temp'             ),
                        }
