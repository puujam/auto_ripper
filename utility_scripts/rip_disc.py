import sys
import os
import time

utility_scripts_dir = sys.path[0]
# Keep only the head (remove the "utility_scripts" part at the end)
auto_ripper_dir = os.path.split( utility_scripts_dir )[0]

# Gives us access to import auto_ripper_lib
sys.path.append( auto_ripper_dir )

from auto_ripper_lib import makemkv as makemkv_module

makemkv = makemkv_module.MakeMKV()

discs = makemkv.list_all_drives()

while discs.running:
    if discs.newest_progress_message:
        print( "Current: {:0.1f} Total: {:0.1f}".format( discs.newest_progress_message.current_percent, discs.newest_progress_message.total_percent ), flush = True )
    time.sleep( 0.1 )

if discs.result:
    print( "Identified {} discs. This script will rip only the first.".format( len( discs.result ) ) )
else:
    print( "No discs found! Exiting" )
    exit()

mkv_job = makemkv.mkv( discs.result[0].index, discs.result[0].disc_name )

last_update = None
while mkv_job.running:
    if mkv_job.newest_progress_message and mkv_job.newest_progress_message != last_update:
        last_update = mkv_job.newest_progress_message
        print( "Current: {:0.1f} Total: {:0.1f}".format( mkv_job.newest_progress_message.current_percent, mkv_job.newest_progress_message.total_percent ), flush = True )
    time.sleep( 0.5 )