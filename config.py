UPLOAD_FOLDER = "static/uploads/" # Carpeta donde se guardan las fotos
ALLOWED_EXTENSIONS = [".jpg"] # Extensiones permitidas por el sistema, se pueden agregar otras si es encesario
METADATA_DIR = "metadata/" # Carpeta que contiene la metadata



DFLT_NEIGHBORS = 500 # Numero de imagenes que muestra cuando se realiza una busqueda
MODEL_CONFIG = "english-128" # Esto determina el modelo a usar en la busqueda. Se puede usar una de las llaves de MODELS: "english-128", "english-300"
MODELS = {
    "english-128":{
        "image-model":"models/english-128/image-model/",
        "text-model":"models/english-128/english-128.kv",
        "stopwords":"stopwords/english.txt",
        "descriptors":f"{METADATA_DIR}/descriptors-en-128.csv",
    },
    "english-300":{
        "image-model":"models/english-300/image-model/",
        "text-model":"models/english-300/english-300.kv",
        "stopwords":"stopwords/english.txt",
        "descriptors":f"{METADATA_DIR}/descriptors-en-300.csv",
    },
}