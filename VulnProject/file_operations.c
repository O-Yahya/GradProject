#include <stdio.h>
#include "file_operations.h"

void read_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Failed to open file\n");
        return;
    }
    // Vulnerability: forgetting to close the file, causing a resource leak
    // fclose(file); // Uncommenting this would fix the resource leak
}
