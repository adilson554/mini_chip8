import os

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
        flag = False
        return flag

