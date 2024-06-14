#include <stdio.h>
#include "utils.h"
#include "file_operations.h"

int main() {

    char buffer1[10];
    get_input(buffer1); // Buffer overflow vulnerability

    char *ptr = NULL;
    if (is_valid(ptr)) { // Null pointer dereference vulnerability
        printf("This is never reached\n");
    }

    read_file("test.txt"); // Resource leak vulnerability
    // Example usage for memory-related vulnerabilities
    char* data = NULL;
    int length = get_string_length(data);
    printf("Null Pointer Dereference Length: %d\n", length);

    int user_input = 15;
    buffer_overflow(user_input);

    int* ptr2 = allocate_memory();
    if (ptr2) {
        *ptr2= 10;
        free(ptr2); // Double free vulnerability
        free(ptr2); // Double free vulnerability
    }

    // Example usage for file handling vulnerabilities
    //char* file_data = read_file("example.txt");
    //if (file_data) {
    //   printf("File Content: %s\n", file_data);
    //    free(file_data); // Free allocated memory to prevent leaks
    //}

    // Example usage for network vulnerabilities
    char buffer[100];
    read_from_socket(buffer); // Unchecked return value

    return 0;
}