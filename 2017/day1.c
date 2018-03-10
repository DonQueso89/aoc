#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* get_inp() {
    FILE* fp = fopen("inp1.txt", "r");
    fseek(fp, 0L, SEEK_END);
    int file_size = ftell(fp);
    fseek(fp, 0L, SEEK_SET);
    char c;
    char* buffer = malloc(file_size);
    int i = 0;
    while((c = fgetc(fp)) != EOF) {
        *(buffer + i) = c;
        i++;
    }
    buffer[i] = '\0';
    return buffer;
}

void p1(char* inp) {
    int i = 0;
    int sum = 0;
    int size = strlen(inp);
    while(i <= size) {
        if(inp[i] == inp[(i + 1) % size]) {
            sum += (inp[i] - '0');
        }
        i++;
    }
    printf("Part 1: %d\n", sum);
}

void p2(char* inp) {
    int i = 0;
    int sum = 0;
    int size = strlen(inp);
    int halfway = size / 2;
    while(i <= size) {
        if(inp[i] == inp[(i + halfway) % size]) {
            sum += (inp[i] - '0');
        }
        i++;
    }
    printf("Part 2: %d\n", sum);
}

int main(void) {
    char* inp = get_inp();
    p1(inp);
    p2(inp);
    return 0;
}
