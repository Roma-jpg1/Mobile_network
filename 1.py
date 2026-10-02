from math import *
import math
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import cmath


def dft(x):
    N = len(x)
    X = []

    for k in range(N):
        value = 0j
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            value += x[n] * cmath.exp(1j * angle)
        X.append(value)

    return X

def q(x, bits):
    A = 12
    levels = 2 ** bits

    result = []

    for value in x:
        code = round((value + A) / (2 * A) * (levels - 1))
        value_q = code / (levels - 1) * 2 * A - A
        result.append(value_q)

    return result


f=14
fs = 2*f
duration = 1
N = fs * duration

ts = np.arange(N) / fs

 
y = [12*cos(2 * np.pi * x * f + np.pi/6) for x in ts]
print(y)
plt.subplot(2, 1, 1)
plt.plot(ts, y)



X=dft(y)
N=len(X)
freq = []
amplitude = []

for k in range(N // 2 + 1):
    freq.append(k * fs / N)

    a = abs(X[k]) / N
    if k != 0 and k != N // 2:
        a *= 2
    amplitude.append(a)

for bits in range(3, 7):
    y_q = q(y, bits)
    X_q = dft(y_q)

    amplitude_q = []
    for k in range(N // 2 + 1):
        a = abs(X_q[k]) / N
        if k != 0 and k != N // 2:
            a *= 2
        amplitude_q.append(a)

    plt.subplot(2, 1, 2)
    plt.plot(freq, amplitude_q, label=f'Quantized with {bits} bits')

    err =0
    for i in range(N):
        err += abs(y[i] - y_q[i])

    err /= N
    print(f'Average error for {bits} bits: {err}')

plt.subplot(2, 1, 2)
plt.plot(freq, amplitude)

plt.show()
