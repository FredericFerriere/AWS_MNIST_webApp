import numpy as np
import re
import base64
import tensorflow as tf
from PIL import Image
from keras.models import load_model
from keras.backend import set_session
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
sess = tf.Session()
graph = tf.compat.v1.get_default_graph()

set_session(sess)
model = load_model('./cnn-mnist')


@app.route('/')
def index():
    return render_template('index.html')

def convertImage(imgData1):
    imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))

def loadImage(fileName):
    img_rows = img_cols = 28

    img = Image.open(fileName).convert('L')
    img = img.resize((img_rows, img_cols))

    aimg = np.array(img)
    aimg = centerImageArray(aimg)
    aimg = aimg/255
    aimg = np.expand_dims(aimg, axis=0)
    aimg = np.expand_dims(aimg, axis=0)
    aimg = np.reshape(aimg, (1, img_rows, img_cols, 1))

    return np.array(aimg)

def centerImageArray(arrimg):
    fner = lner = fnec = lnec = 0
    while np.argmax(arrimg[fner, :]) == 0:
        fner += 1
    lner = fner
    while np.argmax(arrimg[lner:, :]) > 0:
        lner += 1

    while np.argmax(arrimg[:, fnec]) == 0:
        fnec += 1
    lnec = fnec
    while np.argmax(arrimg[:, lnec:]) > 0:
        lnec += 1

    width = lnec - fnec
    height = lner - fner
    side = int(max(width,height)/0.7)
    leftshift = int(0.5*(side-width))
    topshift = int(0.5*(side-height))
    newarr = np.zeros((side, side))
    for i in range(height):
        for j in range(width):
            newarr[i+topshift, j+leftshift] = arrimg[i+fner, j+fnec]

    pimg = Image.fromarray(np.uint8(newarr), 'L')
    pimg = pimg.resize((28, 28))

    return np.array(pimg)

def saveProcessedImage(arrImg):
    img_rows = img_cols = 28
    aimg = np.ndarray((img_rows, img_cols))
    for i in range(img_rows):
        for j in range(img_cols):
            aimg[i, j] = int(255 * (arrImg[0, i, j, 0]))
    pimg = Image.fromarray(np.uint8(aimg), 'L')
    pimg.save('processedImage.png', 'PNG')

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    imgdata = request.get_data()
    convertImage(imgdata)
    img = loadImage('output.png')
    with graph.as_default():
        set_session(sess)
        classes = model.predict(img)
        predicted = np.argmax(classes)
        response = jsonify(str(predicted))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000)