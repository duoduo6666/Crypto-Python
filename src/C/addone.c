#include <stdio.h>
#include <time.h>
#include <mmintrin.h>
void c(){
    unsigned long a = 0;
    for(unsigned char i0 = 0; i0 < 8; i0++){
        a <<= 8;
        for(unsigned char i1 = 0; i1 < 255; i1++){
        a++;}
        }
}
void MMX(){
    signed long a = 0;
    signed long add = 0x0101010101010101;
    __m64 am = _mm_cvtsi64_m64(a);
    __m64 addm = _mm_cvtsi64_m64(add);
    for(unsigned char i = 0; i < 255; i++){
        am = _mm_add_pi8(am,addm);}
    a = _mm_cvtm64_si64(am);
}
int main(){
    clock_t t = clock();
    for(unsigned int i = 0; i < 256; i++){c();}
    printf("C: %ldns\n",clock() - t);

    t = clock();
    for(unsigned int i = 0; i < 256; i++){MMX();}
    printf("MMX: %ldns\n",clock() - t);
    
    return 0;
}