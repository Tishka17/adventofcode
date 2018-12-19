def cal( r5):
    r0 = 18
    r2 = 19

    while r2 <= r5:
        if r5 % r2 ==0:
            r0 += r2
        r2 += 1
    print(r0)


cal(10551350)