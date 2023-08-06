#!cython
"""
cVXI11 is a reimplemented version of the VXI11 module. Previous version of VXI11 modules uses SWIG to generate 
glue code. However, cVXI11 module uses cython instead of SWIG to generate glue code between Python and C-library.
"""
cimport cVXI11

#from cVXI11 cimport device_flags_termchrset, device_flags_end, device_flags_waitlock
#from cVXI11 cimport Device_ReadResp_END,Device_ReadResp_CHR
#
import cython
import socket,struct,os,signal
#
#from __future__ import print_function
#

from vxi11Exceptions import *

class Device_AddrFamily:
    DEVICE_TCP = 0
    DEVICE_UDP = 1

# from VXI11.h
cdef enum:
  device_flags_termchrset = 0x80
  device_flags_end = 0x8
  device_flags_waitlock = 0x1
  DEVICE_FLAGS_TERMCHRSET = 0X80
  DEVICE_FLAGS_END = 0X8
  DEVICE_FLAGS_WAITLOCK = 0X1

cdef enum:
  DEVICE_INTR_SRQ= (<u_int>30)
  #device_intr_prog =DEVICE_INTR
  #device_intr_version =DEVICE_INTR_VERSION
  device_intr_srq =DEVICE_INTR_SRQ

# from rpc/clnt.h

cdef enum:
  Device_ReadResp_REQCNT=1
  Device_ReadResp_CHR=2
  Device_ReadResp_END=4
  DEVICE_READRESP_REQCNT=1
  DEVICE_READRESP_CHR=2
  DEVICE_READRESP_END=4

try:
    import threading
    _enableSRQ=True
except ImportError:
    _enableSRQ=False

class device_core:
   prog=<u_int> DEVICE_CORE
   version=<u_int> DEVICE_CORE_VERSION

class device_async:
   prog = <u_int> DEVICE_ASYNC
   version = <u_int> DEVICE_ASYNC_VERSION

class device_intr:
   prog = <u_int> DEVICE_INTR
   version = <u_int> DEVICE_INTR_VERSION
   srq = <u_int> device_intr_srq # VXI11.h does not have the definiton of DEVICE_INTR_SRQ

class device_flags:
   termchrset = <u_int> 0x80;
   end = <u_int> 0x8;
   waitlock = <u_int> 0x1;

class Device_ErrorCode_class:
   No_Error = 0
   Syntax_Error = 1
   not_Accessible = 3
   invalid_Link_Id = 4
   Parm_Error = 5
   Chan_not_Established = 6
   Op_not_Supported = 8
   Out_of_Resoruces = 9
   Dev_Locked_by_Another = 11
   No_Lock_by_this_Link = 12
   IO_Timeout = 15
   IO_Error = 17
   Ivalid_Addr = 21
   Abort = 23
   Already_Established = 29
   Device_ErrorCode_msg = {
       No_Error:"No Error",
       Syntax_Error:"Syntax Error",
       not_Accessible :"not accessible",
       invalid_Link_Id:"Invalid Link Id",
       Parm_Error:"Parm Error",
       Chan_not_Established:"Channel not Established",
       Op_not_Supported : "Operation not Supported",
       Out_of_Resoruces : "Out of Resources",
       Dev_Locked_by_Another : "Device Locked by Another",
       No_Lock_by_this_Link : "No Lock by this Link",
       IO_Timeout :"I/O Timeout",
       IO_Error :"I/O Error",
       Ivalid_Addr :"Invalid Address",
       Abort : "Abort",
       Already_Established : "Channele Already Established"
   }
   @classmethod
   def msg(cls, code):
       return cls.Device_ErrorCode_msg[code]
   
cdef class Device_GenericParms:
    cdef c_Device_GenericParms *thisptr #
    
    def __cinit__(self,lid, flags, lock_timeout, io_timeout):
        self.thisptr=new c_Device_GenericParms()
        if self.thisptr is NULL:
            raise MemoryError()
        self.thisptr.lid=lid
        self.thisptr.flags=flags
        self.thisptr.lock_timeout=lock_timeout
        self.thisptr.io_timeout=io_timeout

    def __init__(self, lid, flags, lock_timeout, io_timeout):
        pass

    def __dealloc__(self):
        #print "dealloc GenericParms"
        if self.thisptr is NULL:
            return 
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_GenericParms,
                     <c_xdr_free_argtype> self.thisptr)
        #del self.thisptr
    
    def getLid(self):
        return self.thisptr.lid

    def getFlags(self):
        return self.thisptr.flags

    def getLockTimeout(self):
        return self.thisptr.lock_timeout

    def getIoTimeout(self):
        return self.thisptr.io_timeout

    property lid:
        def __get__(self): 
            return self.thisptr.lid
        def __set__(self, lid): 
            self.thisptr.lid=lid

    property flags:
        def __get__(self):
            return self.thisptr.flags
        def __set__(self, flags): 
            self.thisptr.flags=flags

