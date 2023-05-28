CC = mpicc
CFLAGS = -Wall -Wextra -pthread
LDFLAGS = -pthread

TARGET = mpi_thread_funneled_example

all: $(TARGET)

$(TARGET): mpi_thread_funneled_example.o
	$(CC) $(LDFLAGS) $^ -o $@

mpi_thread_funneled_example.o: mpi_thread_funneled_example.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGET) *.o
