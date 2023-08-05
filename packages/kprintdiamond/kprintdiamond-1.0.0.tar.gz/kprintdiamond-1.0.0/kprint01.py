for i in range(1,14,2):
    if i<8:
        print(int((7-i)/2)*" "+i*"*")
    else:
        print(int((i-7)/2)*" "+(14-i)*"*")