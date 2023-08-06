#!cython
"""
vxi11scan will try to connect to the spcified host and device.
Usage:
  python vxi11scan.py [host [device [command]]]
Argument :
  host ipaddress of the VXI11-device
  device "gpibn,m", "inst0,n", or just "inst0" depending on the device and its setting. It is defaulted to "inst0,0"
  command : default:"*IDN?",
"""

cimport cVXI11
from cVXI11 cimport *


import cython
from socket import *
import time,sys

def device_scan(host="10.9.16.20",device="inst0,0",command="*IDN?"):
    clnt=clnt_create(host, device_core_prog, device_core_version, "tcp")
    if not clnt:
        raise IOError

    create_link_1_arg=Create_LinkParms()
    device_write_1_arg=Device_WriteParms()
    device_read_1_arg=Device_ReadParms()
    device_clear_1_arg=Device_GenericParms()
    device_remote_1_arg=Device_GenericParms()

    
    create_link_1_arg.thisptr.lockDevice=0
    create_link_1_arg.thisptr.lock_timeout=0
    create_link_1_arg.thisptr.device=device

    result_1 = create_link_1(create_link_1_arg.thisptr, clnt)

    print "link created to %s \n"%create_link_1_arg.device
    print "\t Error code:%d\n\t LinkID:%d\n\t port %hd\n\t MaxRecvSize:%ld\n"%(
        	       result_1.error, result_1.lid ,
                       result_1.abortPort, result_1.maxRecvSize)
    # 
    #     create_intr_chan_arg=Device_RemoteFunc()
    #     create_intr_chan_arg.progFamily=VXI11.DEVICE_TCP
    #     create_intr_chan_arg.progNum=VXI11.device_intr_prog
    #     create_intr_chan_arg.progVers=VXI11.device_intr_version
    #     create_intr_chan_arg.hostAddr=socket.gethostbyname(socket.gethostname())
    #     create_intr_chan_arg.hostPort=myPort
    #     intr_link=create_intr_chan_1(create_intr_chan_arg,clnt)

    # check remote or not
    device_remote_1_arg.thisptr.lid=result_1.lid;
    device_remote_1_arg.thisptr.io_timeout=0;
    result_7 = device_remote_1(device_remote_1_arg.thisptr, clnt);

    print "Device is remote. RC:%d\n"%result_7.error

    # send a command
    device_write_1_arg.lid=result_1.lid;
    device_write_1_arg.data.data_val = command
    device_write_1_arg.flags = device_flags_end;
    device_write_1_arg.data.data_len= len(device_write_1_arg.data.data_val)
    result_2 = device_write_1(device_write_1_arg, clnt);
    print "wrote %s\n"%device_write_1_arg.data.data_val

    # read response
    device_read_1_arg.thisptr.lid=result_1.lid;
    device_read_1_arg.thisptr.requestSize=255;
    device_read_1_arg.thisptr.io_timeout=5;
    device_read_1_arg.thisptr.lock_timeout=0;
    device_read_1_arg.thisptr.flags = device_flags_termchrset
    device_read_1_arg.thisptr.termChar='\n';

    result_3 = device_read_1(device_read_1_arg.thisptr, clnt);
    print "%d bytes data read:%s\n"%(result_3.data.data_len,
                                      result_3.data.data_val)
    clnt_destroy (clnt);

def rpcinfo(host):
    import os
    os.system("/usr/sbin/rpcinfo -p %s"%host)

