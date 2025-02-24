import sys
import os
import time
import textwrap
import whisper
import shutil
import warnings
import argparse

"""Constants"""  # {{{
MODEL_NAMES = [
    "tiny", "base", "small", "medium", "large", "turbo",
    "tiny.en", "base.en", "small.en", "medium.en"
]
TIMESTAMP_NAMES = [
    "With timestamps / Avec horodatages",
    "Without timestamps / Sans horodatages",
    "Create both a file with and without timestamps / Créer les deux fichier avec and sans horodatages"
]
INFO_TEXTS = {
    "en1": textwrap.fill("""
        There are six model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model. The relative speeds below are measured by transcribing English speech on an A100, and the real-world speed may vary significantly depending on many factors including the language, the speaking speed, and the available hardware.
        """, width=50, initial_indent="   ", subsequent_indent="    "),
    "en2": textwrap.fill("""
        The .en models for English-only applications tend to perform better, especially for the tiny.en and base.en models. We observed that the difference becomes less significant for the small.en and medium.en models. Additionally, the turbo model is an optimized version of large-v3 that offers faster transcription speed with a minimal degradation in accuracy.
        """, width=50, initial_indent="   ", subsequent_indent="    "),
    "fr1": textwrap.fill("""
        Il existe six tailles de modèles, dont quatre avec des versions en anglais uniquement, offrant des compromis en termes de vitesse et de précision. Vous trouverez ci-dessous les noms des modèles disponibles ainsi que leurs besoins approximatifs en mémoire et leur vitesse d'inférence par rapport au grand modèle. Les vitesses relatives ci-dessous sont mesurées en transcrivant la parole en anglais sur un A100, et la vitesse réelle peut varier de manière significative en fonction de nombreux facteurs, notamment la langue, la vitesse d'élocution et le matériel disponible.
        """, width=50, initial_indent="  ", subsequent_indent="     "),
    "fr2": textwrap.fill("""
        Les modèles .en pour les applications en anglais uniquement tendent à être plus performants, en particulier pour les modèles tiny.en et base.en. Nous avons observé que la différence devient moins significative pour les modèles small.en et medium.en. En outre, le modèle turbo est une version optimisée de large-v3 qui offre une vitesse de transcription plus rapide avec une dégradation minimale de la précision.
        """, width=50, initial_indent="  ", subsequent_indent="     ")
}

TIMESTAMP_OPTIONS_TEXT = textwrap.dedent(f"""
   Please choose if you would like to add timestamps / Veuillez indiquer si vous souhaitez ajouter des horodatages :
        0. Exit / Sortie
        1. {TIMESTAMP_NAMES[0]}
        2. {TIMESTAMP_NAMES[1]}
        3. {TIMESTAMP_NAMES[2]}
    """)

MODEL_OPTIONS_TEXT = textwrap.dedent("""
    Please choose a model / Veuillez choisir un modèle :
        0. Exit / Sortie
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
    """)

valid_audio_extensions = ['.mp3', '.m4a',
                          '.wav', '.flac', '.ogg', '.aac', '.opus']
# }}}
"""Functions"""  # {{{


def check_audio_file(file_path):
    """Check that file is a recognised audio file type. Returns error message or None."""
    if not os.path.exists(file_path):
        return textwrap.fill(
            "Error: File not found. Please check the file path and try again. / Erreur : Fichier non trouvé. Veuillez vérifier le chemin du fichier et réessayer.",
            width=50, initial_indent="   ", subsequent_indent="    ")
    if not os.path.isfile(file_path):
        return f"Error: {file_path} is not a file. / Erreur : {file_path} n'est pas un fichier."
    if not file_path.lower().endswith(tuple(valid_audio_extensions)):
        error1 = textwrap.fill(
            "Error: File is not a valid audio file type / File n'est pas un type de fichier audio valide.",
            width=50, initial_indent="   ", subsequent_indent="    ")
        error2 = textwrap.fill(
            f"""The valid file types for transcriptor are / Les types de fichiers valides pour le transcriptor sont les suivants : {
                valid_audio_extensions}""",
            width=50, initial_indent="   ", subsequent_indent="    ")
        return error1 + "\n" + error2
    return None


def replace_extension_without_timestamps(file_name):
    """Replace the audio file extension with .txt."""
    root, ext = os.path.splitext(file_name)
    return root + '.txt'


