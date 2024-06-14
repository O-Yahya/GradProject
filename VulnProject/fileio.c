#include <stdio.h>
#include <stdlib.h>
#include "fileio.h"

char* read_file(const char* file_name) {
    FILE* fp = fopen(file_name, "r");
    char* buffer = NULL;

    if (fp) {
        fseek(fp, 0, SEEK_END);
        long file_size = ftell(fp);
        fseek(fp, 0, SEEK_SET);

        buffer = (char*)malloc(file_size + 1);
        if (buffer) {
            fread(buffer, 1, file_size, fp);
            buffer[file_size] = '\0';
        }

        fclose(fp); // File is not closed, leading to potential resource leak
    }

    return buffer;
}
