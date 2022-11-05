#include <mmintrin.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <signal.h>

void sighandler(int);

extern void MMX_add();

int main()
{
    clock_t clock_sec, start, end;
    signal(SIGINT, sighandler);
    clock_sec = CLOCKS_PER_SEC;
    printf("%luclock\n",clock_sec);
    while (1)
    {
        start = clock();
        for(int a = 0; a < 2621440; a++ ){
            MMX_add();
            }
        end = clock();
        // printf("\r%ld/s",1/(end-start));
        printf("\r%lu/s",clock_sec/(end-start)*2621440);
    }
    

    // printf(
    //     "start: %lu\n"
    //     "end: %lu\n"
    //     "time: %lu\n"
    //     ,start,end,end-start);

    return 0;
}

void sighandler(int signum)
{
    printf("  \n捕获信号 %d, 跳出...\n", signum);
    exit(0);
}