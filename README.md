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
python transcriptor.py <audio_file.m4a> [--dry-run] [--model MODEL_NAME] [--timestamps {y,n,b}]
```

Where:

- `<audio_file.m4a>`: Path to the audio file(s) you want to transcribe.
- `--dry-run` (optional): Executes a simulation without actually performing the transcription, useful for testing.
- `--model MODEL_NAME` (optional): Specifies the Whisper model to use. Accepted values are:  
  `tiny`, `base`, `small`, `medium`, `large`, `turbo`, `tiny.en`, `base.en`, `small.en`, `medium.en`.  
  *If omitted, you’ll be prompted to select a model interactively.*
- `--timestamps {y,n,b}` (optional): Sets the timestamp mode. Options are:  
  - `y`: Timestamps only  
  - `n`: No timestamps  
  - `b`: Both timestamps and non-timestamped transcription  
  *If not provided, you’ll be prompted to choose a timestamp option interactively.*

### Example

**Interactive Mode (using menus):**

```bash
python transcriptor.py example_audio.m4a
```

This command will prompt you to select a model and a timestamp option interactively, then transcribe `example_audio.m4a` and save the output as `example_audio.txt`.

**Bypassing the Menus:**

```bash
python transcriptor.py example_audio.m4a --model small --timestamps b
```

This command bypasses the menus by directly selecting the `small` model and enabling both types of timestamps.

### Interactive Selections

#### Model Selection

If you omit the `--model` flag, the script will display:

```sh
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

Enter the corresponding number to choose the desired model.

### Information Options

- `11`: Displays detailed information about the models in English.
- `12`: Displays detailed information about the models in French.

#### Timestamp Selection

If you omit the `--timestamps` flag, you will be prompted to select your timestamp option (y, n, or b) interactively.

### Help

Use the `--help` or `-h` flag to display detailed usage information:

```bash
python transcriptor.py --help
```

This displays:

```sh
usage: transcriptor.py [-h] [--dry-run]
                       [--model {tiny,base,small,medium,large,turbo,tiny.en,base.en,small.en,medium.en}]
                       [--timestamps {y,n,b}]
                       audio_files [audio_files ...]

Transcribe audio files using Whisper models.

positional arguments:
  audio_files           Audio file(s) to transcribe

options:
  -h, --help            show this help message and exit
  --dry-run             Simulate processing without writing files
  --model {tiny,base,small,medium,large,turbo,tiny.en,base.en,small.en,medium.en}
                        Specify the Whisper model to use (by name)
  --timestamps {y,n,b}  Timestamp option: y=timestamps only, n=no
                        timestamps, b=both
```

### Output

The script outputs one or multiple text file(s) containing the transcribed content. The file is named after the input audio file, replacing its extension with `.txt` for without timestamps text (e.g., `example_audio.m4a` becomes `example_audio.txt`) and `_timestamps.txt` with timestamps text.

## Notes

- Ensure the audio file exists at the specified path.
- The script uses Whisper models, so make sure you have sufficient resources (VRAM) for the selected model size.

## Troubleshooting

- **File not found:** Ensure the correct path to the audio file is provided.
- **Invalid input:** Enter a valid number when choosing a model.
- **Dry run mode:** No transcription is performed, and the script only simulates the steps.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
