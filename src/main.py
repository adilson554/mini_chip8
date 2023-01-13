'''
3XNN ok		00EE ok	8XY5 ok
4XNN ok		8XY0 ok	8XYE no
5XY0 ok 	8XY1 ok	8XY6 ok
7XNN ok		8XY2 ok	FX55 ok
9XY0 ok 	8XY3 ok	FX33 ok
2NNN ok		8XY4 ok	1NNN ok

'''
import random                # usado na instrução Cxkk
from time import sleep
import os

##############################################################################
################### Variáveis ################################################

# 16 8-bit Registradores     # V[0] * 16 
# 4KB (4096 )  memória       # ram[0] * 4096
# 16-bit Index Register      # I = 0
# 16-bit Program Counter     # pc = 0x200, pois a rom é gravada a partir de 0x200
# 16 16-bit Stack            # stack[0] * 16
# 8-bit Stack Pointer        # sp = 0
# 8-bit Delay Timer          # dt = 0
# 8-bit Sound Timer          # st = 0  
# 16 8-bit Keypad            # key[0] * 16, verificar como implementar
# vram array[64*32]          # implementar futuramente com array[256]
# 16-bit opcode              # ? uma função que retorna o opcode dado o pc?
# 1-bit Draw-Flag            # Atualizar a tela apenas quando houver mudança

V = [0] * 16
ram = [0] * 0xFFF
I = 0
pc = 0x200
stack = [0] * 16
sp = 0
dt = 0
st = 0
key = [0] * 16
vram = [0] * 64 * 32
draw_flag = True

################### End Variáveis ############################################
##############################################################################

fontset = [
0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
0x20, 0x60, 0x20, 0x20, 0x70, # 1
0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
0x90, 0x90, 0xF0, 0x10, 0x10, # 4
0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
0xF0, 0x10, 0x20, 0x40, 0x40, # 7
0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
0xF0, 0x90, 0xF0, 0x90, 0x90, # A
0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
0xF0, 0x80, 0x80, 0x80, 0xF0, # C
0xE0, 0x90, 0x90, 0x90, 0xE0, # D
0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]


for i in range(len(fontset)):
    ram[0x50-0x50 + i] = fontset[i]




###################
# teste
ram[0x1ff] = 2 # valor de 1 a 5
ram[0x1fe] = 0

'''
ANNN
Fx65
4XNN
1NNN

'''









##############################################################################
################### Função carregar a rom ####################################
def carregar_rom(memoria):
    with open("../roms/chip8-test-suite.ch8", 'rb') as f:
        rom_byte = f.read()
        for i in range(len(rom_byte)):
            memoria[0x200 + i] = rom_byte[i]
        return memoria
##############################################################################
##############################################################################


def opcode():
    global pc
    global ram
    return (ram[pc]<<8 | ram[pc + 1]) 
    
##############################################################################

