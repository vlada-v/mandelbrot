# -*- coding: utf-8 -*-
# OKAYISH
"""
BARNSLEY FERN
By: it's literally monique
"""

# import libraries needed for program
import matplotlib.pyplot as plt 
from random import randint 
  
def generate_fractal(lim1, lim2, c1, c2, ):
    #initialize list & set first values to 1
    x = [0] 
    y = [0] 

    # create the barnsley fractal by creating the points on the scatterplot
    for i in range(0, 5000): 
    
        z = randint(1, 100) 
        
        if z == 1: 
            x.append(0) 
            y.append(0.16*(y[i])) 
            
        if z>= 2 and z<= 86: 
            x.append(0.3*(x[i]) + 0.9*(y[i])) 
            y.append(-0.9*(x[i]) + 0.2*(y[i])+1.6) 
        
        if z>= 87 and z<= 93: 
            x.append(0.2*(x[i]) - 0.26*(y[i])) 
            y.append(0.23*(x[i]) + 0.2*(y[i])+1.6) 
            
        if z>= 94 and z<= 100: 
            x.append(-0.15*(x[i]) + 0.28*(y[i])) 
            y.append(0.26*(x[i]) + 0.24*(y[i])+0.44)

    # make and show the scatterplot
    plt.scatter(x, y, s = 1, c = 'blue', marker = "d") 
    plt.axis("off")
    plt.savefig('barnsley_fern.png', dpi=300, bbox_inches='tight')
    plt.show()