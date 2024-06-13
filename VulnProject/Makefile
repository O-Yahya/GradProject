CC = gcc
CFLAGS = -g -Wall
LDFLAGS =

SRCS = main.c utils.c file_operations.c
OBJS = $(SRCS:.c=.o)
EXEC = VulnProject

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(LDFAGS) -o $(EXEC) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(EXEC) $(OBJS)
