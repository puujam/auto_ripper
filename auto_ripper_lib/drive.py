import threading
import time

from . import makemkv as makemkv_module

class AutoRipperDrive:
    def __init__( self, id, makemkv ):
        self.id = id
        self.makemkv = makemkv
        
        self.disc = None
        
        self.monitor_thread = threading.Thread( target = self.monitor_loop )
    
    def monitor_loop( self ):
        while True:
            self.update()
            time.sleep( 1 )
    
    def update( self ):
        pass

    @property
    def status_summary_string( self ):
        return "{}: {}".format( self.id, "idle" )