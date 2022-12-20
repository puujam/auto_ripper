import os
import subprocess
import threading
import time

from . import config as config_module
from . import makemkv_messages

class MakeMKV:
    def __init__( self, config = None ):
        if not config:
            config = config_module.AutoRipperConfig()

        self.config = config

    @property
    def console_path( self ):
        if not hasattr( self, "_console_path" ):
            self._console_path = os.path.join( self.config.makemkv_path, "makemkvcon64.exe" )

        return self._console_path

    def run( self, args ):
        run_list = [ self.console_path, "--robot", "--progress=-same" ]
        run_list.extend( args )

        self.config.print_debug( "Running: \"{}\"".format( " ".join( run_list ) ) )

        process = subprocess.Popen( args = run_list, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, text = True )

        return process
    
    def list_all_drives( self ):
        process = self.run( [ "info", "disc:9999" ] )
        
        return MakeMKVListAllDrivesParser( process, self.config )
    
    def mkv( self, disc_id, folder_name, destination = None ):
        if not destination:
            destination = self.config.makemkv_mkv_path
        
        destination = os.path.join( destination, folder_name )

        process = self.run( [ "mkv",  "--minlength={}".format( self.config.makemkv_minimum_length_seconds ), "disc:{}".format( disc_id ), "all", destination ] )
        
        return MakeMKVRipParser( process, self.config )
    
    def get_drive_info( self, drive_index ):
        process = self.run( [ "info", "--minlength={}".format( self.config.makemkv_minimum_length_seconds ), "disc:{}".format( drive_index ) ] )
        
        return MakeMKVDriveInfoParser( process, self.config )

class MakeMKVOutputParser:
    def __init__( self, process, config ):
        self.process = process
        self.config = config

        self.messages = list()
        self.newest_progress_message = None
        self.result = None

        self.thread = threading.Thread( target = self.update )
        self.thread.start()

    @property
    def running( self ):
        return True if self.process.poll() == None else False

    def join( self ):
        return self.thread.join()
    
    def update( self ):
        while self.running:
            line = self.process.stdout.readline()
            if not line:
                pass

            message = makemkv_messages.make_mkv_message_factory( line, self.config )

            if type(message) == makemkv_messages.ProgressBar:
                self.newest_progress_message = message

            self.messages.append( message )
        
        self.parse_results()

    def parse_results( self ):
        """Should be overridden by children"""
        pass

class MakeMKVListAllDrivesParser( MakeMKVOutputParser ):
    def __init__( self, process, config ):
        super().__init__( process, config )
    
    def parse_results( self ):
        # Result is a list of drive info
        self.drives = list()

        for message in self.messages:
            if type( message ) == makemkv_messages.Drive:
                # Filter out drives without a name, they don't seem to be legit
                if message.drive_name:
                    self.drives.append( message )

class MakeMKVRipParser( MakeMKVOutputParser ):
    def __init__( self, process, config ):
        super().__init__( process, config )
    
    def parse_results( self ):
        # No real result for this command
        pass

class MakeMKVDriveInfoParser( MakeMKVOutputParser ):
    def __init__( self, process, config ):
        super().__init__( process, config )
        
    def parse_results( self ):
        self.disc = None
        self.titles = list()