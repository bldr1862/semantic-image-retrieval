from flask import Flask, request, flash, redirect
from flask import render_template

import glob

import utils
import config

app = Flask(__name__)

MODEL_CONFIG = config.MODEL_CONFIG
image_model, text_model, stopwords = utils.load_model(MODEL_CONFIG)

# Create project structure
utils.create_dir_if_not_exists(config.UPLOAD_FOLDER)
utils.create_dir_if_not_exists(config.METADATA_DIR)
utils.init_metadata_if_not_exists()


# Update metadata
utils.update_descriptors(image_model, MODEL_CONFIG)


@app.route('/', methods=["GET"])
def index():
    return redirect("search/")


@app.route('/search/', methods=["GET", "POST"])
def search():
    """
    Ruta para buscar imagenes
    """
    if request.method == "GET":
        images = []
        for ext in config.ALLOWED_EXTENSIONS:
            images = images + glob.glob(config.UPLOAD_FOLDER+f"*{ext}")
        images = [img.split("/")[1] for img in images]
        images = [img.replace("\\", "/") for img in images]
        images = utils.chunks(images, config.GRID_SIZE)
        return render_template('search.html', images=images, cfg=MODEL_CONFIG)

    elif request.method == "POST":
        # Add search logic
        query = request.form['query']
        neighbors = utils.search(query, stopwords, text_model, MODEL_CONFIG)
        neighbors = [img.replace("static/","") for img in neighbors]
        neighbors = utils.chunks(neighbors, config.GRID_SIZE)
        return render_template('search.html', images=neighbors, query=query, cfg=MODEL_CONFIG)

@app.route("/upload-images/", methods=["GET", "POST"])
def upload_files():
    """
    Ruta para subir imagenes, esto toma tiempo ya que necesita indexar las imagenes nuevas
    """
    # Get the name of the uploaded files
    if request.method == "POST":
        files = request.files.getlist("file[]")
        utils.upload_files(files)
        # Update metadata
        utils.update_descriptors(image_model, MODEL_CONFIG)
    return render_template("upload-files.html", cfg=MODEL_CONFIG)

# @app.route("/config/", methods=["GET", "POST"])
# def model_config():
#     # Get the name of the uploaded files
#     if request.method == "POST":
#         pass
#     return render_template("config.html", cfg=MODEL_CONFIG)


if __name__ == "__main__":
    app.run(debug=True, port=8080)

