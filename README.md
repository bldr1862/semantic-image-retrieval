# Semantic Image Retrieval
 
<p>
Si alguna vez has buceado en tus imágenes para encontrar lo que estabas buscando, esta herramienta te puede ahorrar mucho tiempo. Usando Machine Learning, ahora puedes buscar en tus fotos tal como lo haces en Google.
 
</p>
<img src="example.PNG" alt="drawing" style="width:700px;"/>
 
## Cómo usarla
 
### Paso 1: Instalar dependencias
 
Primero debes instalar las dependencias necesarias para ejecutar la aplicación.
 
```
python -m venv virtual_env
cd virtual_env/Scripts/
activate
cd ../../
pip install -r requirements.txt
```
 
### Paso 2: Descargar modelos
 
Luego, debes descargar los modelos, descomprimirlos y copia las carpetas dentro de "models/"
 
* english-300: https://drive.google.com/file/d/1Me2OGM3FyNM95aJGIAIXb7RxclYWQSz4/view?usp=sharing
* spanish-300: https://drive.google.com/file/d/1wP7huw2PDhujpejoOTDKOK-bVyGEAc-K/view?usp=sharing
 
El directorio debe quedar con la siguiente estructura:
```
semantic-image-retrieval/
│   README.md
│   main.py 
|   config.py  
|   ...
│
└───models/
│   │
│   └───english-300/
│   |   │   image-model/
│   |   │   english-300kv
│   |
|   └───spanish-300/
|       |   image-model/
|       |   spanish-300.kv
```
 
 
 
### Paso 3: Start App
 
Para ejecutar la aplicación, debes ejecutar el siguiente comando, el cual levantará un servicio en el puerto 8080.
 
```
python main.py
```
 
 
Ingresa la siguiente dirección en tu navegador: http://127.0.0.1:8080/ Luego entra a la sección uploads y sube las fotos en las que quieres buscar.
Cuando subes las fotos el sistema debe indexarlas para poder buscar en ellas, por lo tanto, este paso puede demorar bastante según la cantidad de fotos que subas.
Cuando esto termina, te va a redirigir a la sección Search donde puedes buscar en tus imágenes
 
### Adicional: Configuración
 
En el archivo config.py hay variables de configuración de la aplicación:
 
* UPLOAD_FOLDER: Carpeta donde quedan almacenadas las fotos - **No cambiar**
* ALLOWED_EXTENSIONS: Son las extensiones de las imágenes permitidas por la aplicación, se puede agregar más si es necesario. 
* METADATA_DIR: Directorio donde se indexan las imágenes - **No cambiar**
* GRID_SIZE: Cantidad de imágenes que se muestran por fila - **No cambiar**
 
 
* DFLT_NEIGHBORS: Cantidad de resultados que entrega la búsqueda
* MODEL_CONFIG: Modelo que se desea utilizar, se pueden usar dos valores: "english-300" para búsquedas en inglés y "spanish-300" para búsquedas en español.
 
* MODELS: Variable de control sobre los modelos - **No cambiar**
 
### Disclaimer 
Estos modelos fueron entrenados con el dataset MSCOCO 2014, por lo tanto hay búsquedas que funcionan mejor que otras según los ejemplos presentes en en este dataset. Para el modelo fue construido a partir de la traducción a través de Google Sheets de MSCOCO, por lo tanto, es esperable que los resultados de las búsquedas sean de menor calidad.