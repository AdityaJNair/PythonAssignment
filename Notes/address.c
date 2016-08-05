#include <stdio.h>
#include <stdlib.h>

#define ADDRESS	0x7fff5e78f800

int main(void) {
	long number = 1234;
	long *pointer = &number;

	printf("number is %ld\n", number);
	printf("The value at %p is %ld.\n", pointer, *pointer);
	*pointer = 42;
	printf("number is %ld\n", number);

	// And I can do the same thing with any address
    // it could cause a segmentation error
	// since MacOS now uses ASLR
	pointer = (long *)ADDRESS;
    // pointer--;
	printf("The value at %p is %lx.\n", pointer, *pointer);
	return EXIT_SUCCESS;
}
