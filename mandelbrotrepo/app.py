"""
Demonstration of how to return an image generated with numpy and a plot
generated with matplotlib using the Flask web server.
Requirements: numpy, flask, scikit-image, matplotlib.
"""

from io import BytesIO
from flask import Flask, send_file, jsonify
import numpy as np
from skimage.io import imsave
import matplotlib.pyplot as plt
import random
import json

app = Flask(__name__)
app.debug = True

URL = 'https://almond-bread.herokuapp.com'

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
    strIO = BytesIO()
    plt.savefig(strIO, dpi=300, bbox_inches='tight')
    strIO.seek(0)
    plt.close()
    return strIO





@app.route('/image/<randomNumber>', methods=['GET'])
def generate_image(randomNumber):
    """
    Return a generated image as a png by
    saving it into a StringIO and using send_file.
    """
    # ang = random.random() * 2 * np.pi
    maxNo = (2**10 - 1)
    ang = (float(int(randomNumber) % maxNo) / maxNo)  * 2 * np.pi
    strIO = mandelbrot(1000,1000,150, ang)
    
    return send_file(strIO, mimetype='image/png')

@app.route('/metadata/<id>/<randomNumber>', methods=['GET'])
def generate_medata(id, randomNumber):
    """
    Return some metadata.
    """
    metadata = {
      "description" : "Almond Bread", 
      # external_url: "https://openseacreatures.io/3", 
      "image" : "{}/image/{}".format(URL, randomNumber), 
      "name" : "Cool Fractal {}".format(id),
    }
   
    return jsonify(metadata)

@app.route('/', methods=['GET'])
def hello():
    """
    Return hello.
    """
    return "Hello World"



if __name__ == '__main__':
    app.run()