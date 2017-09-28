#include <stdio.h>
#define N 256

int main(int argc, char* argv[]) {
    int i=0;

    // Print the entire ASCII table
    for(i=0; i<N; i++){
        char c = i;
        printf("%c\n",c);
    }

    return 0;
}