def decode(opcode):
    global pc
    global vram
    global I
    global V
    global ram
    global sp
    global stack
    global st
    global dt
    
    # --------------------------------------------------------------
    # 0x00E0
    if opcode == 0x00E0:
        print("limpar")
        vram = [0] * 64 * 32
        pc = pc + 2
        
    # --------------------------------------------------------------    
    # 00EE - RET
    elif opcode == 0x00EE:
        print('00EE - RET')
        pc = stack.pop()
        sp = sp - 1
        print(f'------------------------------sp:{sp} e {stack}')
        pc = pc + 2
        #TODO estudar e revisar esta instração.
            
    # --------------------------------------------------------------    
    # 1NNN
    elif opcode & 0xF000 == 0x1000:
        pc = (opcode & 0x0FFF)
        
    # --------------------------------------------------------------    
    # 2nnn - CALL addr
    elif (opcode & 0xf000) == 0x2000:
        sp = sp + 1
        stack.append(pc)
        pc = (opcode & 0x0fff)
    
    # --------------------------------------------------------------    
    # 3xkk - SE Vx, byte
    elif (opcode & 0xf000) == 0x3000:
        print('3xkk - SE Vx, byte')
        x = ((opcode & 0x0f00)>>8)
        kk = (opcode & 0x00ff)
        if V[x] == kk:
            pc = pc+2
        pc = pc + 2
    #TODO verificar se precisa incrementar o pc
    
    # --------------------------------------------------------------
    # 4XNN
    elif (opcode & 0xF000 == 0x4000):
        x = ((opcode & 0x0F00) >> 8)
        nn = opcode & 0x00FF
        if V[x] != nn:
            pc = pc + 2
        pc = pc + 2
    
    # --------------------------------------------------------------
    # 5xy0 - SE Vx, Vy
    elif (opcode & 0xf000) == 0x5000:
        print('5xy0 - SE Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = (opcode & 0x00f0)>>4
        if V[x] == V[y]:
            pc = pc + 2
        pc = pc + 2
    #TODO verificar se precisa incrementar o pc
    #TODO verificar se pode ser qualquer valor além do 0 na istrução 5xy0.
    
    # --------------------------------------------------------------   
    # 6XNN (set register VX)
    elif opcode & 0xF000 == 0x6000:
        #print(f'{pc:04X}: {opcode(pc):04X} - 6XNN (set register VX)')
        x = (opcode & 0x0F00) >> 8
        kk = opcode & 0x00ff
        V[x] = kk
        pc += 2
    
    # --------------------------------------------------------------
    # 7XNN (add value to register VX)
    elif opcode & 0xF000 == 0x7000:
        x = (opcode & 0x0F00) >> 8
        kk = opcode & 0x00ff
        V[x] = (V[x] + kk) & 0xff
        #print(f'{pc:04X}: {opcode(pc):04X} - 7XNN (add value to register VX): {V}')
        pc = pc + 2
    
    # --------------------------------------------------------------
    # 8xy0 - LD Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 0:
        print('8xy0 - LD Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        V[x] = V[y]
        pc = pc + 2
            
    # --------------------------------------------------------------
    # 8xy1 - OR Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 1:
        print('8xy1 - OR Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        V[x] = (V[x] | V[y])
        pc = pc + 2
    
    # --------------------------------------------------------------
    # 8xy2 - AND Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 2:
        print('8xy2 - AND Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        V[x] = V[x] & V[y]
        pc = pc + 2 
    
    # --------------------------------------------------------------
    # 8xy3 - XOR Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 3:
        print('8xy3 - XOR Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        V[x] = V[x] ^ V[y]
        pc = pc + 2
    
    # --------------------------------------------------------------
    # 8xy4 - ADD Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 4:
        print('8xy4 - ADD Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        soma = V[x] + V[y]
        if soma > 0xff:
            V[0xf] = 1
        else:
            V[0xf] = 0
        V[x] = soma & 0xff
        pc = pc + 2 
    
    # --------------------------------------------------------------
    # 8xy5 - SUB Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 5:
        print('8xy5 - SUB Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        if V[x] > V[y]:
            V[0xf] = 1
        else:
            V[0xf] = 0
        subtracao = V[x] - V[y]
        V[x] = subtracao & 0xff # pois o resultado pode ser negativo
        pc = pc + 2
            
    # --------------------------------------------------------------
    # 8xy6 - SHR Vx {, Vy}
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 6:
        print('8xy6 - SHR Vx {, Vy}')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        #V[0xf] = V[x] & 0x1 # V[0xf] recebe o ultimo bit de V[x]
        #V[x] = (V[x] >> 1)
        V[0xf] = (V[x] & 0x1)
        V[x] = (V[x] >> 1) & 0xff
        pc = pc + 2
        #TODO Estudar, pois há contradições em várias fontes
        
    # --------------------------------------------------------------    
    # 8xy7 - SUBN Vx, Vy
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 7:
        print('8xy7 - SUBN Vx, Vy')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        if V[y] > V[x]:
            V[0xf] = 1
        else:
            V[0xf] = 0
        V[x] = (V[y] - V[x]) & 0xff
        pc = pc + 2
            
    # --------------------------------------------------------------        
    # 8xyE - SHL Vx {, Vy}
    elif ((opcode & 0xf000) == 0x8000) and  ((opcode & 0x000f)) == 0x000E:
        print('8xyE - SHL Vx {, Vy}')
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        V[0xf] = ((V[x]) >> 7)
        V[x] = ((V[x] << 1) & 0xff)
        pc = pc + 2
        #TODO estudar pois há divergencias
    
    # --------------------------------------------------------------    
    # 9xy0 - SNE Vx, Vy
    elif ((opcode & 0xf000) == 0x9000):
        x = ((opcode & 0x0f00)>>8)
        y = ((opcode & 0x00f0)>>4)
        if V[x] != V[y]:
            pc = pc + 2
        pc = pc + 2
    
    # --------------------------------------------------------------       
    # ANNN
    elif opcode & 0xF000 == 0xA000:
        I = opcode & 0x0FFF
        pc = pc + 2
    
    # --------------------------------------------------------------
    # BNNN
    elif opcode & 0xF000 == 0xB000:
        nnn = opcode & 0x0FFF
        pc = V[0] + nnn
    
    # --------------------------------------------------------------    
    # Cxkk - RND Vx, byte
    elif ((opcode & 0xf000) == 0xC000):
        print('Cxkk - RND Vx, byte')
        x = ((opcode & 0x0f00)>>8)
        kk = (opcode & 0x00ff)
        V[x] = (random.randint(0,255) & kk)
        pc = pc + 2
    
    # --------------------------------------------------------------  
    # Fx07
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0015)):
        x = (opcode & 0x0F00) >> 8
        V[x] = dt
        pc = pc + 2 
     
    # --------------------------------------------------------------
    # Fx15
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0015)):
        x = (opcode & 0x0F00) >> 8
        dt = V[x]
        pc = pc + 2 
    
    # -------------------------------------------------------------- 
    # Fx18
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0018)):
        x = (opcode & 0x0F00) >> 8
        st = V[x]
        pc = pc + 2   
    
    # -------------------------------------------------------------- 
    # Fx1E
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x001E)):
        x = (opcode & 0x0F00) >> 8
        I = I + V[x]
        pc = pc + 2   
    
    # --------------------------------------------------------------
    # Fx33
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0033)):
        x = (opcode & 0x0F00) >> 8
        c = V[x] // 100
        d = (V[x] % 100) // 10
        u = (V[x] % 10)
        ram[I] = c
        ram[I + 1] = d
        ram[I + 2] = u
        pc = pc + 2
    
    # --------------------------------------------------------------
    # Fx55
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0055)):
        x = (opcode & 0x0F00) >> 8
        for i in range(x+1):
            ram[I+i] = V[i]
        pc = pc + 2
    
    # --------------------------------------------------------------
    # Fx65
    elif (opcode & 0xF000 == 0xF000) and ((opcode & 0x00FF == 0x0065)):
        x = (opcode & 0x0F00) >> 8
        for i in range(x+1):
            V[i] = ram[I+i]
        pc = pc + 2

    # --------------------------------------------------------------
    # DXYN (display/draw)
    elif(opcode & 0xF000 == 0xD000):
        x = V[(opcode & 0x0F00) >> 8]
        y = V[(opcode & 0x00F0) >> 4]
        height = opcode & 0x000F
        V[0xF] = 0
        for yline in range(height):
            pixel = ram[I + yline]
            for xline in range(8):
                if (pixel & (0x80 >> xline)) != 0:
                    if (vram[(x + xline + ((y + yline) * 64))] == 1):
                        V[0xf] = 1
                    vram[x + xline + ((y + yline) * 64)] ^= 1
        draw_flag = True
        pc += 2
    # --------------------------------------------------------------
    else:
        print(f"não encontrado -- {hex(opcode)}")
        pc = pc + 2



