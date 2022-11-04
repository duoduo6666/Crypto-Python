#include <mmintrin.h>
#include <stdio.h>
#include <time.h>

int main()
{
    __int64_t a = 0x030303030303030;
    __int64_t b = 0x0001020304050607;

    __m64 ammx = _mm_cvtsi64_m64(a);
    __m64 bmmx = _mm_cvtsi64_m64(b);
    
    __m64 ym = _mm_add_pi8(ammx, bmmx);

    __int64_t y = _mm_cvtm64_si64(ym);
    printf("0x%lx\n",y);

    
    return 0;
}