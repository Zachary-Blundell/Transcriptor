# Script Transcriptor

🇫🇷 Française | 🇬🇧 [Read in English](README.md)

`transcriptor.py` est un script Python permettant de transcrire des fichiers audio en utilisant le modèle Whisper créer par OpenAI. Il prend en charge plusieurs tailles de modèles et offre des options pour des transcriptions multilingues ou en anglais uniquement.  
Plus d’informations sur openai-whisper sont disponibles [ici (pypi.org)](https://pypi.org/project/openai-whisper/) et [ici (github)](https://github.com/openai/whisper).  

Extensions audio valides : `.mp3`, `.m4a`, `.wav`, `.flac`, `.ogg`, `.aac`, `.opus`

## Prérequis

- Python 3.7 ou supérieur  
- Packages Python requis : `whisper`, `shutil`, `textwrap`  
- Outils en ligne de commande : `ffmpeg`  
- Rust  

<details>
  <summary>Note pour les non-programmeurs</summary>
  Vous devez seulement installer le package `whisper` séparément, car il n'est pas inclus avec Python. Les autres packages comme `shutil` et `textwrap` sont préinstallés avec Python, donc vous n'avez pas à vous en soucier.
</details>

## Installation

1. Clonez ce dépôt ou téléchargez le script `transcriptor.py`.  
2. Assurez-vous d’avoir la bonne version de Python et installez les packages requis :  

   ```bash
   pip install -U openai-whisper
   # sur Arch Linux
   sudo pacman -S python-openai-whisper
   ```

3. Assurez-vous que l’outil en ligne de commande `ffmpeg` est installé sur votre système. Il est disponible via la plupart des gestionnaires de paquets :

   ```bash
   # sur Ubuntu ou Debian
   sudo apt update && sudo apt install ffmpeg

   # sur Arch Linux
   sudo pacman -S ffmpeg

   # sur macOS avec Homebrew (https://brew.sh/)
   brew install ffmpeg

   # sur Windows avec Chocolatey (https://chocolatey.org/)
   choco install ffmpeg

   # sur Windows avec Scoop (https://scoop.sh/)
   scoop install ffmpeg
   ```

4. Si vous rencontrez des erreurs d’installation liées à `tiktoken`, vous devrez peut-être installer Rust. Consultez la page officielle Rust Getting Started pour les instructions d’installation. Vous devrez peut-être aussi configurer la variable d’environnement PATH, par exemple :

   ```bash
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

   Si un message d’erreur indique `No module named 'setuptools_rust'`, installez `setuptools-rust` avec :

   ```bash
   pip install setuptools-rust
   ```

## Utilisation

### Commande de base

Pour exécuter le script, utilisez la commande suivante :

```bash
python transcriptor.py <audio_file.m4a> [--dry-run]
```

- `<audio_file.m4a>` : Chemin du fichier audio à transcrire.  
- `--dry-run` (optionnel) : Exécute le script sans effectuer la transcription, utile pour tester.  

### Exemple

```bash
python transcriptor.py example_audio.m4a
```

Cela transcrira `example_audio.m4a` avec le modèle Whisper sélectionné et enregistrera la transcription dans un fichier texte portant le même nom.

### Sélection d’un modèle

Après avoir lancé le script, vous serez invité à choisir un modèle :

```
Please choose a model / Veuillez choisir un modèle :
    1. tiny
    2. base
    3. small
    4. medium
    5. large
    6. turbo
    7. tiny.en
    8. base.en
    9. small.en
    10. medium.en
    11. More info (English)
    12. Plus d'informations (Français)
```

Entrez le numéro correspondant au modèle souhaité pour continuer.

### Options d’information

- `11` : Affiche des informations détaillées sur les modèles en anglais.  
- `12` : Affiche des informations détaillées sur les modèles en français.  

### Résultat

Le script génère un fichier texte contenant la transcription, nommé d’après le fichier audio d’entrée mais avec une extension `.txt`. Par exemple, si le fichier d’entrée est `example_audio.m4a`, le fichier de sortie sera `example_audio.txt`.

## Remarques

- Assurez-vous que le fichier audio existe à l’emplacement spécifié.  
- Le script utilise les modèles Whisper, donc assurez-vous d’avoir des ressources suffisantes (VRAM) pour la taille du modèle sélectionné.  

## Dépannage

- **Fichier introuvable** : Vérifiez que le chemin du fichier audio est correct.  
- **Entrée invalide** : Entrez un numéro valide lors du choix du modèle.  
- **Mode simulation (`dry run`)** : Aucune transcription n’est effectuée, le script ne fait que simuler les étapes.  

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
