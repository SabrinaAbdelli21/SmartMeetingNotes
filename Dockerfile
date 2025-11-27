# ÉTAPE 1: Image de base Python. Utilisation d'une version 'slim' pour rester léger.
FROM python:3.11-slim-bookworm

# ÉTAPE 2: Installer les dépendances système. 
# 'ffmpeg' est absolument nécessaire pour Whisper afin de lire les fichiers audio/vidéo.
# 'libsm6' et 'libxext6' sont parfois requis pour les librairies de traitement d'images/vidéo.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ÉTAPE 3: Définir le répertoire de travail par défaut dans le conteneur.
WORKDIR /app

# ÉTAPE 4: Copier le fichier de dépendances Python.
COPY requirements.txt .

# ÉTAPE 5: Installer les dépendances Python listées dans requirements.txt.
# --no-cache-dir pour réduire la taille de l'image.
RUN pip install --no-cache-dir -r requirements.txt

# ÉTAPE 6: Copier le script principal.
COPY main.py .

# ÉTAPE 7: Créer les dossiers qui serviront de points de montage pour les VOLUMES.
# C'est une bonne pratique pour clairement définir les I/O.
COPY data /app/data
RUN mkdir -p /app/retranscription/

# ÉTAPE 8: Commande par défaut à exécuter lorsque le conteneur démarre.
CMD ["python", "main.py"]