cdef class Device_RemoteFunc:
    cdef c_Device_RemoteFunc *thisptr # "this" is a reserved keyword in C++
    def __cinit__(self):
        self.thisptr=new c_Device_RemoteFunc()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __dealloc__(self):
        if self.thisptr is not NULL:
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_RemoteFunc,
                         <c_xdr_free_argtype> self.thisptr)
            #del self.thisptr

    property progFamily:
        def __get__(self): return self.thisptr.progFamily
        def __set__(self,progFamily): self.thisptr.progNum=progFamily

    property progNum:
        def __get__(self): return self.thisptr.progNum
        def __set__(self,progNum): self.thisptr.progNum=progNum

    property progVers:
        def __get__(self): return self.thisptr.progVers
        def __set__(self,progVers): self.thisptr.progVers=progVers

    property hostAddr:
        def __get__(self): return self.thisptr.hostAddr
        def __set__(self, hostAddr): self.thisptr.hostAddr=hostAddr

    property progPort:
        def __get__(self): return self.thisptr.hostPort
        def __set__(self,hostPort): self.thisptr.hostPort=hostPort

cdef class Create_LinkParms:
   cdef c_Create_LinkParms *thisptr # "this" is a reserved keyword in C++
   def __cinit__(self):
       self.thisptr=new c_Create_LinkParms()
       if self.thisptr is NULL:
           raise MemoryError()

   def __dealloc__(self):
       # temp=<long > self.thisptr
       #print "dealloc LinkParms", '0x%x'%temp
       # if self.thisptr:
       # this xdr_free crash system
       #     with nogil:
       #         xdr_free(<xdrproc_t> xdr_Create_LinkParms, self.thisptr)
       if self.thisptr is not NULL:
           del self.thisptr

cdef class Create_LinkResp:
   cdef c_Create_LinkResp *thisptr # "this" is a reserved keyword in C++
   def __cinit__(self):
      self.thisptr=new c_Create_LinkResp()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       with nogil:
           xdr_free(<xdrproc_t> xdr_Create_LinkResp,
                    <c_xdr_free_argtype>  self.thisptr)
       del self.thisptr

cdef class Device_WriteParms:
   cdef c_Device_WriteParms *thisptr #
   def __cinit__(self):
      self.thisptr=new c_Device_WriteParms()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       #print "dealloc WriteParms"
       # this xdr_free crash
       #with nogil:
       #xdr_free(<xdrproc_t> xdr_Device_WriteParms, self.thisptr)
       if self.thisptr is NULL: return 
       del self.thisptr

cdef class Device_ReadParms:
   cdef c_Device_ReadParms *thisptr #
   def __cinit__(self):
       self.thisptr=new c_Device_ReadParms()
       if self.thisptr is NULL:
           raise MemoryError()

   def __dealloc__(self):
       #print "dealloc ReadParms"
       if self.thisptr is NULL: return
       with nogil:
           xdr_free(<xdrproc_t> xdr_Device_ReadParms, <c_xdr_free_argtype> self.thisptr)
       del self.thisptr

cdef class Device_ReadResp:
    cdef c_Device_ReadResp *thisptr #

    def __cinit__(self):
        self.thisptr=new c_Device_ReadResp()
        if self.thisptr == NULL:
            raise MemoryError("cannot allocate Device_ReadResp")


    # def __cinit__(self,c_Device_ReadResp *thisptr):
    #     self.thisptr=thisptr
    
    def __dealloc__(self):
        #print "dealloc ReadResp"
        if self.thisptr is NULL: return 
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> self.thisptr)
        del self.thisptr

    def release(self):
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> self.thisptr)
        self.thisptr = NULL

    def get_binary_data(self):
        if self.thisptr:
            return self.thisptr.data.data_val
        else:
            raise RuntimeError("empty responce")

cdef class Device_ReadStbResp:
   cdef c_Device_ReadStbResp *thisptr#
   def __cinit__(self):
      self.thisptr=new c_Device_ReadStbResp()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       with nogil:
           xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> self.thisptr)
       del self.thisptr

