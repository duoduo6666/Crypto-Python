#include <stdio.h>
#include <limits.h>

char SHA1_Computation(char M[64],unsigned int H[5]){
    
    return 0;
}
char* SHA1(char M[],unsigned int e){
    unsigned int a = (e+9)/64;
    if ((e+9)%64 > 0){
        a++;}
    unsigned char byte[a*64];
    for (int i = 0; i < e; i++){
        byte[i] = M[i];
    }
    printf("\n");
    return M;
}

int main()
{
    char data[] = "abc";
    unsigned int len = 63;
    printf("%s\n",SHA1(data,5));

    int src = 2;
    int dst;   

    asm (
        "mov %2, %0\n\t"
        "add $1, %0\n\t"
        "add $1, %0\n\t"
        : "=r" (dst) 
        : "r" (src), "r" (len)
        );

    printf("%d\n", dst);
    // printf("supports: %u\n",__builtin_cpu_supports("sse4.2"));
    // printf("is: %u\n",__builtin_cpu_is("core2"));
    // SHA1_Computation(data,len);
    return 0;
}