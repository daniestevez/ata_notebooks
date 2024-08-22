KPL/FK
 
   FILE: spice/ata.tf
 
   This file was created by PINPOINT.
 
   PINPOINT Version 3.3.0 --- December 13, 2021
   PINPOINT RUN DATE/TIME:    2023-09-12T19:38:33
   PINPOINT DEFINITIONS FILE: pinpoint-definitions.txt
   PINPOINT PCK FILE:         spice/pck00010.tpc
   PINPOINT SPK FILE:         spice/ata.bsp
 
   The input definitions file is appended to this
   file as a comment block.
 
 
   Body-name mapping follows:
 
\begindata
 
   NAIF_BODY_NAME                      += 'ATA'
   NAIF_BODY_CODE                      += 399999
 
\begintext
 
 
   Reference frame specifications follow:
 
 
   Topocentric frame ATA_TOPO
 
      The Z axis of this frame points toward the zenith.
      The X axis of this frame points North.
 
      Topocentric frame ATA_TOPO is centered at the
      site ATA, which has Cartesian coordinates
 
         X (km):                 -0.2524163678123E+04
         Y (km):                 -0.4123372633635E+04
         Z (km):                  0.4147764944198E+04
 
      and planetodetic coordinates
 
         Longitude (deg):      -121.4733000000000
         Latitude  (deg):        40.8175000000000
         Altitude   (km):         0.1007999999999E+01
 
      These planetodetic coordinates are expressed relative to
      a reference spheroid having the dimensions
 
         Equatorial radius (km):  6.3781366000000E+03
         Polar radius      (km):  6.3567519000000E+03
 
      All of the above coordinates are relative to the frame ITRF93.
 
 
\begindata
 
   FRAME_ATA_TOPO                      =  1399999
   FRAME_1399999_NAME                  =  'ATA_TOPO'
   FRAME_1399999_CLASS                 =  4
   FRAME_1399999_CLASS_ID              =  1399999
   FRAME_1399999_CENTER                =  399999
 
   OBJECT_399999_FRAME                 =  'ATA_TOPO'
 
   TKFRAME_1399999_RELATIVE            =  'ITRF93'
   TKFRAME_1399999_SPEC                =  'ANGLES'
   TKFRAME_1399999_UNITS               =  'DEGREES'
   TKFRAME_1399999_AXES                =  ( 3, 2, 3 )
   TKFRAME_1399999_ANGLES              =  ( -238.5267000000000,
                                             -49.1825000000000,
                                             180.0000000000000 )
 
\begintext
 
 
Definitions file pinpoint-definitions.txt
--------------------------------------------------------------------------------
 
begindata
 
   SITES = ( 'ATA' )
   ATA_FRAME = 'ITRF93'
   ATA_CENTER = 399
   ATA_IDCODE = 399999
   ATA_LATLON = ( 40.8175, -121.4733, 1.008 )
   ATA_UP = 'Z'
   ATA_NORTH = 'X'
 
begintext
 
begintext
 
[End of definitions file]
 
