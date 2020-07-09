UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = [".jpg"]


MODEL_CONFIG = "english-128" # Change this to use another model
DFLT_NEIGHBORS = 500

METADATA_DIR = "metadata/"

GRID_SIZE = 3

MODELS = {
    "english-128":{
        "image-model":"models/english-128/image-model/",
        "text-model":"models/english-128/english-128.kv",
        "stopwords":"stopwords/english.txt",
        "descriptors":"metadata/descriptors-en-128.csv",
    },
    "english-300":{
        "image-model":"models/english-300/image-model/",
        "text-model":"models/english-300/english-300.kv",
        "stopwords":"stopwords/english.txt",
        "descriptors":"metadata/descriptors-en-300.csv",
    },
}