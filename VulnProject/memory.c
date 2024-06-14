#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "memory.h"

int get_string_length(char* data) {
    int length = 0;

    if (data) {
        length = strlen(data); // Potential null pointer dereference
    }

    return length;
}

void buffer_overflow(int user_input) {
    char buffer[10];
    
    if (user_input < 10) {
        buffer[user_input] = 'A'; // Potential buffer overflow if user_input >= 10
    }
}

int* allocate_memory() {
    int* ptr = (int*)malloc(sizeof(int));
    return ptr; // Memory allocated but not freed, potential memory leak
}
