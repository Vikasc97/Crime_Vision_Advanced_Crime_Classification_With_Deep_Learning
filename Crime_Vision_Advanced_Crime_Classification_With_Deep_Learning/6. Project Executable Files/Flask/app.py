import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'



from flask import Flask , request, render_template
#from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

app = Flask(__name__)
model = load_model("crime_vision_densenet.h5", compile=False)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def preprocess_image(img, target_size=(224, 224)):

  # Convert to NumPy array
  img = img_to_array(img)

  # Rescale (assuming your model expects normalized pixel values)
  img = img / 255.0  # Rescale to range [0, 1]

  # Resize if necessary
  if img.shape[0:2] != target_size:
    img = tf.image.resize(img, target_size)

  return img

@app.route('/predict',methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        
        # Ensure the folder 'uploads' exists in the current directory
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        filepath = os.path.join(uploads_dir, f.filename)
        f.save(filepath)
        
        img = load_img(filepath, target_size=(224, 224))
        preprocessed_img = preprocess_image(img)

        x = preprocessed_img
        x = np.expand_dims(x, axis=0)
        preds = model.predict(x)
        
        index = ['Abuse', 'Arrest', 'Arson', 'Assault', 'Burglary', 'Explosion', 'Fighting', 
                 'NormalVideos', 'RoadAccidents', 'Robbery', 'Shooting', 'Shoplifting', 'Stealing', 'Vandalism']
        
        predicted_class_index = np.argmax(preds)
        predicted_class = index[predicted_class_index]
        
        text = "The predicted crime is: " + predicted_class

        # Render predict.html with the prediction result
        return text

    # Render predict.html with empty text (if accessed via GET request)
    return render_template('predict.html', text="")
if __name__ == '__main__':
    app.run(debug = False, threaded = False)