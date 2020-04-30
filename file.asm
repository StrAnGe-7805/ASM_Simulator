.data
arr:
  .word 14, 15, 16, 16, 27, 5, 32, 45, 9, 8
arr1:
   .asciiz "Hi dude\nHow are you"
.text
.globl main
main:
la $s1,arr
addi $s2,$zero,9
loop1:
      beq $s6,$s2,exit
     sub $t4,$s2,$s6
    add $s3,$zero,$zero
loop2: sll $t1,$s3,2
       beq $s3,$t4, loo1
        add $t2,$s1,$t1
        lw  $t5,0($t2)
        lw $t6, 4($t2)
        slt $s4,   $t5,$t6
        beq  $s4,$zero,swap
  back: 
      addi $s3,$s3,1
        j loop2

loo1: addi $s6,$s6,1
     beq  $t8,$zero,loop1

swap: add $t5,$t5,$t6
     sub $t6,$t5,$t6
     sub $t5,$t5, $t6
    sw $t5, 0($t2)
      sw $t6,4($t2)
     j back
     jr $ra

exit:
jr $ra