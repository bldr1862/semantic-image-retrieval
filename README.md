# Semantic Image Retrieval

<img src="example.PNG" alt="drawing" style="width:700px;"/>

### Instalar dependencias

```
python -m venv virtual_env
cd virtual_env/Scripts/
activate
cd ../../
pip install -r requirements.txt
```

### Configuración

Descargar los modelos de los siguientes links y descromprimirlos dentro de la carpeta models:
* english-128: https://drive.google.com/file/d/1Cr7ZIYqYdoYUVHjHoEj_YoPY6Zh8swRG/view?usp=sharing
* english-300: https://drive.google.com/file/d/1TQxYBlQe7Cr1jU9zsbslGCcSGaxEIAT_/view?usp=sharing


Abrir el archivo config y configurar el modelo que se desea usar: english-128, english-300

### Start

python main.py

### Cómo usar?

Entrar a uploads y subir las fotos, luego entrar a search y empezar a buscar. En la barra lateral aparece el modelo que se está usando