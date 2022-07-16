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
        self.debug = False

    @property
    def console_path( self ):
        if not hasattr( self, "_console_path" ):
            self._console_path = os.path.join( self.config.makemkv_path, "makemkvcon64.exe" )

        return self._console_path

    def run( self, command, args ):
        run_list = [ self.console_path, "--robot", "--progress=-same", command ]
        run_list.extend( args )

        if self.debug:
            print( "Running: \"{}\"".format( " ".join( run_list ) ), flush = True )

        process = subprocess.Popen( run_list, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, text = True )

        return MakeMKVOutputParser( process, command )
    
    def list_all_drives( self ):
        return self.run( "info", [ "disc:9999" ] )
    
    def mkv( self, disc_id, destination = None ):
        if not destination:
            destination = self.config.makemkv_mkv_path

        return self.run( "mkv", [  "--minlength={}".format( self.config.makemkv_minimum_length_seconds ), "disc:{}".format( disc_id ), "all", destination ] )

class MakeMKVOutputParser:
    def __init__( self, process, command ):
        self.process = process
        self.command = command
        self.messages = list()
        self.result = None
        self.debug = False

        self.thread = threading.Thread( target = self.update_loop )
        self.thread.start()

    @property
    def running( self ):
        return False if not self.process.poll() else True

    def join( self ):
        return self.thread.join()
    
    def update( self ):
        for line in self.process.stdout.readlines():
            message = makemkv_messages.make_mkv_message_factory( line )

            if type(message) == makemkv_messages.ProgressBar:
                self.newest_progress_message = message

                if self.debug:
                    print( "Current: {} Total: {}".format( message.current_percent, message.total_percent ), flush = True )

            self.messages.append( message )

    def update_loop( self ):
        while self.running:
            self.update()
            time.sleep(0.25)

        # One last update after process closes
        self.update()
        self.parse_results()

    def parse_results( self ):
        if self.command == "info":
            # Result is a list of drive info
            self.result = list()

            for message in self.messages:
                if type( message ) == makemkv_messages.Drive:
                    # Filter out drives without a name, they don't seem to be legit
                    if message.drive_name:
                        self.result.append( message )
        elif self.command == "mkv":
            # No real result for this command
            self.result = None