import os
import glob
from werkzeug.utils import secure_filename

import re
import numpy as np
from unidecode import unidecode
from gensim.models import KeyedVectors


os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Comenta esta linea si quieres usar cuda
import cv2
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

import config

def allowed_file(filename):
    """
    Revisa si el archivo tiene una extension valida
    """
    basename, ext = os.path.splitext(filename)
    return  ext in config.ALLOWED_EXTENSIONS

def create_dir_if_not_exists(path):
    """
    Crea un directorio si no existe
    """
    if not os.path.exists(path):
        os.makedirs(path)

def init_metadata_if_not_exists():
    """
    Crea los archivos dentro de metadata en caso de que no existan
    """
    for cfg in config.MODELS:
        if not os.path.exists(config.MODELS[cfg]["descriptors"]):
            df = pd.DataFrame()
            df["paths"] = []
            df.to_csv(config.MODELS[cfg]["descriptors"], sep="|", index=False)


def upload_files(files):
    """
    Sube los archivos a la carpeta definida
    """
    # Iterate over files
    for file in files:
        # Check if file exist and have an allowed extension
        if file and allowed_file(file.filename):
            # Verify filename
            filename = secure_filename(file.filename)
            # Save file
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))

def load_kv_model(path):
    """
    Carga el LookUpTable de W2V
    """
    return KeyedVectors.load(path, mmap='r')

def load_tf_model(path):
    """
    Carga el modelo de regresion de imagenes
    """
    return tf.keras.models.load_model(path)

def read_stopwords(path):
    """
    Carga las stopwords para el modelo de texto
    """
    with open(path, 'r') as f:
        stopwords = f.readlines()
    return [stopword.strip() for stopword in stopwords]

def load_model(model):
    """
    Wrapper de las funcioens load_kf, load_tf, read_stopwords
    """
    # model :: english-128
    text_model = load_kv_model(config.MODELS[model]["text-model"])
    image_model = load_tf_model(config.MODELS[model]["image-model"])
    stopwords = read_stopwords(config.MODELS[model]["stopwords"])
    return image_model, text_model, stopwords

def annotations_to_lower(annotations):
    """
    Recibe una lista de textos y los pasa a minuscula
    """
    return [ann.lower() for ann in annotations]

def annotations_to_unidecode(annotations):
    """
    Recibe una lista de textos y quita los caracteres extranos
    """
    return [unidecode(ann) for ann in annotations]

def remove_non_alphabetic(annotations):
    """
    Recibe una lista de textos y elimina los numeros u otros caracteres
    """
    regex = re.compile('[^a-zA-Z]')
    return [regex.sub(' ', ann) for ann in annotations]

def strip_annotations(annotations):
    """
    Recibe una lista de textos y quita los espacios al comienzo y final
    """
    return [ann.strip() for ann in annotations]

def remove_stopwords(annotations, stop_words=[]):
    """
    Recibe una lista de textos y stopwords, luego elimina las stopwords para cada elemento de la lista de textos
    """
    return [' '.join([word for word in ann.split() if word not in stop_words]) for ann in annotations]

def tokenize_annotations(annotations):
    """
    Recibe una lista de textos y los tokeniza: "hola como estas" -> ["hola", "como", "estas"]
    """
    return [ann.split() for ann in annotations]

def clean_annotation_pipeline(annotation, stopwords):
    """
    Wrapper de todas las funciones de procesamiento de texto anteriores
    """
    # convert to list if necessary
    if not isinstance(annotation, list):
        annotations = [annotation]
    annotations = annotations_to_lower(annotations)
    annotations = annotations_to_unidecode(annotations)
    annotations = remove_non_alphabetic(annotations)
    annotations = strip_annotations(annotations)
    annotations = remove_stopwords(annotations, stopwords)
    return annotations

def get_word_vector(kv_vectors, word, missing_mode="zeros"):
    """
    Recibe una palabra y retorna su vector, si no esta en el vocabulario retonar ceros
    """
    if word in kv_vectors.vocab:
        return kv_vectors.vocab[word]
    else:
        # what to do with unknown words
        if missing_mode == "zeros":
            return np.zeros(kv_vectors.vector_size)

def get_annotations_vector(kv_vectors, annotations, missing_mode="zeros", agg_mode="mean"):
    # convert to list if necessary
    """
    Recibe una lista de frases y retonar el vector de la clase segun el metodo establecido:
    agg_mode = mean: promedia los vectores de las palabras
    """
    if not isinstance(annotations, list):
        annotations = [annotations]
    sentences_vectors = []
    for sentence in tokenize_annotations(annotations):
        words_vectors = [get_word_vector(kv_vectors, token) for token in sentence]
        # how to aggregate word vectors
        if agg_mode == "mean":
            sentence_vector = np.mean(words_vectors, axis=0)
        sentences_vectors.append(sentence_vector)
    return sentences_vectors


def get_image_descriptors(model, paths, resize=224):
    """
    Recibe el modelo de imagenes junto una lista imagenes y calcula su descriptores
    """
    if not isinstance(paths, list):
        paths = [paths]
    n = paths.__len__()
    descriptors = []
    for i, path in enumerate(paths):
        print(f"Calculando descriptores para imagen {i} de {n}", end="\r", flush=True)
        img =  cv2.imread(path)
        img = cv2.resize(img,(resize,resize))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        descriptors.append(model.predict(img)[0])
    return descriptors

def update_descriptors(model, cfg):
    """
    Actualiza los archivos de metadata según la configuracion dada
    """
    metadata = pd.read_csv(config.MODELS[cfg]["descriptors"], sep="|")
    images = [img.replace("\\","/") for ext in config.ALLOWED_EXTENSIONS for img in glob.glob(config.UPLOAD_FOLDER+f"*{ext}") ]

    inner = metadata[metadata["paths"].isin(images)]
    out = [p for p in images if p not in list(metadata["paths"])]

    out_descriptors = get_image_descriptors(model, out)

    out_df = pd.DataFrame(out_descriptors)
    out_df.columns = [f"des_{col}" for col in out_df.columns]
    out_df["paths"] = out
    

    metadata_update = pd.concat([inner, out_df])
    metadata_update.to_csv(config.MODELS[cfg]["descriptors"], sep="|", index=False)

def cosine_similarity(array1, array2):
    """
    Calcula la similitud coseno entre dos arrays
    """
    # -sum(l2_norm(y_true) * l2_norm(y_pred))
    return -dot(array1, array2)/(norm(array1)*norm(array2))

def get_neighbors(metadata, descriptor, k=5):
    """
    Busca los k vecinos mas de un array::descriptor en un dataframe::metadata
    """
    neighbors = metadata.copy()
    cols = [x for x in neighbors.columns if "des" in x]

    neighbors['similarity'] = neighbors[cols].apply(lambda x: cosine_similarity(x, descriptor), axis=1)
    neighbors = neighbors.sort_values(by=["similarity"], ascending=True)
    return neighbors["paths"].tolist()[:k]


def search(query, stopwords, text_model, cfg):
    """
    Recibe un texto y busca las imagenes correspondientes
    """
    query = clean_annotation_pipeline(query, stopwords)
    query_descriptor = get_annotations_vector(text_model, query)[0]

    metadata = pd.read_csv(config.MODELS[cfg]["descriptors"],sep="|")
    neighbors = get_neighbors(metadata, query_descriptor, k=config.DFLT_NEIGHBORS)
    
    return neighbors

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    chunked = []
    for i in range(0, len(lst), n):
        chunked.append(lst[i:i + n])
    return chunked