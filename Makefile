CC = g++
CFLAGS = -c -Wall
LDFLAGS = 
SRC = main.cpp tmp.cpp
OBJ = $(SRC:.cpp=.o)
EXE = fib

all: $(SRC) $(EXE)

$(EXE): $(OBJ)
	$(CC) $(LDFLAGS) $(OBJ) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	del -f $(OBJ) $(EXE)