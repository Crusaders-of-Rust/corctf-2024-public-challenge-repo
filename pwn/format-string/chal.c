#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void do_printf()
{
    char buf[4];

    if (scanf("%3s", buf) <= 0)
        exit(1);

    printf("Here: ");
    printf(buf);
}

void do_call()
{
    void (*ptr)(const char *);

    if (scanf("%p", &ptr) <= 0)
        exit(1);

    ptr("/bin/sh");
}

int main()
{
    int choice;

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    while (1)
    {
        puts("1. printf");
        puts("2. call");

        if (scanf("%d", &choice) <= 0)
            break;

        switch (choice)
        {
            case 1:
                do_printf();
                break;
            case 2:
                do_call();
                break;
            default:
                puts("Invalid choice!");
                exit(1);
        }
    }

    return 0;
}