def replace_extension_timestamps(file_name):
    """Replace the audio file extension with .txt."""
    root, ext = os.path.splitext(file_name)
    return root + '_timestamps.txt'


def write_txt_file_with_timestamps(transcription, text_file_path):
    with open(text_file_path, 'w', encoding='utf-8') as f:
        for segment in transcription["segments"]:
            start = convert(segment['start'])
            end = convert(segment['end'])
            f.write(f"{start} - {end}:{segment['text']}\n")


def write_txt_file_without_timestamps(transcription, text_file_path):
    with open(text_file_path, 'w', encoding='utf-8') as f:
        for segment in transcription["segments"]:
            clean_text = segment['text'].lstrip()
            f.write(f"{clean_text}")


def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    if dry_run:
        print(center_text("Dry Run Activated / Mode Test activé"))


def convert(seconds):
    """Convert seconds to a formatted time string."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}h:{m:02d}m:{s:02d}s"


def center_text(text):
    """Center the given text based on the terminal width."""
    terminal_width = shutil.get_terminal_size().columns
    centered_text = text.center(terminal_width)
    return centered_text


def display_model_table():
    """Display a table of model information."""
    headers = ["Multilingual", "Size", "English-only",
               "Required VRAM", "Relative speed"]
    rows = [
        ("tiny", "39 M", "tiny.en", "~1 GB", "~10x"),
        ("base", "74 M", "base.en", "~1 GB", "~7x"),
        ("small", "244 M", "small.en", "~2 GB", "~4x"),
        ("medium", "769 M", "medium.en", "~5 GB", "~2x"),
        ("large", "1550 M", "N/A", "~10 GB", "1x"),
        ("turbo", "809 M", "N/A", "~6 GB", "~8x")
    ]
    models = "Models"
    print(f"{models:<12}")
    print(f"""{headers[0]:<12} {headers[1]:<10} {
          headers[2]:<12} {headers[3]:<15} {headers[4]:<12}""")
    print("-" * 80)
    for row in rows:
        print(f"""{row[0]:<12} {row[1]:<10} {
              row[2]:<12} {row[3]:<15} {row[4]:<12}""")
        print("-" * 80)


def display_model_options():
    """Display the model options and info texts."""
    display_model_table()
    print(center_text(MODEL_OPTIONS_TEXT))


def display_timestamp_options():
    """Display the timestamp options and info texts."""
    print(center_text(TIMESTAMP_OPTIONS_TEXT))


def get_user_timestamp_choice():
    """Get and return the user's timestamp choice."""
    while True:
        try:
            clear_terminal()
            display_timestamp_options()
            choice = int(input(
                "Enter the number of your choice (1-3) / Entrez le numéro de votre choix (1-3): "))
            if 0 <= choice <= 3:
                if choice == 0:
                    print("Exiting")
                    sys.exit(1)
                else:
                    return choice - 1
            else:
                print("Invalid choice, please select a number between 1 and 3. / Choix invalide, veuillez sélectionner un numéro entre 1 et 3.")
        except ValueError:
            print(
                "Invalid input, please enter a number. / Entrée invalide, veuillez entrer un numéro.")


def get_user_model_choice():
    """Get and return the user's model choice."""
    while True:
        try:
            clear_terminal()
            display_model_options()
            choice = int(input(
                "Enter the number of your choice (1-12) / Entrez le numéro de votre choix (1-12): "))
            if 0 <= choice <= 12:
                if choice == 0:
                    print("Exiting")
                    sys.exit(1)
                if choice == 11:
                    clear_terminal()
                    print(INFO_TEXTS["en1"])
                    print(INFO_TEXTS["en2"])
                    input("Press Enter to continue...")
                elif choice == 12:
                    clear_terminal()
                    print(INFO_TEXTS["fr1"])
                    print(INFO_TEXTS["fr2"])
                    input("Appuyez sur Entrée pour continuer...")
                else:
                    return MODEL_NAMES[choice - 1]
            else:
                print("Invalid choice, please select a number between 1 and 12. / Choix invalide, veuillez sélectionner un numéro entre 1 et 12.")
        except ValueError:
            print(
                "Invalid input, please enter a number. / Entrée invalide, veuillez entrer un numéro.")


