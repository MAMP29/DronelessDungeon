# Instrucciones de uso

## 1. Crear un entorno virtual de Python

### En Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### En Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### En Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 2. Ejecutar el programa

Una vez activado el entorno virtual, puedes ejecutar el programa:

### Linux/macOS:
```bash
source venv/bin/activate
python main.py
```

### Windows (CMD):
```cmd
venv\Scripts\activate
python main.py
```

### Windows (PowerShell):
```powershell
venv\Scripts\Activate.ps1
python main.py
```

---

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

---

## Agradecimientos

Agradecemos a los siguientes artistas por los assets utilizados en esta aplicación:

### 🎵 Música
- [8 Bit Dungeon](https://pixabay.com/music/video-games-8-bit-dungeon-251388/) – Kaden Cook (Pixabay)  
- [跡地 Ruins](https://pixabay.com/music/pulses-ruins-168316/) – nojisuma (Pixabay)  
- [Ruins of Huja](https://pixabay.com/music/upbeat-ruins-of-huja-291401/) – HTb-music (Pixabay)  
- [Waiting Time](https://pixabay.com/music/video-games-waiting-time-175800/) – Lesiakower (Pixabay)  

### 🎨 Gráficos
- [A Blocky Dungeon](https://opengameart.org/content/a-blocky-dungeon) – Buch (OpenGameArt)  
- [Free Effect and Bullet 16x16](https://bdragon1727.itch.io/free-effect-and-bullet-16x16) – BDragon1727 (Itch.io)
