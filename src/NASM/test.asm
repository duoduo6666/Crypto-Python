section .text
global main
main:
    mov rax,0x3030303030303030
    mov rbx,0x0001020304050607
    movd mm0,rax
    movd mm1,rbx
    paddusb mm0,mm1
    movd rax,mm0
    mov [msg], rax
    mov eax,4 ;　　 4号调用
    mov ebx,1 ;　　 ebx送1表示输出
    mov ecx,msg ;　字符串的首地址送入ecx
    mov edx,10 ;　　字符串的长度送入edx
    int 80h ;　　　 输出字串
    mov eax,1 ;　　 1号调用
    int 80h ;　　　 结束　

section .data
msg: db "01234567",0ah,0dh