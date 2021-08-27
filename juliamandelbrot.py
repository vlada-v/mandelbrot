import numpy as np
import matplotlib.pyplot as plt
import random

def mandelbrot(n_rows, n_columns, iterations, angle, k = 0.7885, cnt=0):
    cx = k*np.cos(angle)
    cy = k*np.sin(angle)
    x_cor = np.linspace(-2, 2, n_rows)
    y_cor = np.linspace(-2, 2, n_columns)
    x_len = len(x_cor)
    y_len = len(y_cor)
    output = np.zeros((x_len,y_len))
    c = complex(cx, cy)
    for i in range(x_len):
        for j in range(y_len):
            z = complex(x_cor[i], y_cor[j])
            count = 0
            for k in range(iterations):
                z = (z * z) + c
                count = count + 1
                if (abs(z) > 4):
                    break
            output[i,j] = count

    plt.imshow(output.T, cmap='hot')
    plt.axis("off")
    plt.savefig('fract{}.png'.format(cnt), dpi=300, bbox_inches='tight')
    plt.show()

for i in range(5):
    ang = random.random()*2*np.pi
    mandelbrot(1000,1000,150, ang)
