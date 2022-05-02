HDF5DIR=/usr/include/hdf5/serial
EVENTDIR=../../simu/GRAND/c-aires-reader/src
ANTENNADIR=../c-antenna-test/src
ROOTSYS = /home/bram/root
libgrand_utillib.a: Makefile aires_util.c hardware_util.c antenna_util.c complex_util.c fft_util.c matrix.c io_util.c reco_util.c
	g++ -c -I$(HDF5DIR) -I$(ANTENNADIR) -I$(ROOTSYS)/include aires_util.c antenna_util.c hardware_util.c complex_util.c fft_util.c matrix.c reco_util.c io_util.c 
	ar -rv libgrand_utillib.a aires_util.o antenna_util.o hardware_util.o complex_util.o matrix.o fft_util.o io_util.o reco_util.o
