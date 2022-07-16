
import sys
import os

utility_scripts_dir = sys.path[0]
# Keep only the head (remove the "utility_scripts" part at the end)
auto_ripper_dir = os.path.split( utility_scripts_dir )[0]

# Gives us access to import auto_ripper_lib
sys.path.append( auto_ripper_dir )

from auto_ripper_lib import makemkv as makemkv_module

makemkv = makemkv_module.MakeMKV()
makemkv.debug = True

discs = makemkv.list_all_drives()
discs.join()

print( "Identified {} discs. This script will rip only the first.".format( len( discs.result ) ) )

mkv_job = makemkv.mkv( discs.result[0].index )
mkv_job.debug = True
mkv_job.join()