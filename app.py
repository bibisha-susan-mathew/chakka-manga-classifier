from flask import Flask, render_template, Request
from keras.models import load_model
import os,shutil
from keras.preprocessing import image
import numpy as np
from werkzeug.utils import secure_filename

model = load_model('model.h5')

app=Flask(__name__)

@app.route('/')
def index():
      return render_template("index.html",data="hey")


@app.route("/prediction", methods=["POST"])
def prediction():

  f= request.files['img']

  folder = r'uploads'
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
       shutil.rmtree(file_path)



  
  basepath = os.path.dirname(__file__)
  file_path = os.path.join(
      basepath, 'uploads', secure_filename(f.filename))
  f.save(file_path)
  img = image.load_img(file_path,target_size=(224,224)) ##loading the image
  img = np.asarray(img) ##converting to an array
  img = img / 255 ##scaling by doing a division of 255
  img = np.expand_dims(img, axis=0) ##expanding the dimensions
  output = model.predict(img)
  if output[0][0] > output[0][1]:
          result = "manga"
  else:
           result = "chakka"

  return render_template("prediction.html",prediction=result)



if __name__=="__main__":
      app.run(debug=True)
