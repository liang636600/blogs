# 1 使用

1. `gcc main.c` 默认生成的可执行文件a.out

2. `gcc main.c -o main`指定输出文件

3. `gcc -S main.c`只想输出汇编代码而非二进制代码

   `-masm=intel`

4. `gcc -g -O0 main.c -o main` -g表示为了让编译器生成额外的信息便于调试，-O0禁止所有编译器优化，产生main文件，运行main `./main`