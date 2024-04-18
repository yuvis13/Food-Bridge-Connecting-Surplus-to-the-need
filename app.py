# Flask app code
import os
import sys
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image, ImageFile
import my_tf_mod
from io import BytesIO
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about-us')
def Aboutus():
    return render_template('About-us.html')


@app.route('/Prediction', methods=['GET', 'POST'])
def pred():
    if request.method == 'POST':
        file = request.files['file']
        org_img, img = my_tf_mod.preprocess(file)

        print(img.shape)
        fruit_dict = my_tf_mod.classify_fruit(img)
        rotten = my_tf_mod.check_rotten(img)

        img_x = BytesIO()
        plt.imshow(org_img/255.0)
        plt.savefig(img_x, format='png')
        plt.close()
        img_x.seek(0)
        plot_url = base64.b64encode(img_x.getvalue()).decode('utf8')

        if rotten[0] > rotten[1]:  # If fresh
            return redirect(url_for('fresh'))
        else:  # If rotten
            return redirect(url_for('rotten'))

    return render_template('Pred3.html')


@app.route('/fresh')
def fresh():
    return render_template('fresh.html')


@app.route('/rotten')
def rotten():
    return render_template('rotten.html')


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

