def ratioCalc(a1, a2, a3):
    return (a2-a1)/(a3-a2)

bf1 = 0.473
bf2 = 0.837
bf3 = 0.921
bf4 = 0.942
bf5 = 0.948

print(ratioCalc(bf1,bf2,bf3))
print(ratioCalc(bf2,bf3,bf4))
print(ratioCalc(bf3,bf4,bf5))