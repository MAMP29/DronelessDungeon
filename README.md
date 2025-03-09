
# Instrucciones de uso

Para ejecutar el programa deberá crear un entorno virtual de python, para ello emplee los siguientes comandos:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ingrese al entorno virtual y ejecute el programa desde el archivo main.py
```bash
source venv/bin/activate
python main.py
```

## Cargar un mapa
Para cargar un mapa debe seleccionar el botón "Load" y eliga un archivo de mapa en el cuadro de diálogo, este debe de
ser un archivo de texto con la siguiente estructura (o similar):

```
0 0 0 0 0 0 3
0 0 1 0 0 2 0
0 0 1 3 0 0 0
0 1 1 1 1 1 0
0 0 4 0 0 4 0
```

Donde cada número representa lo siguiente:

- 0: vacío
- 1: obstáculo
- 2: dron
- 3: campo electromagnético
- 4: paquete

