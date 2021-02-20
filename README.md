### Assembly Code Simulator.

    Our Simulator works similar to Mips .

        - It has 32 registers, and those are :-
          [ $s0 - $s7 , $t0 - $t9 , $a0 - $a3 , $v0 - $v1 , $g0 - $g5 , $z0(similar to $zero) ,  $ra ]
        - Memory of 4kb .
        - Size of the main memory is fixed and the value is 1024 bytes or 2**10 bytes.
        - It has 2 levels of cache.
        - It performs pipelining.
        - Both the levels of the cache has same Block size. But size and associativity of both the levels of the cache can be of user's wish.
        - Our simulator uses "Least recently used (LRU)" cache policy. And it is based on Exclusive cache.
        - It has some of the instructions used in Mips , and they are
            * la    #load address
            * li    #load index
            * sll   #shift left logic
            * lw    #load word
            * sw    #store word
            * lui   #load upper index
            * add   #add
            * addi  #add immediate
            * sub   #subtract
            * and   #and
            * bne   #branch on not equal
            * beq   #branch on equal
            * j     #jump
            * slt   #set on less than
            
            all the above instructions perform same action as in Qtspim.But the way they do things may be different from Qtspim. 

    Warnings :-

        - The address given has to be given in 32bit numbers and with base 16.
        - The address given should be a multiple of 4.
        - If there are any instructions other than those mentioned above, then those instructions might not be executed . So please check the code before simulating.
        - If the input given is more than 4kb then the simulator is not going to accept it .

    Team Members :-
        
        - Jawahar Sai Nathani.       CS18B023
        - Pavan Kumar Katikala.      CS18B015
        - Sala Raj Kumar.            CS18B030
