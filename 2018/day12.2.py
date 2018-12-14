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


state='.'*20+init+'.'*240
half=20

def n(i):
    return i-half

def s():
    return sum(
    n(i) for i in range(len(state)) if state[i]=='#'
)


print(' 0', state)
for k in range(230):
    state='..' + ''.join(
        pot(state[i-2:i+3]) for i in range(2, len(state)-2)
    ) + '..'
    print('%2s'%(k+1), state[-200:])
    print(len(state.strip('.')), state.index('#')-20, s())
    

print('len', len(state), 'center', half, 'init', len(init))


print(s())
