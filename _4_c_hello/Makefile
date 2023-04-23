
FC=gfortran
CFLAGS=-fPIC
LDFLAGS=-L./ -lplugin

all: myprogram

myprogram: c_hello.o libplugin.so
	$(FC) $(LDFLAGS) -o $@ $^

c_hello.o: c_hello.f90
	$(FC) -c $< -o $@

libplugin.so: hello.c
	gcc $(CFLAGS) -shared -o $@ $<

clean:
	rm -f myprogram c_hello.o libplugin.so
