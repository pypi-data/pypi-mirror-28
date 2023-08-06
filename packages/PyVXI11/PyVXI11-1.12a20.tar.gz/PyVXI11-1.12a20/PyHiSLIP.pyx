cimport PyHiSLIP

import struct 

ctypedef class MessageHeader:
    cdef short prologue #"HS"
    cdef unsigned char messageType
    cdef unsinged char controlCode
    cdef unsinged int messageParameter
    cdef unsinged long payloadLength
    cdef char data[]
    cdef char raw

    def unpack(self,data):
        self.prologue=data[:2]
        self.messageType=data[2]
        self.controlCode=data[3]
        self.messageParameter=data[4:8]
        self.payloadLength=data[8:16]
        self.data=data[16:]

    def pack(self):
        self.raw=struct.pack(
            "2cccil",
            self.prologue,
            self.messageType,
            self.controlCode,
            self.messageParameter,
            self.payloadLength)
        raw +=self.data



cdef HiSLIPDevice:

     def __init__(self):
     	 pass

     def Open(self):
         pass

     def Write(self):
         pass

     def Read(self):
         pass

     def ReadSTB(self):
         pass

     def Clear(self):
         pass

     def Lock(self):
         pass

     def Unlock(self):
         pass

     
