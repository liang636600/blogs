1. 文件->项目->空项目

   ![image-20221111193212301](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20221111193212301.png)

2. 生成依赖项->生成自定义->勾选masm

   ![image-20221111193425375](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20221111193425375.png)

3. 添加汇编源程序文件

   右键项目->添加->新建项->'test(名称).asm'

   编辑文件,功能完成1+2+...+100的和并打印结果

   ```ASM
   .686P
   .model flat,c
    ExitProcess    proto stdcall :dword
    includelib      kernel32.lib
    printf            proto c :vararg
    includelib      libcmt.lib
    includelib      legacy_stdio_definitions.lib
    .data
     lpFmt db "%d", 0ah, 0dh, 0
     .stack 200
     .code
      main proc
      mov eax, 0
      mov ebx, 1
   lp:cmp ebx,100
       jg exit
   	add eax,ebx
   	inc ebx
   	jmp lp
   exit:
       invoke printf,offset lpFmt, eax
   	invoke ExitProcess, 0
   main endp
   end
   ```

   ```asm
   注释
   .686P
   .model flat,c
    ExitProcess    proto stdcall :dword
    includelib      kernel32.lib
    printf            proto c :vararg（下面两个includelib表示printf要使用的库）
    includelib      libcmt.lib
    includelib      legacy_stdio_definitions.lib
    .data
     lpFmt db "%d", 0ah, 0dh, 0 （定义了全局变量lpFmt，初始值是等同于c语言"%d\nk"）
     .stack 200（200表示堆栈段大小是200字节）
     .code（代码段定义伪指令）
      main proc
      mov eax, 0
      mov ebx, 1
   lp:cmp ebx,100
       jg exit
   	add eax,ebx
   	inc ebx
   	jmp lp
   exit:
       invoke printf,offset lpFmt, eax
   	invoke ExitProcess, 0
       main endp
   end（表示整个程序结束）
   ```

   例2输入5个有符号数到数组缓冲区中，然后求最大值并显示该最大值

   ```asm
   .686P
   .model flat,c
    ExitProcess    proto stdcall :dword
    includelib      kernel32.lib
    printf            proto c :ptr sbyte, :vararg
    scanf            proto c :ptr sbyte, :vararg
    includelib      libcmt.lib
    includelib      legacy_stdio_definitions.lib
    .data
     lpFmt db "%d", 0ah, 0dh, 0
     buf db "%d",0
     x   dd 5 dup(0)   ;int x[5];
     .stack 200
     .code
      main proc
       ;表示注释 输入五个数 ebx=0;
      ; do {scanf("%d",&x[ebx*4]); ebx++;} while (ebx!=5)
        mov ebx,0
        mov ebx,0
      input_5num:
        invoke scanf, offset buf, addr [x+ebx*4]
   	 inc ebx
   	 cmp ebx,5
   	 jne  input_5num
   	 ;求这五个数的最大数，先将第一个数作为最大数，放在eax中
   	 ; eax=x[0]
   	 ; for (ebx=1;ebx<=4;ebx++) if (eax <x[ebx*4]) eax = x[ebx*4]
   	 mov eax, x[0]
   	 mov ebx,1
   	 lp:cmp ebx,4
   	     jg exit
   	    cmp eax, x[ebx*4]
   	    jge next
   		mov eax,x[ebx*4]
   	  next:
   	    add ebx,1
   	    jmp    lp
      exit:
        invoke printf,offset lpFmt, eax
   	 invoke ExitProcess, 0
    main endp
   end
   ```

4. 右键项目->生成->运行

   ![image-20221111194733165](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20221111194733165.png)

---

# C/C++编译器配置

1. 生成汇编语言程序

   输出文件->汇编程序输出->带源代码的程序集

   ![image-20221111201002000](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20221111201002000.png)

2. 变量的空间分配（解决变量之间有间隙）

   代码生成->基本运行时检查中设为默认值

3. 结构成员对齐

   默认情况下，结构变量中各字段的起始地址是采用自然边界对齐的方式，即各字段在结构中的偏移量为类型长度的整数倍。若要采用紧凑模式，代码生成->结构成员对齐->设置为1字节