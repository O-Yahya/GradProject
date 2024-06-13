#include <stdio.h>
#include "utils.h"
#include "file_operations.h"

int main() {
    char buffer[10];
    get_input(buffer); // Buffer overflow vulnerability

    char *ptr = NULL;
    if (is_valid(ptr)) { // Null pointer dereference vulnerability
        printf("This is never reached\n");
    }

    read_file("test.txt"); // Resource leak vulnerability
    return 0;
}
