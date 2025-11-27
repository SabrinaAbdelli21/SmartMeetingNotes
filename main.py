import whisper
import os

# --- Fonctions ---

# Charge le modèle Whisper et transcrit le fichier audio
# Le chemin du fichier doit être relatif au conteneur Docker.
def transcrire_audio(chemin_fichier, modele="small"):
    # Vérification de l'existence du fichier audio
    if not os.path.exists(chemin_fichier):
        # Utilise un message d'erreur clair au lieu d'alert()
        print(f"ERREUR: Le fichier audio '{chemin_fichier}' n'a pas été trouvé dans le conteneur.")
        print("Veuillez vous assurer que le volume de montage est correctement configuré.")
        return None, None

    print(f"Chargement du modèle '{modele}'...")
    try:
        # Tente de charger le modèle
        model = whisper.load_model(modele)
    except Exception as e:
        print(f"ERREUR lors du chargement du modèle Whisper: {e}")
        return None, None

    print(f"Transcription du fichier '{chemin_fichier}'...")
    try:
        # Tente de transcrire
        result = model.transcribe(chemin_fichier)
    except Exception as e:
        print(f"ERREUR lors de la transcription: {e}")
        return None, None

    return result["text"], result["segments"]

# Enregistrement du texte dans un fichier .txt
def enregistrer_transcription_txt(texte, chemin_txt):
    if texte is None:
        print("Opération d'enregistrement annulée car la transcription a échoué.")
        return

    try:
        # Utilisation de 'w' pour écraser le contenu ou créer le fichier
        with open(chemin_txt, "w", encoding="utf-8") as f:
            f.write(texte)
        print(f"Transcription enregistrée dans '{chemin_txt}'.")
    except Exception as e:
        print(f"ERREUR lors de l'enregistrement du fichier: {e}")

# --- Programme principal ---
if __name__ == "__main__":
    # NOTE IMPORTANTE:
    # Le chemin d'accès au fichier audio est DANS LE CONTENEUR.
    # Lorsque vous lancerez le conteneur, vous utiliserez un VOLUME
    # pour mapper votre dossier local (C:/Users/sabdelli/Documents/Whisper_audio/)
    # au dossier /app/input/ du conteneur.

    # L'audio doit être placé dans le conteneur sous ce nom :
    CHEMIN_FICHIER_AUDIO_DANS_CONTENEUR = "/app/data/Everyday Conversation In Slow French Super Easy French.mp3"
    
    # Le fichier de sortie sera créé ici (dans le conteneur).
    # Il apparaîtra dans votre dossier local si vous utilisez un autre volume pour la sortie.
    CHEMIN_FICHIER_TXT_DANS_CONTENEUR = "/app/retranscription/Everyday Conversation In Slow French Super Easy French.txt"
    
    NOM_MODELE = "small"

    # Transcription
    texte_transcrit, timestemps = transcrire_audio(CHEMIN_FICHIER_AUDIO_DANS_CONTENEUR, modele=NOM_MODELE)

    # Affichage des timestamps si la transcription a réussi
    if timestemps:
        print("\n--- Timestamps ---")
        for segment in timestemps:
            print(f"[ {segment['start']:.2f} - {segment['end']:.2f} ] {segment['text']}")

    # Enregistrer dans un fichier
    enregistrer_transcription_txt(texte_transcrit, CHEMIN_FICHIER_TXT_DANS_CONTENEUR)