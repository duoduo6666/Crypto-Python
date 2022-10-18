#include <stdio.h>
#include <limits.h>

char* SHA1(char data[],unsigned int len){
    static unsigned char str[20];
    unsigned int a = (len+9)/64;
    if ((len+9)%64 > 0){
        a++;}
    unsigned char byte[a*64];
    for (int i = 0; i < len; i++){
        byte[i] = data[i];
    }
    printf("%u\n",a);
    printf("%s",byte);
    return data;
}

int main()
{
    char data[] = "abc";
    unsigned int len = 3;
    printf("%s\n",SHA1(data,5));
 
    return 0;
}