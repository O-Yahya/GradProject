#include <stdio.h>
#include "network.h"

void read_from_socket(char* buffer) {
    // Simulated socket read operation
    scanf("%s", buffer); // Unchecked return value of scanf
}
