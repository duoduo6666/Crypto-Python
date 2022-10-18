#include <mmintrin.h>
#include <stdio.h>

int main()
{
    __int64_t a = 0x81818181;
    __int64_t b = 0x80808080;

    __m64 am = _mm_cvtsi64_m64(a);
    __m64 bm = _mm_cvtsi64_m64(b);

    __m64 ym = _mm_adds_pi8(am, bm);

    __int64_t y = _mm_cvtm64_si64(ym);
    printf("0x%lx\n",y);

    
    return 0;
}