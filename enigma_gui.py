"""
Qt6 GUI Interface for Enigma Machine Cipher (Historical Enigma M3 Wehrmacht model interface)
This file contains the modern PySide6 (Qt6) GUI implementation with refined aesthetics
and input validation.
It requires a 'main.py' file with an 'EnigmaMachine' class to function.
"""

import re
import sys

from PySide6.QtCore import QRegularExpression, Qt, Signal
from PySide6.QtGui import QFont, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# --- CORRECTED IMPORT BLOCK ---
try:
    # Attempt to import the EnigmaMachine class from the main logic file
    from main import EnigmaMachine
except ImportError:
    # If main.py is missing or the import fails, the stub from the request is used as a fallback.
    # This prevents the GUI from crashing if the logic file isn't correctly structured.
    print(
        "Warning: Could not import EnigmaMachine from 'main.py'. Using stub for simulation."
    )

    class EnigmaMachine:
        def __init__(
            self, reflector, rotors, ring_settings, initial_positions, plugboard_pairs
        ):
            self._position = list(initial_positions.upper())
            self.initial_positions = initial_positions.upper()

        def encrypt(self, text):
            # Simple shifting stub: just shifts the letter by the rightmost rotor's position
            encrypted = ""
            # In the real main.py, positions are [L, M, R]. We use the R index (2)
            R_idx = 2

            for char in text.upper():
                if "A" <= char <= "Z":
                    # Simple shift based on the right rotor's current position (stub)
                    current_pos_int = ord(self._position[R_idx]) - ord("A")
                    shifted_char = chr(
                        ((ord(char) - ord("A") + current_pos_int) % 26) + ord("A")
                    )
                    encrypted += shifted_char
                    # Rotate the right rotor (stub)
                    self._position[R_idx] = chr(
                        ((ord(self._position[R_idx]) - ord("A") + 1) % 26) + ord("A")
                    )
                else:
                    encrypted += char
            return encrypted.replace(" ", "")

        def decrypt(self, text):
            # Reciprocal cipher logic (stub)
            return self.encrypt(text)

        def reset(self):
            self._position = list(self.initial_positions)

        def get_position_letters(self):
            return "".join(self._position)
# ------------------------------


