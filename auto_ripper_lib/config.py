import configparser
import os
import datetime

class AutoRipperConfig:
    def __init__( self, file_path = None ):
        if not file_path:
            this_module_path = os.path.split( __file__ )[0]
            project_path = os.path.split( this_module_path )[0]
            file_path = os.path.join( project_path, "config.ini" )

        self.parser = configparser.ConfigParser()
        self.parser.read( file_path )

        if self.debug_file_path:
            self.debug_file_handle = open( self.debug_file_path, mode = "a" )
    
    @property
    def makemkv_path( self ):
        return self.parser["MakeMKV"]["install_path"].strip( "\"" )

    @property
    def makemkv_mkv_path( self ):
        return self.parser["MakeMKV"]["mkv_path"].strip( "\"" )

    @property
    def makemkv_minimum_length_seconds( self ):
        return int( self.parser["MakeMKV"]["minimum_length_seconds"] )

    @property
    def debug( self ):
        return self.parser["General"].getboolean( "debug" )
    
    @property
    def debug_file_path( self ):
        return self.parser["General"]["debug_file_path"].strip( "\"" )

    def print_debug( self, string ):
        if self.debug:
            print( string, flush = True )
    
        if self.debug_file_path:
            print( "{},{}".format( datetime.datetime.now().isoformat(), string ), file = self.debug_file_handle, flush = True )