# Transcriptor Script

🇬🇧 English | 🇫🇷[Lire en français](README_fr.md)

`transcriptor.py` is a Python script for transcribing audio files using the Whisper model created by OpenAI. It supports multiple model sizes and offers options for both multilingual and English-only transcriptions.
More info on openai-whisper can be found [here (pypi.org)](https://pypi.org/project/openai-whisper/) and [here (github)](https://github.com/openai/whisper)

Valid audio extensions: `.mp3`, `.m4a`, `.wav`, `.flac`, `.ogg`, `.aac`, `.opus`

## Prerequisites

- Python 3.7 or higher
- Required Python packages: `whisper`, `shutil`, `textwrap`
- Command-line tools: `ffmpeg`
- Rust

<details>
  <summary>Note for Non-Programmers</summary>
You only need to install the `whisper` package separately because it's not included with Python. The other packages like `shutil` and `textwrap` come pre-installed with Python, so you don't need to worry about them.
</details>

## Installation

1. Clone this repository or download the `transcriptor.py` script.
2. Ensure you have the necessary Python version and install the required packages:

   ```bash

   pip install -U openai-whisper
   # on Arch Linux
   sudo pacman -S python-openai-whisper
   ```

3. Ensure the command-line tool `ffmpeg` is installed on your system, which is available from most package managers:

   ```bash
   # on Ubuntu or Debian
   sudo apt update && sudo apt install ffmpeg
   
   # on Arch Linux
   sudo pacman -S ffmpeg
   
   # on MacOS using Homebrew (https://brew.sh/)
   brew install ffmpeg
   
   # on Windows using Chocolatey (https://chocolatey.org/)
   choco install ffmpeg
   
   # on Windows using Scoop (https://scoop.sh/)
   scoop install ffmpeg
   ```

4. If you encounter installation errors related to tiktoken, you may need to install Rust. Please refer to the Rust Getting Started page for installation instructions. You may also need to configure the PATH environment variable, e.g.:

  ```bash
  export PATH="$HOME/.cargo/bin:$PATH"
  ```

If the error message states No module named 'setuptools_rust', install setuptools-rust with:

  ```bash
  pip install setuptools-rust
  ```

## Usage

### Basic Command

To run the script, use the following command:

```bash
python transcriptor.py <audio_file.m4a> [--dry-run]
```

- `<audio_file.m4a>`: Path to the audio file you want to transcribe.
- `--dry-run` (optional): Runs the script without actually performing the transcription, useful for testing.

### Example

```bash
python transcriptor.py example_audio.m4a
```

This will transcribe `example_audio.m4a` using the selected Whisper model and save the transcription to a text file with the same name.

### Selecting a Model

After running the script, you will be prompted to choose a model:

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

Enter the number corresponding to the desired model to proceed.

### Information Options

- `11`: Displays detailed information about the models in English.
- `12`: Displays detailed information about the models in French.

### Output

The script generates a text file with the transcribed content, named after the input audio file but with a `.txt` extension. For example, if the input file is `example_audio.m4a`, the output will be `example_audio.txt`.

## Notes

- Ensure the audio file exists at the specified path.
- The script uses Whisper models, so make sure you have sufficient resources (VRAM) for the selected model size.

## Troubleshooting

- **File not found:** Ensure the correct path to the audio file is provided.
- **Invalid input:** Enter a valid number when choosing a model.
- **Dry run mode:** No transcription is performed, and the script only simulates the steps.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
