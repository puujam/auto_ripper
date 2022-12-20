def make_mkv_message_factory( line, config ):
    config.print_debug( line.strip() )

    if ":" in line:
        message_code, message_content = line.split( ":", maxsplit = 1 )

        for message_class in message_classes:
            if message_code == message_class.CODE:
                return message_class( message_content )

        return line
    else:
        return line

class Generic:
    CODE = "MSG"

    def __init__( self, string ):
        self.string = string

class CurrentProgress:
    CODE = "PRGC"

    def __init__( self, string ):
        self.string = string

        split = self.string.split( "," )
        self.code = split[0]
        self.id = split[1]
        self.name = split[2]

class TotalProgress:
    CODE = "PRGT"

    def __init__( self, string ):
        self.string = string

        split = self.string.split( "," )
        self.code = split[0]
        self.id = split[1]
        self.name = split[2]

class ProgressBar:
    CODE = "PRGV"

    def __init__( self, string ):
        self.string = string

        split = self.string.split( "," )
        self.current = int( split[0] )
        self.total = int( split[1] )
        self.max = int( split[2] )

        self.current_percent = (self.current / self.max) * 100
        self.total_percent = (self.total / self.max) * 100

class Drive:
    CODE = "DRV"

    def __init__( self, string ):
        self.string = string

        split = self.string.split( "," )
        self.index = split[0]
        self.visible = True if split[1] == "1" else False
        self.enabled = True if split[2] == "1" else False
        self.flags = split[3].strip( "\"" )
        self.drive_name = split[4].strip( "\"" )
        self.disc_name = split[5].strip( "\"" )

class TitleCount:
    CODE = "TCOUNT"

    def __init__( self, string ):
        self.string = string
        
        self.count = int( string )

class DiscInfo:
    CODE = "CINFO"

    def __init__( self, string ):
        self.string = string

class TitleInfo:
    CODE = "TINFO"

    def __init__( self, string ):
        self.string = string

class StreamInfo:
    CODE = "SINFO"

    def __init__( self, string ):
        self.string = string

message_classes = [
    Generic,
    CurrentProgress,
    TotalProgress,
    ProgressBar,
    Drive,
    TitleCount,
    DiscInfo,
    TitleInfo,
    StreamInfo
]