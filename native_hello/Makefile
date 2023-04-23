FC = gfortran
FFLAGS = -Wall

SRC = hello.f90
EXE = nativeHello

all:$(EXE)

$(EXE):$(SRC)
	$(FC) $(FFALGS) -o $@ $<

clean:
	rm -f $(EXE)
