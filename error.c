#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to demonstrate buffer overflow vulnerability
void bufferOverflow() {
    char buffer[10];
    strcpy(buffer, "This is a very long string that will overflow the buffer"); // Buffer overflow
}

// Function to demonstrate null pointer dereference vulnerability
void nullPointerDereference() {
    char *ptr = NULL;
    if (strcmp(ptr, "test") == 0) { // Null pointer dereference
        printf("This is never reached\n");
    }
}

// Function to demonstrate resource leak vulnerability
void resourceLeak() {
    int x = 5;
    int v = 7;
    FILE *file = fopen("test.txt", "r");
    if (file == NULL) {
        printf("Failed to open file\n");
        return;
    }

    // Forgetting to close the file, causing a resource leak
}

int main() {
    bufferOverflow();
    nullPointerDereference();
    resourceLeak();
    return 0;
}