cdef class Device_EnableSrqParms:
   cdef c_Device_EnableSrqParms *thisptr #
   def __cinit__(self):
      self.thisptr=new c_Device_EnableSrqParms()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       #xdr_free(<xdrproc_t> xdr_Device_EnableSrqParms, self.thisptr)
       del self.thisptr

cdef class Device_LockParms:
   cdef c_Device_LockParms *thisptr #
   def __cinit__(self):
       self.thisptr=new c_Device_LockParms()
       if self.thisptr is NULL:
           raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       #with nogil:
       #  xdr_free(<xdrproc_t> xdr_Device_LockParms, self.thisptr)
       del self.thisptr

cdef class Device_DocmdParms:
   cdef c_Device_DocmdParms *thisptr #
   def __cinit__(self):
       self.thisptr=new c_Device_DocmdParms()
       if self.thisptr is NULL:
           raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return 
       #with nogil:
       #  xdr_free(<xdrproc_t> xdr_Device_DocmdParms, self.thisptr)
       del self.thisptr

cdef class Device_DocmdResp:
   cdef c_Device_DocmdResp *thisptr #
   def __cinit__(self):
      self.thisptr=new c_Device_DocmdResp()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       with nogil:
           xdr_free(<xdrproc_t> xdr_Device_DocmdResp, <c_xdr_free_argtype> self.thisptr)
       del self.thisptr

cdef class Device_SrqParms:
   cdef c_Device_SrqParms *thisptr #
   def __cinit__(self):
      self.thisptr=new c_Device_SrqParms()
      if self.thisptr is NULL:
          raise MemoryError()

   def __dealloc__(self):
       if self.thisptr is NULL: return
       with nogil:
           xdr_free(<xdrproc_t> xdr_Device_SrqParms, <c_xdr_free_argtype> self.thisptr)
       #del self.thisptr

cdef class clnt:
    cdef c_CLIENT *thisptr 
    def __init__(self, char *host, u_int prog,u_int vers,char *prot):
        self.thisptr=clnt_create(host, prog, vers, prot)
        if self.thisptr is NULL:
            raise MemoryError()

    def __dealloc__(self):
       if self.thisptr is NULL: return
       clnt_destroy(self.thisptr)

    def perror(self,char *errmsg):
        clnt_perror(self.thisptr, errmsg)   
        return errmsg

    def sperror(self,char *errmsg):
        clnt_sperror(self.thisptr,errmsg)
        return errmsg

