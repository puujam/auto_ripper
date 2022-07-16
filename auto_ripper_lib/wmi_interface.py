import wmi

class WMIInterface():
    def __init__( self ):
        self.handle = wmi.WMI()

    def get_all_drives( self ):
        return [ WMIDrive(data) for data in self.handle.Win32_CDRomDrive() ]

class WMIDrive():
    def __init__( self, data ):
        self.data = data

    @property
    def id( self ):
        return self.data.DeviceID
    
    @property
    def media_loaded( self ):
        return self.data.MediaLoaded

    @property
    def drive_letter( self ):
        pass