# Enigma Machine - Historical Cipher Implementation

A faithful Python implementation of the Enigma M3 cipher machine used by the German Wehrmacht during World War II, featuring both CLI and modern Qt6 GUI interfaces.

![Enigma](https://img.shields.io/badge/Enigma-M3-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Qt6](https://img.shields.io/badge/Qt-6-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ⚠️ Historical Disclaimer

This project uses historical terminology and examples for purely educational purposes and historical accuracy. References to Nazi military organizations (Wehrmacht, Kriegsmarine) and inclusion of historical phrases are used exclusively to:

- Maintain historical fidelity of the implementation
- Provide educational context about World War II
- Demonstrate actual usage of the Enigma machine in its era

**This project firmly condemns Nazism, fascism, and all ideologies of hatred.** The goal is to preserve the history of cryptography and honor the work of Allied cryptographers who helped defeat the Nazi regime.

## 📜 Description

This project faithfully recreates the operation of the legendary Enigma machine, including:

- **8 historical rotors** with authentic wirings (I, II, III, IV, V, VI, VII, VIII)
- **5 authentic reflectors** (A, B, C, B-Thin, C-Thin)
- **Plugboard (Steckerbrett)** with up to 10 letter pair swaps
- **Ring settings (Ringstellung)** - fully configurable
- **Double-stepping mechanism** - The historical mechanical "flaw" of Enigma
- **Modern Qt6 GUI** with KDE Plasma Breeze styling
- Original German terminology

## 🚀 Features

- [X] Historically accurate Enigma M3 implementation
- [X] Rotors with authentic notches (including double-notch rotors)
- [X] Reflectors used by Wehrmacht and Kriegsmarine
- [X] Correct stepping mechanism (including double-stepping)
- [X] Military-style codebook configuration
- [X] Full reciprocity: encrypt = decrypt with same configuration
- [X] Modern Qt6 GUI with KDE Breeze dark theme
- [X] Real-time rotor position display
- [X] Input validation and error handling

## 📦 Installation

### Prerequisites

- Python 3.9 - 3.13
- Poetry (for dependency management)

### Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Setup with Poetry

```bash
# Clone the repository
git clone https://github.com/LoboGuardian/enigma-cipher.git
cd enigma-cipher

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## 💻 Quick Start

### GUI Version (Recommended)

```bash
# Method 1: Using the launcher script
poetry run python run_gui.py

# Method 2: Direct execution
poetry run python enigma_gui.py

# Method 3: After activating Poetry shell
poetry shell
python run_gui.py
```

### CLI Version (Original)

```bash
poetry run python main.py
```

## 🎨 GUI Features

### Modern KDE Plasma Interface

The GUI features a modern dark theme inspired by KDE Plasma's Breeze design:

- **KDE Breeze dark color palette** with proper contrast ratios
- **Card-style group boxes** for organized configuration
- **Real-time rotor position display** with gradient indicators
- **Native Qt6 controls** with smooth hover states
- **Professional typography** using Noto Sans and Noto Mono fonts
- **Responsive layout** with proper spacing and margins

### Machine Configuration

The GUI allows you to configure all aspects of the Enigma M3 machine:

#### Reflector (Umkehrwalze)
- Choose from: B, C, A, B-Thin, C-Thin
- Default: B (most commonly used in Wehrmacht)

#### Rotors (Walzen)
- Three rotor positions: Left, Middle, Right
- Available rotors: I, II, III, IV, V, VI, VII, VIII
- Default configuration: III, II, I (standard Wehrmacht setup)

#### Ring Settings (Ringstellung)
- Set values 1-26 for each rotor
- Left, Middle, Right ring positions
- Default: 1, 1, 1

#### Initial Position (Grundstellung)
- Three-letter starting position (e.g., "AAA", "XYZ")
- Displays current rotor positions in real-time
- Can be reset to initial values

#### Plugboard (Steckerbrett)
- Configure letter pair swaps
- Format: "AB CD EF GH IJ KL"
- Up to 10 pairs (20 letters maximum)
- Default: "AB CD EF GH IJ KL"

### Encryption/Decryption Operations

1. **Configure the machine** with your desired settings
2. **Enter your message** in the input text area
3. **Click Encrypt** to encrypt plaintext
4. **Click Decrypt** to decrypt ciphertext (same operation due to Enigma's reciprocal nature)
5. **View output** in the output text area
6. **Copy output** to clipboard with the "Copy Output" button

### Control Buttons

- **Encrypt**: Encrypts the input text
- **Decrypt**: Decrypts the input text (same as encrypt for Enigma)
- **Reset Positions**: Returns rotors to initial position
- **Copy Output**: Copies the output text to clipboard
- **Clear**: Clears both input and output fields and resets positions

## 🎯 Usage Examples

### Example 1: Basic CLI Usage

```python
from main import EnigmaMachine

# Create Enigma machine with configuration
enigma = EnigmaMachine(
    reflector='B',                    # Reflector B (most common)
    rotors=('I', 'II', 'III'),       # Rotors left-middle-right
    ring_settings=(1, 1, 1),         # Ringstellung (1-26)
    initial_positions='AAA',          # Grundstellung
    plugboard_pairs='AB CD EF GH'    # Steckerbrett
)

# Encrypt message
plaintext = "HELLO WORLD"
ciphertext = enigma.encrypt(plaintext)
print(f"Encrypted: {ciphertext}")

# Decrypt (reset to initial position)
enigma.reset()
decrypted = enigma.decrypt(ciphertext)
print(f"Decrypted: {decrypted}")
```

### Example 2: Wehrmacht Standard Configuration

```python
enigma = EnigmaMachine(
    reflector='B',
    rotors=('I', 'II', 'III'),
    ring_settings=(1, 1, 1),
    initial_positions='AAA',
    plugboard_pairs='AB CD EF GH IJ KL'
)

message = "ATTACK AT DAWN"
encrypted = enigma.encrypt(message)  # Output: "KFZAJH BU CTMV"
```

### Example 3: Kriegsmarine (Naval) Configuration

```python
enigma_naval = EnigmaMachine(
    reflector='B',
    rotors=('IV', 'V', 'VI'),        # Naval rotors
    ring_settings=(10, 5, 12),
    initial_positions='WXY',
    plugboard_pairs='AE BF CM DQ HU JN LX PR SZ VW'
)

message = "THE QUICK BROWN FOX"
encrypted = enigma_naval.encrypt(message)
```

### Example 4: GUI Workflow

#### Sender (Alice):
1. Launch GUI: `poetry run python run_gui.py`
2. Configure machine with agreed settings
3. Set initial position to "XYZ"
4. Enter message: "ATTACK AT DAWN"
5. Click "Encrypt"
6. Send encrypted text to Bob

#### Receiver (Bob):
1. Launch GUI with **same settings** as Alice
2. Set initial position to "XYZ" (same as Alice)
3. Enter encrypted text
4. Click "Decrypt"
5. Read original message: "ATTACK AT DAWN"

## 🔧 Configuration

### Available Reflectors

| Reflector | Historical Use |
|-----------|----------------|
| A | Wehrmacht (early) |
| B | Wehrmacht (most common) |
| C | Wehrmacht (late) |
| B-Thin | Kriegsmarine M4 |
| C-Thin | Kriegsmarine M4 |

### Available Rotors

| Rotor | Notch | Usage |
|-------|-------|-------|
| I | Q | Wehrmacht standard |
| II | E | Wehrmacht standard |
| III | V | Wehrmacht standard |
| IV | J | Wehrmacht/Kriegsmarine |
| V | Z | Wehrmacht/Kriegsmarine |
| VI | Z, M | Kriegsmarine (double-notch) |
| VII | Z, M | Kriegsmarine (double-notch) |
| VIII | Z, M | Kriegsmarine (double-notch) |

### Configuration Parameters

- **reflector**: String - Reflector name ('A', 'B', 'C', 'B-Thin', 'C-Thin')
- **rotors**: Tuple - 3 rotors in order (left, middle, right)
- **ring_settings**: Tuple - Ring adjustment, range 1-26 for each rotor
- **initial_positions**: String - 3-letter initial position (e.g., 'AAA')
- **plugboard_pairs**: String - Letter pairs separated by space (e.g., 'AB CD EF')

## 📚 Enigma Concepts

### German Terminology

- **Umkehrwalze**: Reflector - Reflects the signal back through the rotors
- **Walzen**: Rotors - Rotating discs that perform substitution
- **Ringstellung**: Ring Settings - Alphabet ring offset
- **Grundstellung**: Initial Position - Starting position of the rotors
- **Steckerbrett**: Plugboard - Letter swap panel
- **Klartext**: Plaintext - Unencrypted message
- **Geheimtext**: Ciphertext - Encrypted message

### How It Works

1. **Before each letter**: Rotors advance according to stepping mechanism
2. **Input**: Letter passes through plugboard
3. **Rotors (→)**: Signal traverses 3 rotors from right to left
4. **Reflector**: Signal is reflected (why Enigma is reciprocal!)
5. **Rotors (←)**: Signal returns through 3 rotors from left to right
6. **Output**: Letter passes through plugboard again
7. **Result**: Encrypted letter is displayed

### Double-Stepping

Enigma had a mechanical "flaw": when the middle rotor reached its notch, it would step twice in succession (once alone and once with the left rotor). This behavior is correctly implemented and was one of the weaknesses that helped Alan Turing break Enigma.

## 🔐 Historical Security

### Strengths
- Approximately 159 quintillion (159 × 10¹⁸) possible configurations
- Reciprocity: same configuration for encrypt and decrypt
- Daily key change via codebook

### Weaknesses (Exploited at Bletchley Park)
- A letter never encrypts to itself
- Double-stepping created predictable patterns
- Use of standard format messages (like weather reports)
- Human errors in choosing configurations

## 🧪 Testing

```python
# Basic reciprocity test
enigma1 = EnigmaMachine(
    reflector='B',
    rotors=('I', 'II', 'III'),
    ring_settings=(1, 1, 1),
    initial_positions='AAA',
    plugboard_pairs='AB CD'
)

original = "TESTMESSAGE"
encrypted = enigma1.encrypt(original)

enigma1.reset()
decrypted = enigma1.decrypt(encrypted)

assert original == decrypted, "Reciprocity error!"
print("✅ Test passed: Message encrypted and decrypted correctly")
```

## 🛠️ Troubleshooting

### GUI doesn't start
- Ensure Poetry environment is activated: `poetry shell`
- Check that PySide6 is installed: `poetry show pyside6`
- Verify Python version: `python --version` (should be 3.9-3.13)

### "poetry: command not found"
Install Poetry first:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Display issues
- Try different Qt styles (the app uses Fusion by default)
- Ensure your system has Qt6 libraries installed

### Configuration errors
- Verify rotor selections are unique or allowed combinations
- Check that initial position contains only letters A-Z
- Ensure ring settings are within 1-26 range
- Validate plugboard pairs use unique letters

### Import errors
```bash
# Make sure you're in the project directory
cd enigma-cipher

# Ensure virtual environment is set up
poetry install
```

## 📁 Project Structure

```
enigma-cipher/
├── main.py              # Core Enigma machine implementation (CLI)
├── main_simple.py       # Simplified CLI version
├── enigma_gui.py        # Qt6 GUI implementation (KDE Breeze style)
├── run_gui.py           # GUI launcher script
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Locked dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

## 📖 History

The Enigma machine was invented by German engineer Arthur Scherbius at the end of World War I. During World War II, it was used extensively by German armed forces to protect military communications.

The cryptanalysis of Enigma by the Allies at Bletchley Park, led by Alan Turing, was one of the most important intellectual achievements of the 20th century and significantly shortened the duration of the war.

## 🤝 Contributing

Contributions are welcome. To improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🎯 Development

To modify the GUI:

1. Edit `enigma_gui.py`
2. Test changes: `poetry run python run_gui.py`
3. The core Enigma logic is in `main.py` (EnigmaMachine class)

### GUI Customization

The GUI uses Qt6 stylesheets for theming. To modify the appearance:

- Edit the `apply_kde_breeze_theme()` method in `enigma_gui.py`
- Adjust color values in the CSS-like stylesheet
- Modify widget layouts in the `create_*_section()` methods

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- Alan Turing and the Bletchley Park team for their incredible work
- Historians and cryptographers who documented Enigma's technical specifications
- The open-source community
- Qt/PySide6 developers for the excellent GUI framework

## 📚 References

- [Enigma Machine - Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine)
- [Technical Details of the Enigma Machine](https://www.cryptomuseum.com/crypto/enigma/)
- [Breaking the Enigma Code](https://www.iwm.org.uk/history/how-alan-turing-cracked-the-enigma-code)
- [The Enigma Cipher Machine](https://www.codesandciphers.org.uk/enigma/)
- [Bletchley Park](https://bletchleypark.org.uk/)
- [Alan Turing and Code Breaking](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma)

## ⚠️ Security Notice

This is an **educational implementation** of a historical cipher machine. The Enigma cipher was broken during WWII and provides **no security** for modern communications. Do not use for actual secure communications - use modern cryptographic standards instead.

This implementation is for historical and educational purposes only.

---

**Developed for educational purposes and historical preservation** 🎖️
