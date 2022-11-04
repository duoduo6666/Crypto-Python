nasm -f elf64 -o /home/duoduo/Crypto/out.o /home/duoduo/Crypto/src/C-NASM/MMX.asm
if [ $? == 0 ]
then
    gcc -o /home/duoduo/Crypto/out /home/duoduo/Crypto/src/C-NASM/MMX.c /home/duoduo/Crypto/out.o
    if [ $? == 0 ]
    then
        /home/duoduo/Crypto/out
        rm /home/duoduo/Crypto/out
    rm /home/duoduo/Crypto/out.o
    fi
fi
