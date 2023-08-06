

all:cVXI11 vxi11scan vxi11_device_clear 


cVXI11:setup.py
	python setup.py clean
	python setup.py build

vxi11scan:vxi11_scan
	ln vxi11_scan vxi11scan

vxi11_scan:vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g vxi11_scan.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_scan

device_clear:vxi11_device_clear

vxi11_device_clear:vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c 
	$(CC) -g vxi11_device_clear.c VXI11_clnt.c  VXI11_xdr.c -o vxi11_device_clear