cdef class Vxi11Device:
    cdef char *host
    cdef char *device
    cdef char *proto
    cdef Device_Link lid
    cdef u_short abortPort
    cdef u_long maxRecvSize
    cdef unsigned int intr_host
    cdef unsigned short intr_port
    cdef c_CLIENT *clnt
    cdef c_CLIENT *abt
    cdef c_CLIENT *intr
    cdef c_SVCXPRT *svc_xprt
    # python property
    cpdef readonly hostName
    cpdef readonly deviceName
    cpdef readonly protoName
    cpdef readonly intr_socket
    cpdef readonly svc_thread
    cpdef readonly svc_lock
    cpdef readonly srq_port
    cpdef readonly srq_sock

    property lid:
        def __get__(self): 
            return self.lid
        def __set__(self,lid):
            self.lid = lid

    property host:
        def __get__(self):
            return self.host

    property device:
        def __get__(self):
            return self.device

    property proto:
        def __get__(self):
            return self.proto

    property abortPort:
        def __get__(self):
            return self.abortPort

    property maxRecvSize:
        def __get__(self):
            return self.maxRecvSize

    srq_locks=dict() # thread-id:(lock object, osc)
    
    def __init__(self, char * host, char *device="gpib0,0",
                 char *proto="tcp",lock_timeout=0,lockDevice=0):
        cdef u_int prog=device_core.prog
        cdef u_int vers=device_core.version
        cdef int socknum=0

        # Python propeties
        # copy string to Python object  
        self.hostName=str(host)
        self.deviceName=str(device)
        self.protoName=str(proto)
        self.intr_socket=None
        self.svc_thread=None
        #
        self.host=host
        self.device=device
        self.proto=proto
        #
        with nogil:
            self.clnt=clnt_create(host, prog, vers, proto)
        if self.clnt == NULL:
            raise RuntimeError("cannot connect to host. Check output from  /usr/sbin/rpcinfo -p %s"%host)

        parm=Create_LinkParms()
        parm.thisptr.lockDevice=lockDevice
        parm.thisptr.lock_timeout=lock_timeout
        parm.thisptr.device=device
        
        with nogil:
            res= create_link_1(parm.thisptr, self.clnt)
        if (not res):
            raise IOError
        elif (res.error !=0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Create_LinkResp, 
                         <c_xdr_free_argtype> res)
            raise IOError("%d"%res.error)

        self.lid=res.lid
        self.abortPort=res.abortPort
        self.maxRecvSize=res.maxRecvSize
        #
        with nogil:
            xdr_free(<xdrproc_t> xdr_Create_LinkResp, <c_xdr_free_argtype> res)      

        #print "abort port:0x%dX"%res.abortPort,self.host
        #print "maxRecvSize:%ld"%res.maxRecvSize
        
        # DEVICE_ASYNC service is not registered to portmapper. 
        # So we should use clnttcp_create for abort channel.
        # Tek osc has rpc service. #395184 is a service number for abort channel
        if self.hasAsynService(host):
            self.abt=clnt_create(host, 
                                 device_async.prog,
                                 device_async.version,
                                 "tcp")
        # createAbortChannel
        elif (res.abortPort != 0):
            self.abt=createAbtChannel(host, res.abortPort, &socknum,
                                      device_async.prog, device_async.version,
                                      res.maxRecvSize, res.maxRecvSize)
        else:
            self.abt=NULL
            
    def hasAsynService(self,host):
        import os
        comtemp="%%s -t %s 395184"%host # 395184 : VXI11-Asyn service number in TCP
        # search for rpcinfo in /usr/sbin or PATH.
        for path in ["/usr/sbin"]+os.getenv("PATH").split(os.path.pathsep):
            if os.path.exists(os.path.join(path, "rpcinfo")):
                if os.system(comtemp%os.path.join(path, "rpcinfo"))== 0: 
                    return True
                else:
                    return False
        return False
    
    def createSrqSocket(self):
        ds=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ds.connect((self.hostName, 111)) # 111 is a port number for RPC server
        rpcservername=ds.getsockname()[0]
	#print "rpcservername",rpcservername
        ds.close()
        srqBindSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        srqBindSocket.bind((rpcservername, 0)) # follow EPICS/drvVXI11.c
        return srqBindSocket

    def createSVCThread(self):
        cdef c_SVCXPRT *xprt
        cdef bool_t reg
        xprt=svctcp_create(cVXI11.RPC_ANYSOCK, 0, 0)
        if xprt == NULL:
            #raise RuntimeError("cannot create tcp service")
            raise RuntimeError("cannot create udp service")

        with nogil:
            IF UNAME_SYSNAME == "Darwin":
                reg=svc_register(xprt, 
                             cVXI11.DEVICE_INTR, 
                             cVXI11.DEVICE_INTR_VERSION, 
                             <void (*)()> device_intr_1, # we need cast here.
                             0) # we don't use portmapper
            ELSE: # Linux
                reg=svc_register(xprt, 
                                 cVXI11.DEVICE_INTR, 
                                 cVXI11.DEVICE_INTR_VERSION, 
                                 # we need cast here.
                                 <void (*)(c_svc_req *, c_SVCXPRT *)> device_intr_1, 
                                 0) # we don't use portmapper
                
        if not reg:
            # print "svc_register result:",reg
            raise RuntimeError("cannot register RPC server")

        self.svc_xprt=xprt
        self.srq_port=xprt.xp_port
        self.srq_sock=xprt.xp_sock

        def run_svc(): # we can define this function elsewhere.
            with nogil:# we must rlease Python GIL here. Otherwise main thread cannot getback GIL again.
                svc_run()
            return

        self.svc_thread=threading.Thread(name="SRQ_SVC-%s"%(self.srq_port,),
                                         target=run_svc, 
                                         args=())
        self.svc_lock=threading.Lock()
        Vxi11Device.srq_locks[self.svc_thread]=(self.svc_lock, self)
        self.svc_thread.setDaemon(True) # for False, which is Thread default

        #trick to find the local ip which is connected to the device
        ds=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        ds.connect((self.hostName, 111)) #111 is a port number for RPC server
        bs=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        bs.bind((ds.getsockname()[0], 0)) # follow EPICS/drvVXI11.c
        host=bs.getsockname()[0]
        ds.close()
        bs.close()

        pa=socket.inet_aton(host)
        self.intr_host=struct.unpack("!L",pa)[0]

        print "start server",self.svc_thread
        self.svc_thread.start()
        self.create_intr_chan(host=self.intr_host, 
                              intr_port=self.srq_port, 
                              proto=DEVICE_TCP)
        return

    def create_intr_chan(self, host=None, intr_port=None, proto=DEVICE_TCP):
        """
        notify a port number of srq socket to rpc server on device side
        """
        if(not host):
            self.intr_socket=self.createSrqSocket()
            host, self.intr_port=self.intr_socket.getsockname()
            pa=socket.inet_aton(host)
            self.intr_host=struct.unpack("!L",pa)[0]
        else:
            self.intr_host=host
            self.intr_port=intr_port
        print "intr_host/port:","%x"%self.intr_host, self.intr_port

        rf_parm=Device_RemoteFunc()
        rf_parm.thisptr.progFamily=proto
        rf_parm.thisptr.progNum=device_intr.prog
        rf_parm.thisptr.progVers=device_intr.version
        rf_parm.thisptr.hostAddr=self.intr_host
        rf_parm.thisptr.hostPort=self.intr_port
        
        with nogil:
            res=create_intr_chan_1(rf_parm.thisptr, self.clnt)

        if (not res) :
            raise RuntimeError("create_intr_chan failed error Empty return value")
        elif (res.error != 0):
            raise RuntimeError("create_intr_chan failed error %d"%res.error)

        #self.trigger()

    def destroy_intr_chan(self):
        print "destroy intr_chan in destroy_intr_chan method"
        with nogil:
            res=destroy_intr_chan_1(NULL, self.clnt)
        if res and res.error == 0:
            return
        else:
            raise RuntimeError("destroy_intr_chan failed")

    def abort(self):
       cdef int parm
       if self.abt == NULL:
           raise RuntimeError("No abort channel")
       parm=self.lid
       with nogil:
           res=device_abort_1(cython.address(parm), self.abt)
       if res and res.error == 0:
          return
       else:
           if res:
               raise RuntimeError("%d"%res.error)
           else:
               raise RuntimeError("Unknown Error")

    def destroy_link(self):
       cdef int parm
       cdef c_Device_Error *res=NULL

       parm=self.lid
       with  nogil:
           res=destroy_link_1(cython.address(parm),self.clnt)
       if res and res.error == 0:
           return
       else:
           if res:
               raise RuntimeError("destroy_link error:%d"%res.error)
           else:
               raise RuntimeError("destroy_link: Unknown Error")
	
    def __del__(self):
        if (self.clnt != NULL) and (self.svc_thread != None):
            with nogil:
                res=destroy_intr_chan_1(NULL, self.clnt)
            print "intr_chan was destroyed"

        if self.svc_thread:
            if self.svc_thread.isAlive():
                os.killpg(signal.SIGKILL, os.getpgid(os.getpid()))
                self.svc_thread.join()
        if self.clnt:
            with nogil:
                clnt_destroy (self.clnt)


    def remote(self,io_timeout=0):
        parm=Device_GenericParms(self.lid, 0, 0, io_timeout)
        with nogil:
            res = device_remote_1(parm.thisptr, self.clnt)
        if res and res.error == 0:
            return "remote"
        else:
            return "local %d"%res.error

    def local(self, io_timeout=0):
        parm=Device_GenericParms(self.lid, 0, 0, io_timeout)

        with nogil:
            res = device_local_1(parm.thisptr, self.clnt)
        if res and (res.error == 0):
            return "local"
        else:
            return "remote %d"%res.error

    def write(self,cmd="*IDN?;\n"):
       cdef c_Device_WriteResp *res=NULL

       parm=Device_WriteParms()
       parm.thisptr.lid=self.lid;
       parm.thisptr.flags =DEVICE_FLAGS_END
       parm.thisptr.data.data_val = cmd
       parm.thisptr.data.data_len=len(cmd)
       try:
           with nogil:
               res = device_write_1(parm.thisptr, self.clnt)
           if (not res):
               clnt_perror(self.clnt, "")
               raise RuntimeError
           elif (res.error != 0):
               clnt_perror(self.clnt, "")
               with nogil:
                   xdr_free(<xdrproc_t> xdr_Device_WriteResp, <c_xdr_free_argtype> res)           
               raise RuntimeError, res.error
           rsize=res.size
           with nogil:
               xdr_free(<xdrproc_t> xdr_Device_WriteResp, <c_xdr_free_argtype> res)           
           return rsize
       except:
           raise RuntimeError,"device_write Error"

    def read_one(self,
                requestSize=255, io_timeout=3000, lock_timeout=0,
                flags=device_flags_termchrset, termChar="\n"):
        r,reason=self._read_one(reuestSize, io_timeout, lock_timeout,
                                flags, termChar)
        return r

    def _read_one(self,
                requestSize=255, io_timeout=3000, lock_timeout=0,
                flags=device_flags_termchrset, termChar="\n"):
        # read response, timeout in msec.
        parm=Device_ReadParms()
        parm.thisptr.lid=self.lid
        parm.thisptr.requestSize=requestSize
        parm.thisptr.io_timeout=io_timeout
        parm.thisptr.lock_timeout=lock_timeout
        parm.thisptr.flags = int(flags)
        parm.thisptr.termChar= ord(termChar)
        with nogil:
            res=device_read_1(parm.thisptr, self.clnt)
        if (not res):
            raise IOError
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> res)
            raise IOError
        data=res.data.data_val[:res.data.data_len]
        reason=res.reason
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> res)
        return (data, reason)

    def read(self, requestSize=4096,
             io_timeout=3000, lock_timeout=0,
             flags=device_flags_termchrset, termChar="\n"):
        #resp=""
        resp=[]
        r, reason=self._read_one(requestSize=requestSize,
                     io_timeout=io_timeout,
                     lock_timeout=lock_timeout,
                     flags=flags,
                     termChar=termChar)
        if r:
            #resp += r
            resp.append(r)
            #print len(r),
        #print "reason:",self.lastRes_reason,"resp:",len(r),r
        while ((reason & (DEVICE_READRESP_END|DEVICE_READRESP_CHR) == 0)):
            r=None
            try:
                r, reason = self._read_one(requestSize=requestSize,
                                           io_timeout=io_timeout,
                                           lock_timeout=lock_timeout,
                                           flags=flags,
                                           termChar=termChar)
                #print "lastRes:",reason,r,
                if r:
                    #resp +=r
                    resp.append(r)
                    #print len(r)
            except IOError,m:
                print "IO error:read_one in read",m
                raise 
                #break
            except TypeError,m:
                print "TypeError:read_one in read",m
                raise 
                #break
        resp="".join(resp)
        return resp

    def readResponce(self,requestSize=4096,io_timeout=30):
        return self.read(requestSize=requestSize, io_timeout=io_timeout)
    
    def read_raw(self,requestSize=4096,io_timeout=30):
        return self.read(requestSize=requestSize, io_timeout=io_timeout)

    def ask(self, message, io_timeout=3000, termChar="\n", requestSize=4096):
        """ A name borrowed from PyVISA module """
        self.write(message)
        return self.read(io_timeout=io_timeout, termChar=termChar, 
                         requestSize=requestSize)

    def ask_block(self,message, io_timeout=3000, requestSize=255):
        self.write(message)
        return self.readResponce(io_timeout=io_timeout, 
                                 requestSize=requestSize)
        
    def readstb(self, flags=0, lock_timeout=0, io_timeout=5):
        parm=Device_GenericParms(self.lid, flags, lock_timeout, io_timeout)
        with nogil:
            res=device_readstb_1(parm.thisptr, self.clnt)
        if (not res):
            raise RuntimeError
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> res)
            raise RuntimeError
        rstb=res.stb
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> res)
        return rstb

    def trigger(self, flags=0, lock_timeout=0, io_timeout=5):
        parm=Device_GenericParms(self.lid, flags,
                                 lock_timeout, io_timeout)
        with nogil:
            res=device_trigger_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError
        
    def clear(self,flags=0,lock_timeout=0,io_timeout=5):
        parm=Device_GenericParms(self.lid, flags,
                                 lock_timeout,io_timeout)
        with nogil:
            res=device_clear_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError

    def lock(self,flags=0,lock_timeout=0):
        parm=Device_LockParms()
        parm.thisptr.lid=self.lid
        parm.thisptr.flags=flags
        parm.thisptr.lock_timeout=lock_timeout
        with nogil:
            res=device_lock_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError

    def unlock(self):
       cdef int parm
       parm=self.lid
       with nogil:
           res=device_unlock_1(cython.address(parm), self.clnt)
       if (not res) or (res.error != 0):
           raise RuntimeError

    def enable_srq(self,enable=True):
        parm=Device_EnableSrqParms()
        parm.thisptr.lid=self.lid
        if enable:
            parm.thisptr.enable=1
        else:
            parm.thisptr.enable=0
        with nogil:
            res=device_enable_srq_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError("enable_srq_1 failed")

    def docmd(self,cmd, data="", flags=0, io_timeout=5,
              lock_timeout=0, network_order=1, ):
        parm=Device_DocmdParms()
        parm.thisptr.flags=flags
        parm.thisptr.io_timeout=5
        parm.thisptr.lock_timeout=lock_timeout
        parm.thisptr.network_order=1
        parm.thisptr.lid=self.lid
        parm.thisptr.cmd=cmd
        parm.thisptr.datasize=len(data)
        parm.thisptr.data_in.data_in_val=data
        parm.thisptr.data_in.data_in_len=len(data)
        with nogil:
            res=device_docmd_1(parm.thisptr,self.clnt)
        if (not res):
            raise RuntimeError("docmd failed")
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_DocmdResp, 
		         <c_xdr_free_argtype> res)
            raise RuntimeError("docmd failed[%s]"%res.error)
        data=res.data_out.data_out_val[:res.data_out.data_out_len]
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_DocmdResp, 
                     <c_xdr_free_argtype> res)
        return data

    # Common * commsnds

    def CLS(self):
        return self.write("*CLS")

    def qESR(self):
        return self.ask("*ESR?")

    def ESE(self):
        return self.write("*ESE")

    def qESE(self):
        return self.ask("*ESE?")

    def qESR(self):
        return self.ask("*ESR?")
    
    def qIDN(self):
        return self.ask("*IDN?")

    def qLRN(self):
        self.write("*LRN?")
        return self.readResponce()

    def qLRN_as_dict(self):
        self.write("*LRN?")
        s=self.readResponce()
        d=dict([w.split() for w in s.split(";")])
        return d
        
    def OPC(self):
        return self.write("*OPC")

    def qOPC(self):
        return self.ask("*OPC?")
    
    def qOPT(self):
        return self.ask("*OPT?")
    
    def RCL(self,value=0):
        "<value> ::= {0 | 1 | 2 | 3 | 4 |5 | 6 | 7 | 8 | 9}"
        return self.write("*RCL %d"%value)

    def SAV(self,value=0):
        "<value> ::= {0 | 1 | 2 | 3 | 4 |5 | 6 | 7 | 8 | 9}"
        return self.write("*SAV %d"%value)

    def RST(self):
        return self.write("*RST")

    def SRE(self,mask=255):
        """
        <mask> ::= sum of all bits thatare set, 0 to 255; an integer inNR1 format.
        <mask> ::= followingvalues:
        Bit Weight Name Enables
        --- ------ ---- ----------
        7 128 OPER Operation Status Reg
        6 64 ---- (Not used.)
        5 32 ESB Event Status Bit
        4 16 MAV Message Available
        3 8 ---- (Not used.)
        2 4 MSG Message
        1 2 USR User
        0 1 TRG Trigger
        quoted from "600_series_prog_refernce.pdf" by Agilent Tecnology.
        """
        return self.write("*SRE %d"%value)

    def qSRE(self,mask=255):
        return self.ask("*SRE?")

    def qSTB(self):
        """
        <value> ::= 0 to 255; an integer in NR1 format, as shown in the following:
        Bit Weight Name  "1" Indicates
        --- ------ ----  ---------------
        7   128   OPER  Operation status condition occurred. 
        6   64 RQS/ MSS Instrument is requesting service.
        5   32 ESB  Enabled event status condition occurred. 
        4   16 MAV  Message available. (Not used.)
        3   8 ---- 
        2   4 MSG   Message displayed. 
        1   2 USR   User event condition occurred. 
        0   1 TRG   A trigger occurred.
        quoted from "600_series_prog_refernce.pdf" by Agilent Tecnology.
        """
        return self.ask("*STB?")

    def TRG(self):
        return self.write("*TRG")

    def qTST(self):
        return self.ask("*TST?")

    def WAI(self):
        return self.write("*WAI")

