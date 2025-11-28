# 🧠 SmartMeetingNotes

**SmartMeetingNotes** est un projet permettant de **transcrire des fichiers audio en texte** en utilisant le modèle`Whisper`de OpenAI. 
Le script est conçu pour être utilisé dans un **conteneur Docker**, avec des volumes pour mapper les fichiers audio et les fichiers de sortie entre le conteneur et votre machine locale.


## 🚀 Prérequis

- Docker installé sur votre machine  
- Python 3.8+ dans le conteneur  
- Bibliothèque `whisper` installée dans l’environnement Python du conteneur  


## 📁 Structure du Projet

```
SmartMeetingNotes/
├── 📂 data/
│ └── 🎵 FichierAudio1.mp3 <-- Vos fichiers audio à traiter
├── 📂 retranscription/
│ └── 📝 transcription.txt <-- La sortie après l'exécution
├── 🐍 main.py <-- Le script Python (Moteur de transcription)
├── 🐳 Dockerfile <-- La recette de construction de l'environnement
└── 📦 requirements.txt <-- Les dépendances Python (whisper)
```

## 🛠️ Instructions d'Installation et d'Utilisation

Suivez ces étapes pour transcrire un nouveau fichier audio.


### Étape 1 : Préparation de l'Audio

Placez votre nouveau fichier audio (ex : `MonNouveauFichier.mp3`) dans le dossier `data/`.

> ⚠️ **Attention** : Le Dockerfile actuel est optimisé pour les fichiers se trouvant directement dans le dossier `data/`.  
> Si vous utilisez le script qui traite un seul fichier, assurez-vous de mettre à jour la ligne `CHEMIN_FICHIER_AUDIO_DANS_CONTENEUR` dans `main.py`.


### Étape 2 : Construction de l'Image Docker

Depuis la racine du projet (`F:\SmartMeetingNotes`), exécutez :

```bash
docker build -t smart-meeting-whisper .
```

###  Étape 3 : Exécution de la Transcription

Lancez la transcription et mappez votre dossier de sortie local :

```bash
docker run --rm -v F:\SmartMeetingNotes\retranscription:/app/retranscription smart-meeting-whisper
```

### Étape 4 : Récupération du Résultat

Une fois l'exécution terminée, le fichier de transcription (transcription.txt ou le nom correspondant à l'audio) sera disponible dans votre dossier local :

```bash
F:\SmartMeetingNotes\retranscription\
```
 
## ⚙️ Détails Techniques

* Modèle utilisé : small (bonne balance entre vitesse et précision). Vous pouvez le modifier en éditant main.py.
* Conteneur : Utilise python:3.11-slim-bookworm et installe ffmpeg.
* Persistance : Le volume de montage (-v) garantit que les données transcrites sont stockées sur votre PC et ne sont pas perdues lorsque le conteneur est supprimé.


