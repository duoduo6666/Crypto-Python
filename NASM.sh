nasm -f elf64 -o /home/duoduo/Crypto/out.o /home/duoduo/Crypto/src/NASM/test.asm
if [ $? == 0 ]
then
    gcc -no-pie -o /home/duoduo/Crypto/out /home/duoduo/Crypto/out.o
    if [ $? == 0 ]
    then
        /home/duoduo/Crypto/out
        rm /home/duoduo/Crypto/out
    rm /home/duoduo/Crypto/out.o
    fi
fi
