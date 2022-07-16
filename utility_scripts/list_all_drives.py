import sys
import os

# Helpful for debugging weird import problems
# print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)

utility_scripts_dir = sys.path[0]
# Keep only the head (remove the "utility_scripts" part at the end)
auto_ripper_dir = os.path.split( utility_scripts_dir )[0]

# Gives us access to import auto_ripper_lib
sys.path.append( auto_ripper_dir )

from auto_ripper_lib import wmi_interface
from auto_ripper_lib import makemkv as makemkv_module
from auto_ripper_lib import config
from auto_ripper_lib import makemkv_messages

print( "WMI results:" )
wmi = wmi_interface.WMIInterface()
for drive in wmi.get_all_drives():
    print( "{}: {}media loaded".format( drive.id, "" if drive.media_loaded else "no " ) )

print( "" )

print( "MakeMKV results:" )
config = config.AutoRipperConfig()
makemkv = makemkv_module.MakeMKV( config = config )
parser = makemkv.list_all_drives()

# Just wait it out
parser.thread.join()

for message in parser.result:
    print( "{}: {}".format( message.drive_name, message.disc_name ) )