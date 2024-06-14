#include <stdio.h>
#include <stdlib.h>
#include "utility.h"

void use_after_free() {
    int* ptr = (int*)malloc(sizeof(int));
    free(ptr);
    *ptr = 10; // Use after free vulnerability
}
