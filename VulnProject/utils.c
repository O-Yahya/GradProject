#include <stdio.h>
#include <string.h>
#include "utils.h"

void get_input(char *buffer) {
    // Vulnerability: buffer overflow
    strcpy(buffer, "This is a very long string that will overflow the buffer");
}

int is_valid(char *ptr) {
    // Vulnerability: null pointer dereference
    return strcmp(ptr, "valid") == 0;
}
