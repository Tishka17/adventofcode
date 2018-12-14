with open('/sdcard/src/in12.txt') as f:
    init=f.readline().strip().split(': ')[1]
    mapping = [
        x.strip().split(' => ') for x in f if x
    ]
print(init)
for m in mapping:
    print(m)
print()

def pot(state):
    for m in mapping:
        if m[0]==state:
            return m[1]
    return '.'


state='.'*20+init+'.'*25
print(' 0', state)
for k in range(20):
    state='..' + ''.join(
        pot(state[i-2:i+3]) for i in range(2, len(state)-2)
    ) + '..'
    print('%2s'%(k+1), state)
    

half=20
print('len', len(state), 'center', half, 'init', len(init))
def n(i):
    print(i, i-half)
    return i-half
    
s = sum(
    n(i) for i in range(len(state)) if state[i]=='#'
)

print(s)