# from VXI11_svc.c RPC handler for intr routine
#cdef extern void device_intr_1(c_svc_req *rqstp, c_SVCXPRT *transp)
cdef public int _rpcsvcdirty=0 # export _rpcsvcdirty for C-library

# SVC stubs
cdef public c_Device_Error *device_abort_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_WriteResp *device_write_1_svc(c_Device_WriteParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_WriteResp result
    return &result

cdef public c_Device_ReadResp *device_read_1_svc(c_Device_ReadParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_ReadResp result
    return &result

cdef public c_Device_ReadStbResp * device_readstb_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_ReadStbResp result
    return &result

cdef public c_Device_Error *device_trigger_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_clear_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_remote_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_local_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_lock_1_svc(c_Device_LockParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_unlock_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *device_enable_srq_1_svc(c_Device_EnableSrqParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_DocmdResp *device_docmd_1_svc(c_Device_DocmdParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_DocmdResp result
    return &result

cdef public c_Device_Error *destroy_link_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Device_Error *create_intr_chan_1_svc(c_Device_RemoteFunc *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

cdef public c_Create_LinkResp *create_link_1_svc(c_Create_LinkParms *argp, c_svc_req *rqstp) nogil:
    cdef c_Create_LinkResp result
    return &result

cdef public c_Device_Error *destroy_intr_chan_1_svc(void  *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error result
    return &result

# intr_srq handler
cdef public void *device_intr_srq_1_svc(c_Device_SrqParms *argp, c_svc_req *rqstp) nogil:
    cdef void *result=NULL

    with gil:
        # print "SRQ received",threading.currentThread(), \
        #        argp.handle.handle_len, argp.handle.handle_val[:argp.handle.handle_len]
        try:
            lock, osc=Vxi11Device.srq_locks[threading.currentThread()]
            if lock.locked():
                lock.release()
                #print "SRQ received:" #,int(rqstp.rq_prog)
        except:
            raise
            #return result
    return result 

def test_dso():
    dev=Vxi11Device("169.254.254.254",device="gpib0,7")
    return dev

def test_dpo():
    dev=Vxi11Device("169.254.254.254",device="inst0")
    return dev

# from Table B.1 "Allowed Generic Commands" in vxi-11.2 documents.

cdef enum:
    # name            cmd     data_in/data_len  datasize
    SEND_CMD      = 0x020000 # 0-128             1
    BUS_STATUS_CMD= 0x020001 # 2                 2
    ATN_CNTRL_CMD = 0x020002 # 2                 2
    REN_CNTRL_CMD = 0x020003 # 2                 2
    PASS_CNTRL_CMD= 0x020004 # 4                 4
    BUS_ADRS_CMD  = 0x02000A # 4                 4
    IFC_CNTRL_CMD  =0x020010 # 0                 X

class GenericCommands:
    SEND=SEND_CMD
    BUS_STATUS=BUS_STATUS_CMD
    ATN=ATN_CNTRL_CMD
    REN=REN_CNTRL_CMD
    PASS=PASS_CNTRL_CMD
    BUS_ADRS=BUS_ADRS_CMD
    IFC=IFC_CNTRL_CMD

# from Table B.2 "Table B.2 Received and Returned Values for Bus Status" in vxi-11.2 document
class Bus_Status:
    # name = data_in  return value
    REMOTE=1          # 1 if REN 0 otherwise
    SRQ   =2          # 1 if SRQ 0 otherwise 
    NDAC  =3          # 1 if NDAC 0 otherwise
    SYSTEM_CONTROLLER=4  # 1 or 0
    CONTROLLER_IN_CHARGE=5 # 1 or 0
    TALKER= 6              # 1 or 0
    LISTENER=7             # 1 or 0
    BUS_ADDRESS=8          # TCP/IP IEEE 488.1 interface device's address 0-30

class GPIBInterfaceDevice(Vxi11Device):
    """
    class for TCP/IP IEEE488.1 Interface device, described in the vxi-11.1 
    """
    def SEND(self,data):
        """
        Send arbitrary interface dependent command to the device. 
        """
        return self.docmd(GenericCommands.SEND, data=data)

    def BUS_STATUS(self,data):
        return self.docmd(GenericCommands.BUS_STATUS, data=data)

    def ATN(self,data):
        return self.docmd(GenericCommands.ATN,data=data)

    def REN(self,data):
        return self.docmd(GenericCommands.REN,data=data)

    def PASS(self,data):
        return self.docmd(GenericCommands.PASS,data=data)

    def BUSADRS(self,data):
        return self.docmd(GenericCommands.BUS_ADRS, data=data)

    def IFC(self):
        return self.docmd(GenericCommands.IFC, data="\0")