# }}}
"""Main script"""  # {{{


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using Whisper models.")
    parser.add_argument('audio_files', nargs='+',
                        help='Audio file(s) to transcribe')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simulate processing without writing files')
    parser.add_argument('--model', choices=MODEL_NAMES,
                        help='Specify the Whisper model to use (by name)')
    parser.add_argument('--timestamps', choices=['y', 'n', 'b'],
                        help='Timestamp option: y=timestamps only, n=no timestamps, b=both')
    args = parser.parse_args()

    dry_run = args.dry_run
    audio_files = args.audio_files

    # Validate all files
    all_errors = []
    for file in audio_files:
        error = check_audio_file(file)
        if error:
            all_errors.append(error)

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)

    # Determine model choice
    if args.model:
        model_choice = args.model
    else:
        model_choice = get_user_model_choice()
    print(
        f"The {model_choice} model was chosen / Le modèle {model_choice} a été choisi.")

    # Determine timestamp choice
    if args.timestamps is not None:
        timestamp_choice_letter = args.timestamps
        if timestamp_choice_letter == 'y':
            timestamp_choice = 0
        elif timestamp_choice_letter == 'n':
            timestamp_choice = 1
        else:  # timestamp_choice_letter == 'b'
            timestamp_choice = 2
    else:
        timestamp_choice = get_user_timestamp_choice()
    timestamp_txt_list = TIMESTAMP_NAMES[timestamp_choice].split(' / ')
    print(
        f"{timestamp_txt_list[0]} was chosen / {timestamp_txt_list[1]} a été choisi.")

    if not dry_run:
        print("Loading the model / Chargement du modèle")
        model = whisper.load_model(model_choice)
        # Suppress the FP16 warning
        warnings.filterwarnings("ignore",
                                message="FP16 is not supported on CPU; using FP32 instead",
                                category=UserWarning)

    for audio_file_path in audio_files:
        audio_dir = os.path.dirname(audio_file_path)
        audio_file_name = os.path.basename(audio_file_path)

        text_file_name = replace_extension_without_timestamps(audio_file_name)
        text_file_name_timestamp = replace_extension_timestamps(
            audio_file_name)

        text_file_path = os.path.join(audio_dir, text_file_name)
        text_file_with_timestamps_path = os.path.join(
            audio_dir, text_file_name_timestamp)

        if dry_run:
            print(f"\nDry run: Processing / Traitement du {audio_file_name}")
            if timestamp_choice == 0:
                print(
                    f"Would create timestamped file / Créerait un fichier horodaté : {text_file_name_timestamp}")
            elif timestamp_choice == 1:
                print(
                    f"Would create simple transcript / Créerait un fichier simple : {text_file_name}")
            elif timestamp_choice == 2:
                print(f"Would create both files / Créerait les deux fichiers :")
                print(f"- {text_file_name}")
                print(f"- {text_file_name_timestamp}")
            continue  # Skip actual processing for dry-run

        print(center_text(
            f"Processing {audio_file_name} with {model_choice} model / Traitement de {audio_file_name} avec le modèle {model_choice}"))
        start_time = time.time()
        print(center_text("Transcription started / Transcription commencée"))

        transcription = model.transcribe(audio_file_path)

        end_time = time.time()
        duration = end_time - start_time
        print(center_text(
            f"Transcription finished in / Transcription terminée en {convert(duration)}"))

        if timestamp_choice == 0:
            write_txt_file_with_timestamps(
                transcription, text_file_with_timestamps_path)
            print(center_text(
                f"Transcription with timestamps saved to / Transcription avec horodatages enregistrée dans {text_file_with_timestamps_path}"))
        elif timestamp_choice == 1:
            write_txt_file_without_timestamps(transcription, text_file_path)
            print(center_text(
                f"Transcription saved to / Transcription enregistrée dans {text_file_path}"))
        else:
            write_txt_file_with_timestamps(
                transcription, text_file_with_timestamps_path)
            print(center_text(
                f"Transcription with timestamps saved to / Transcription avec horodatages enregistrée dans {text_file_with_timestamps_path}"))
            write_txt_file_without_timestamps(transcription, text_file_path)
            print(center_text(
                f"Transcription saved to / Transcription enregistrée dans {text_file_path}"))
            # }}}
