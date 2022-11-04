section .text
global MMX_add
MMX_add:
    mov rax,0x3030303030303030
    mov rbx,0x0001020304050607
    movd mm0,rax
    movd mm1,rbx
    paddusb mm0,mm1
    movd rax,mm0