class EnigmaGUI(QMainWindow):
    """Main GUI window for the Enigma Machine, using a modern dark theme."""

    # Enigma M3 Rotor and Reflector Constants
    ROTOR_OPTIONS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    REFLECTOR_OPTIONS = ["B", "C", "A", "B-Thin", "C-Thin"]

    # Custom signal for configuration changes
    config_changed = Signal()

    def __init__(self):
        super().__init__()
        self.enigma: EnigmaMachine | None = None
        self.init_ui()
        # Connect the custom signal to machine creation
        self.config_changed.connect(self.create_enigma_machine)
        self.create_enigma_machine()  # Initial creation

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Enigma M3 Simulator")
        self.setMinimumSize(950, 750)

        # Placeholder icon (assuming no external file access)
        self.setWindowIcon(QIcon("enigma_icon.png"))

        self.apply_modern_dark_theme()

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # Header Title
        title_label = QLabel("ENIGMA M3")
        title_font = QFont("Segoe UI", 28, QFont.ExtraBold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Wehrmacht Cipher Simulation")
        subtitle_font = QFont("Segoe UI", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Configuration Section (2 rows of configurations)
        config_group = self.create_configuration_section()
        main_layout.addWidget(config_group)

        # Rotor Display and Interaction
        rotor_display_group = self.create_rotor_display()
        main_layout.addWidget(rotor_display_group)

        # Input/Output Section
        io_group = self.create_io_section()
        main_layout.addWidget(io_group, 1)

        # Control Buttons
        button_layout = self.create_button_section()
        main_layout.addLayout(button_layout)

        # Status bar
        self.statusBar().setStyleSheet("background-color: #252526; color: #d4d4d4;")
        self.statusBar().showMessage("Ready. Configure your machine settings.", 5000)

    def apply_modern_dark_theme(self):
        """Apply a modern, flattened dark theme stylesheet."""
        self.setStyleSheet("""
            /* Base Colors */
            :root {
                --bg-primary: #1e1e1e; /* Darkest background */
                --bg-secondary: #252526; /* Group box background */
                --text-primary: #d4d4d4;
                --accent-color: #007acc; /* VS Code blue/Highlight */
                --rotor-color: #ffcc00; /* Enigma yellow/gold */
            }

            QWidget {
                background-color: var(--bg-primary);
                color: var(--text-primary);
                font-family: "Segoe UI", monospace;
                font-size: 13px;
            }
            QMainWindow { background-color: var(--bg-primary); }

            /* Group Boxes (Containers) */
            QGroupBox {
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                margin-top: 1.5ex;
                background-color: var(--bg-secondary);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: var(--text-primary);
                font-weight: 600;
            }

            /* Inputs (LineEdit, TextEdit, ComboBox, SpinBox) */
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background-color: #333333;
                color: var(--text-primary);
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: var(--accent-color);
            }

            /* Buttons */
            QPushButton {
                background-color: #4a4a4a;
                color: var(--text-primary);
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 10px 15px;
                min-height: 35px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #555555; }
            QPushButton:pressed { background-color: #3a3a3a; }

            /* Accent Button (e.g., Encrypt) */
            #EncryptButton {
                background-color: var(--accent-color);
                border: none;
                font-weight: bold;
            }
            #EncryptButton:hover { background-color: #008fec; }
            #EncryptButton:pressed { background-color: #006bbd; }

            /* Special Rotor Display Labels */
            #RotorLabel {
                padding: 5px;
                border: 3px solid var(--rotor-color);
                border-radius: 6px;
                background-color: #333;
                color: var(--rotor-color);
                font-weight: 900;
                min-width: 50px;
            }
        """)

    def create_configuration_section(self):
        """Create the configuration group box for rotors, ring settings, and plugboard."""
        group = QGroupBox("Machine Configuration")
        layout = QGridLayout()

        # --- Row 1: Reflector and Rotor Order (L, M, R) ---
        layout.addWidget(QLabel("Reflector (UKW):"), 0, 0)
        self.reflector_combo = QComboBox()
        self.reflector_combo.addItems(self.REFLECTOR_OPTIONS)
        self.reflector_combo.currentTextChanged.connect(self.config_changed.emit)
        layout.addWidget(self.reflector_combo, 0, 1)

        layout.addWidget(QLabel("Left Rotor:"), 1, 0)
        self.rotor_left = QComboBox()
        self.rotor_left.addItems(self.ROTOR_OPTIONS)
        self.rotor_left.setCurrentText("III")
        self.rotor_left.currentTextChanged.connect(self.config_changed.emit)
        layout.addWidget(self.rotor_left, 1, 1)

        layout.addWidget(QLabel("Middle Rotor:"), 2, 0)
        self.rotor_middle = QComboBox()
        self.rotor_middle.addItems(self.ROTOR_OPTIONS)
        self.rotor_middle.setCurrentText("II")
        self.rotor_middle.currentTextChanged.connect(self.config_changed.emit)
        layout.addWidget(self.rotor_middle, 2, 1)

        layout.addWidget(QLabel("Right Rotor:"), 3, 0)
        self.rotor_right = QComboBox()
        self.rotor_right.addItems(self.ROTOR_OPTIONS)
        self.rotor_right.setCurrentText("I")
        self.rotor_right.currentTextChanged.connect(self.config_changed.emit)
        layout.addWidget(self.rotor_right, 3, 1)

        # --- Row 2: Ring Settings and Plugboard ---

        # Ring Settings (Ringstellung)
        layout.addWidget(QLabel("Ring Settings (1-26):"), 0, 2)
        ring_layout = QHBoxLayout()

        # Ring settings are L, M, R
        for i, (label_text, default_val) in enumerate(zip(["L", "M", "R"], [1, 1, 1])):
            spinbox = QSpinBox()
            spinbox.setRange(1, 26)
            spinbox.setValue(default_val)
            spinbox.valueChanged.connect(self.config_changed.emit)
            setattr(
                self, f"ring_{label_text.lower()}", spinbox
            )  # Set instance attributes

            ring_layout.addWidget(QLabel(f"{label_text}:"))
            ring_layout.addWidget(spinbox)

        layout.addLayout(ring_layout, 1, 2, 1, 2)

        # Initial Positions (Grundstellung)
        layout.addWidget(QLabel("Initial Position (LMR):"), 2, 2)
        self.initial_position = QLineEdit("AAA")
        self.initial_position.setMaxLength(3)
        # Validator: exactly 3 uppercase letters
        pos_validator = QRegularExpressionValidator(QRegularExpression("^[A-Z]{3}$"))
        self.initial_position.setValidator(pos_validator)
        self.initial_position.textChanged.connect(self.on_position_changed)
        layout.addWidget(self.initial_position, 2, 3)

        # Plugboard (Steckerbrett)
        layout.addWidget(QLabel("Plugboard (A-Z pairs, max 10):"), 3, 2)
        self.plugboard = QLineEdit("AB CD EF GH IJ KL")
        self.plugboard.setPlaceholderText("e.g., AB CD EF...")
        # Validator: Allows optional space-separated pairs of A-Z, max 10 pairs
        plug_validator = QRegularExpressionValidator(
            QRegularExpression("^([A-Z]{2}\\s?){0,10}$")
        )
        self.plugboard.setValidator(plug_validator)
        self.plugboard.setMaxLength(29)
        self.plugboard.textChanged.connect(self.config_changed.emit)
        layout.addWidget(self.plugboard, 3, 3)

        group.setLayout(layout)
        return group

    def create_rotor_display(self):
        """Create a visual display for the current rotor positions (L - M - R)."""
        group = QGroupBox("Current Rotor Position (L - M - R)")
        layout = QHBoxLayout()
        layout.setSpacing(20)

        self.rotor_pos_labels = []
        for _ in range(3):
            label = QLabel("A")
            label.setObjectName("RotorLabel")  # Used for CSS styling
            font = QFont("Roboto Mono", 24, QFont.Bold)
            label.setFont(font)
            label.setFixedSize(60, 60)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            self.rotor_pos_labels.append(label)

        layout.addStretch()

        reset_btn = QPushButton("Reset Rotor Positions")
        reset_btn.clicked.connect(self.reset_position)
        reset_btn.setToolTip(
            "Resets rotors to the configured 'Initial Position' (Grundstellung)."
        )
        layout.addWidget(reset_btn)

        group.setLayout(layout)
        return group

    def create_io_section(self):
        """Create input/output section."""
        group = QGroupBox("Cipher Operations")
        layout = QVBoxLayout()

        input_font = QFont("Roboto Mono", 12)

        # Input
        layout.addWidget(QLabel("Input Message (Plaintext / Ciphertext):"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Enter A-Z characters only. Spaces/other characters will be preserved, but all others will be ignored."
        )
        self.input_text.setMaximumHeight(180)
        self.input_text.setFont(input_font)
        layout.addWidget(self.input_text)

        # Output
        layout.addWidget(QLabel("Output Message:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(180)
        self.output_text.setFont(input_font)
        layout.addWidget(self.output_text)

        group.setLayout(layout)
        return group

    def create_button_section(self):
        """Create control buttons section."""
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.setObjectName("EncryptButton")
        self.encrypt_btn.clicked.connect(self.encrypt_message)
        layout.addWidget(self.encrypt_btn, 3)  # Give more horizontal space

        self.decrypt_btn = QPushButton("Decrypt (Same Key)")
        self.decrypt_btn.clicked.connect(self.decrypt_message)
        layout.addWidget(self.decrypt_btn, 3)  # Give more horizontal space

        self.copy_btn = QPushButton("Copy Output")
        self.copy_btn.clicked.connect(self.copy_output)
        layout.addWidget(self.copy_btn, 2)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn, 1)

        return layout

    def create_enigma_machine(self):
        """Create or recreate the Enigma machine with current settings."""
        try:
            # Rotor order: (Left, Middle, Right) - This matches the internal list structure [L, M, R]
            rotors = (
                self.rotor_left.currentText(),
                self.rotor_middle.currentText(),
                self.rotor_right.currentText(),
            )

            # Ring settings order: (Left, Middle, Right) (1-26)
            ring_settings = (
                self.ring_l.value(),
                self.ring_m.value(),
                self.ring_r.value(),
            )

            # Initial position is validated for A-Z
            initial_pos = self.initial_position.text().upper().ljust(3, "A")[:3]

            # Plugboard input validation
            plugboard_pairs = self.plugboard.text().upper().replace(" ", "")
            if len(set(plugboard_pairs)) != len(plugboard_pairs):
                # Check for duplicate letters in plugboard pairs
                raise ValueError(
                    "Plugboard pairs must use unique letters (e.g., AB CD EF, not AA or AB AC)."
                )

            # Re-format plugboard pairs with spaces for consistency
            formatted_plugboard = " ".join(
                [plugboard_pairs[i : i + 2] for i in range(0, len(plugboard_pairs), 2)]
            )

            # Recreate the EnigmaMachine object
            self.enigma = EnigmaMachine(
                reflector=self.reflector_combo.currentText(),
                rotors=rotors,
                ring_settings=ring_settings,
                initial_positions=initial_pos,
                plugboard_pairs=formatted_plugboard,
            )

            self.update_position_display()
            self.statusBar().showMessage("Machine configured successfully", 3000)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Configuration Error",
                f"Error creating Enigma machine: {str(e)}\nEnsure all settings are valid, especially unique plugboard letters.",
            )
            self.enigma = None  # Mark machine as invalid
            self.statusBar().showMessage("Configuration error: Check settings", 5000)

    def on_position_changed(self, text):
        """Handle initial position text changes and emit config signal."""
        text = text.upper()

        # Keep the QLineEdit value uppercase
        if text != self.initial_position.text():
            self.initial_position.blockSignals(True)
            self.initial_position.setText(text)
            self.initial_position.blockSignals(False)

        # Recreate machine only if it's a valid 3-letter string
        if len(text) == 3 and self.initial_position.hasAcceptableInput():
            self.config_changed.emit()

    def update_position_display(self):
        """Update the rotor position display with new visual labels (L - M - R)."""
        if self.enigma:
            # get_position_letters() returns the string (L, M, R)
            position_letters = self.enigma.get_position_letters()

            if len(position_letters) == 3:
                # Labels are in L, M, R order (index 0, 1, 2)
                self.rotor_pos_labels[0].setText(position_letters[0])
                self.rotor_pos_labels[1].setText(position_letters[1])
                self.rotor_pos_labels[2].setText(position_letters[2])

    def reset_position(self):
        """Reset rotor positions to initial settings and update display."""
        if self.enigma:
            self.enigma.reset()
            self.update_position_display()
            self.statusBar().showMessage(
                "Rotor positions reset to initial setting", 2000
            )

    def encrypt_message(self):
        """Encrypt the input message."""
        if not self.enigma:
            QMessageBox.warning(
                self, "Error", "Enigma machine is not configured correctly."
            )
            return

        input_text = self.input_text.toPlainText()
        if not input_text:
            QMessageBox.warning(self, "Warning", "Please enter text to encrypt.")
            return

        # 1. Reset machine to configured initial position
        self.enigma.reset()

        try:
            # 2. Encrypt and clean output
            encrypted = self.enigma.encrypt(input_text)
            self.output_text.setPlainText(encrypted)
            self.update_position_display()

            self.statusBar().showMessage(
                f"Encryption successful. Final position: {self.enigma.get_position_letters()}",
                5000,
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Encryption Error", f"Error during operation: {str(e)}"
            )
            self.statusBar().showMessage("Encryption failed", 5000)

    def decrypt_message(self):
        """Decrypt the input message (same logic as encrypt for Enigma with the same key)."""
        if not self.enigma:
            QMessageBox.warning(
                self, "Error", "Enigma machine is not configured correctly."
            )
            return

        input_text = self.input_text.toPlainText()
        if not input_text:
            QMessageBox.warning(self, "Warning", "Please enter text to decrypt.")
            return

        # 1. Reset machine to configured initial position
        self.enigma.reset()

        try:
            # 2. Decrypt and clean output
            decrypted = self.enigma.decrypt(input_text)
            self.output_text.setPlainText(decrypted)
            self.update_position_display()

            self.statusBar().showMessage(
                f"Decryption successful. Final position: {self.enigma.get_position_letters()}",
                5000,
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Decryption Error", f"Error during operation: {str(e)}"
            )
            self.statusBar().showMessage("Decryption failed", 5000)

    def clear_all(self):
        """Clear input and output fields and reset rotor position."""
        self.input_text.clear()
        self.output_text.clear()
        self.reset_position()
        self.statusBar().showMessage("Cleared all fields and reset position", 2000)

    def copy_output(self):
        """Copy output text to clipboard."""
        output = self.output_text.toPlainText()
        if output:
            clipboard = QApplication.clipboard()
            clipboard.setText(output)
            self.statusBar().showMessage("Output copied to clipboard", 2000)
        else:
            QMessageBox.information(self, "Info", "No output to copy.")


def main():
    """Main entry point for the GUI application."""
    if "PySide6" not in sys.modules:
        print("Error: PySide6 is not imported. Ensure it is installed.")
        sys.exit(1)

    app = QApplication(sys.argv)

    # Use Fusion style for a solid cross-platform base look
    app.setStyle("Fusion")

    window = EnigmaGUI()
    window.show()

    # The use of sys.exit(app.exec()) is crucial for a PySide6 application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
