
cdef int HiSLIPPort=4880        # not in /etc/services
cdef int SCPIRawSocketPort=5025 # both udp/tcp
cdef int SCPITelnetPort=5024    # both udp/tcp

cdef enum HiSLIPMessageType:
         Initialize=0
         InitializeResPonce=1
         FatalError=2
         Error=3
         AsynLock=4
         AsynLockResponse=5,
         Data=6
         DataEnd=7
         DeviceClearComplete=8
         DeviceCLearAcknowledge=9
         AsyncRemoteLocalContro=10 
         AsyncRemoteLocalResponcse=11
         Trigger=12 
         Interrupted=13
         AsyncInterrupted=14 
         AsyncMaximumMessageSize=15 
         AsyncMaximumMessageSizeResponse=16
         AsyncInitilalize=17
         AsyncIntializeResponse=18
         AsyncDeviceClear=19
         AsyncServiceRequest=20
         AsynStatusQuery=21
         AsyncStatusResponse=22
         AsyncDeviceClearAcknowledge=23
         AsynLockInfo=24 
         AsynLockInfoResponse=25
         # VendorSpecific 128-255 inclusive

cdef enum FatalErrorCodes:
        UndefinedError=0
        PoorlyFormedMessage=1
        UnEstablishedConnection=2
        InvalidInitializationSequence=3
        ServerRefued=4
        # 5-127 : reserved
        FirstDeviceDefinedError=128
        # 128-255 : Device Defined Error

cdef enum ErrorCode:
        UndefinedError=0
        UnrecognizedMessageType=1
        UnrecognizedControlCode=2
        UnrecognizedVendorDefinedMessage=3
        MessageTooLarge=4
        # 5-127 : Reserved
        FirstDviceDefinedError=128
        #128-255:Device Defined Error

cdef enum  LockControlCode:
        release=0
        request=1

cdef enum LockResponseControlCode:
        fail=0
        success=1
        successSharedLock=2
        error=3

cdef RemoteLocalControlCode:
        disableRemote=0
        enableRemote=1
        disableAndGTL=2
        enableAndGotoRemote=3
        enableAndLockoutLocal=4
        enableAndGTRLLO=5
        justGTL=6


