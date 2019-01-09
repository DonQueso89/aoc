#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    // Read file into buffer
    FILE *fp = fopen("input1", "r");
    if(!fp) {
        perror("File opening failed");
        return 1;
    }
    fseek(fp, 0L, SEEK_END);
    char buffer[ftell(fp) * sizeof(char)];
    rewind(fp);
    char c;
    int i = 0;
    while ((c = fgetc(fp)) != EOF) {
        *(buffer + i++) = c;
    }
    if(ferror(fp)) {
        puts("I/O error while reading file");
    } else if(feof(fp)) {
        puts("End of file reached successfully");
    }
    fclose(fp);

    // Output the data read
    printf("INPUT: \n");
    puts(buffer);
    printf("\n");
    
    // Iterate input keeping track of coordinates and direction
    int direction = 0; int x = 0; int y = 0;
    i = 0;
    int input_size = strlen(buffer);
    printf("hello world");
    while(i < input_size) {
        c = *(buffer + i++);
        // Next character is R
        if(c == 82) {
            direction = (direction + 1) % 4;
        } 
        // Next character is L
        if (c == 76) {
            direction = (direction - 1) % -4;
            if(direction < 0) {
                direction *= -1;
            }
        }
        // Next character is an integer
        if(48 <= c && c <= 57) {
            char *stepss = ""; 
            while(c != 44 && i++ < input_size) { // read until ,
                stepss = strcat(stepss, &c);
                c = *(buffer + i);
            }
            puts(stepss);
            int steps = atoi(stepss);
            if(direction == 0) { // N
                y += steps;
            } else if(direction == 1) { // E
                x += steps;
            } else if(direction == 2) { // S
                y -= steps;
            } else { // W
                x -= steps;
            }
        }
    }

    if(x < 0) {
        x *= -1;
    }
    if(y < 0) {
        y *= -1;
    }

    printf("P1: %i", x + y);


    return 0;
}
