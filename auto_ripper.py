import time
import threading

from auto_ripper_lib import drive as drive_module
from auto_ripper_lib import config as config_module
from auto_ripper_lib import makemkv as makemkv_module

class Globals:
    latest_drive_scan = list()
    drive_monitor_thread_running = True

def main():
    try:
        drives = list()
        
        config = config_module.AutoRipperConfig()
        makemkv = makemkv_module.MakeMKV( config = config )
        
        drive_monitor_thread = threading.Thread( target = drive_monitor_work, args = [ makemkv ] )
        drive_monitor_thread.start()

        while True:
            drives = update_drives( drives, makemkv )
            
            if drives:
                for drive in drives:
                    print( drive.status_summary_string )
            else:
                print( "No drives" )
            
            print( "Loop end." )
            time.sleep( 1 )
    except KeyboardInterrupt as ex:
        print( "interrupt detected" )
        Globals.drive_monitor_thread_running = False
        drive_monitor_thread.join()

def update_drives( drives, makemkv ):
    prior_drive_ids = { drive.id for drive in drives }
    current_drive_ids = { drive.index for drive in Globals.latest_drive_scan }
    
    new_drive_ids = current_drive_ids - prior_drive_ids
    lost_drive_ids = prior_drive_ids - current_drive_ids
    
    for new_drive_id in new_drive_ids:
        print( "Found new drive at index {}".format( new_drive_id ) )
        drives.append( drive_module.AutoRipperDrive( new_drive_id, makemkv ) )
    
    for lost_drive_id in lost_drive_ids:
        print( "Drive at index {} disconnected".format( lost_drive_id ) )
        to_remove = None

        for drive in drives:
            if drive.id == lost_drive_id:
                to_remove = drive
                break
        
        if to_remove != None:
            drives.remove( to_remove )
    
    return drives

def drive_monitor_work( makemkv ):
    """Detects added and removed drives."""

    while Globals.drive_monitor_thread_running:
        drives = makemkv.list_all_drives()
        drives.join()
        
        Globals.latest_drive_scan = drives.result
        
        time.sleep( 5 )

if __name__ == "__main__":
    main()