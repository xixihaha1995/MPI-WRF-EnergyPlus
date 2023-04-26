
FC=gfortran
CFLAGS=-fPIC
LDFLAGS=-L./ -lxxxhhhplugin

all: myprogram

myprogram: c_hello.o libxxxhhhplugin.so
	$(FC) $(LDFLAGS) -o $@ $^

c_hello.o: c_hello.f90
	$(FC) -c $< -o $@

libxxxhhhplugin.so: hello.c
	gcc $(CFLAGS) -shared -o $@ $<

clean:
	rm -f myprogram c_hello.o libxxxhhhplugin.so
