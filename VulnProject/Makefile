CC = gcc
CFLAGS = -Wall -Wextra
LDFLAGS =

SRCS = main.c memory.c fileio.c network.c utility.c utils.c error.c
OBJS = $(SRCS:.c=.o)
TARGET = vulnerable_project

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