####################################################################
################### Screen #########################################

def font(k):
    if k == 1:
        return u"\u2588"+u"\u2588"
    elif k == 0:
        return u"\u2591"+u"\u2591"


def draw_screen(vector, flag, font=font):
    if flag:
        flag_flush = False
        os.system('clear')
        
        print()
        for i in range(len(vector)):
            if i == 0:
                print(font(vector[i]), end='', flush=flag_flush)
            elif i % 64 == 0:
                print()
                print(font(vector[i]), end='', flush=flag_flush)
            else:
                print(font(vector[i]), end='', flush=flag_flush)
        print()
        #flag = False
        return flag
################### End Screen #####################################
####################################################################




if __name__ == '__main__':
    carregar_rom(ram)
    # Vamos usar o teste 1 
    # para isso será necessário implementar estas instruções
    '''
    00E0 - Clear the screen
    6XNN - Load normal register with immediate value
    ANNN - Load index register with immediate value
    DXYN - Draw sprite to screen (only aligned)
    '''
    k = 0
    while k < 2400: # 240
        sleep(0.0016)
        draw_screen(vram, draw_flag)
        decode(opcode())
        print(hex(ram[pc]), hex(pc))
        print(ram[0x1ff])
        print(k)
        k = k + 1
        if dt > 0:
            dt = dt -1
        if st > 0:
            st = st - 1
            

   
        
