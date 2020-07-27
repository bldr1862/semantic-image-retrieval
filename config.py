UPLOAD_FOLDER = "static/uploads/" # Carpeta donde se guardan las fotos
ALLOWED_EXTENSIONS = [".jpg"] # Extensiones permitidas por el sistema, se pueden agregar otras si es encesario
METADATA_DIR = "metadata/" # En está carpeta se indexan las imágenes
GRID_SIZE = 3 # NO cambiar: Controla la cantidad de imagenes por fila, NO TOCAT


DFLT_NEIGHBORS = 500 # Numero de imagenes que muestra cuando se realiza una busqueda
MODEL_CONFIG = "english-300" # Esto determina el modelo a usar en la busqueda. Se puede usar una de las llaves de MODELS: "english-128", "english-300"

MODELS = {

    "english-300":{
        "image-model":"models/english-300/image-model/",
        "text-model":"models/english-300/english-300.kv",
        "stopwords":"stopwords/en-stopwords.txt",
        "descriptors":f"{METADATA_DIR}/descriptors-en-300.csv",
    },

    "spanish-300":{
        "image-model":"models/spanish-300/image-model/",
        "text-model":"models/spanish-300/spanish-300.kv",
        "stopwords":"stopwords/es-stopwords.txt",
        "descriptors":f"{METADATA_DIR}/descriptors-es-300.csv",
    },
}