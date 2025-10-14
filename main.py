class EnigmaMachine:
    """
    Authentic implementation of the Enigma machine (Wehrmacht M3 model).
    Based on real historical specifications.
    """

    
    # Historical rotor wirings (actual configurations used)
    ROTORS = {
        'I':    ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
        'II':   ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
        'III':  ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
        'IV':   ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
        'V':    ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
        'VI':   ('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),  # Double notch
        'VII':  ('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),  # Double notch
        'VIII': ('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),  # Double notch
    }
    
    # Historical authentic reflectors
    REFLECTORS = {
        'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
        'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',  # Most common
        'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
        'B-Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',  # For M4
        'C-Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',  # For M4
    }
    
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, reflector='B', rotors=('I', 'II', 'III'), 
                 ring_settings=(1, 1, 1), initial_positions='AAA', 
                 plugboard_pairs=''):
        """
        Initializes the Enigma machine with historical configuration.

        Args:
            reflector: Reflector to use ('A', 'B', 'C')
            rotors: Tuple of 3 rotors (e.g., ('I', 'II', 'III'))
            ring_settings: Ringstellung - ring settings (1-26)
            initial_positions: Grundstellung - initial position (e.g., 'AAA')
            plugboard_pairs: Steckerbrett - plugboard pairs (e.g., 'AB CD EF')
        """
        if len(rotors) != 3:
            raise ValueError("Se requieren exactamente 3 rotores")
        
        self.reflector = self.REFLECTORS[reflector]
        self.reflector_name = reflector
        
        # Configure rotors (right, middle, left)
        self.rotor_wirings = []
        self.rotor_notches = []
        self.rotor_names = rotors
        
        for rotor in rotors:
            wiring, notch = self.ROTORS[rotor]
            self.rotor_wirings.append(wiring)
            self.rotor_notches.append(notch)
        
        # Ring settings (convert from 1-26 to 0-25)
        self.ring_settings = [r - 1 for r in ring_settings]
        
        # Initial positions (convert letters to numbers)
        self.positions = [self.ALPHABET.index(c) for c in initial_positions.upper()]
        self.initial_positions = self.positions.copy()
        
        # Configure plugboard (Steckerbrett)
        self.plugboard = {}
        if plugboard_pairs:
            pairs = plugboard_pairs.upper().split()
            for pair in pairs:
                if len(pair) == 2:
                    self.plugboard[pair[0]] = pair[1]
                    self.plugboard[pair[1]] = pair[0]
    
    def reset(self):
        """Resets the machine to its initial position."""
        self.positions = self.initial_positions.copy()
    
    def get_position_letters(self):
        """Returns current positions as letters."""
        return ''.join([self.ALPHABET[p] for p in self.positions])
    
    def set_positions(self, positions):
        """Sets new positions (e.g., 'XYZ')."""
        self.positions = [self.ALPHABET.index(c) for c in positions.upper()]
        self.initial_positions = self.positions.copy()
    
    def rotate_rotors(self):
        """
        Rotor stepping mechanism.
        Implements correct Enigma double-stepping.
        """
        # Right rotor (fast) - always rotates
        rotate_middle = False
        rotate_left = False
        
        # Check if middle rotor is at its notch (double-stepping)
        middle_pos_letter = self.ALPHABET[self.positions[1]]
        if middle_pos_letter in self.rotor_notches[1]:
            rotate_middle = True
            rotate_left = True
        
        # Check if right rotor is at its notch
        right_pos_letter = self.ALPHABET[self.positions[0]]
        if right_pos_letter in self.rotor_notches[0]:
            rotate_middle = True
        
        # Execute rotations
        if rotate_left:
            self.positions[2] = (self.positions[2] + 1) % 26
        if rotate_middle:
            self.positions[1] = (self.positions[1] + 1) % 26
        # Right rotor always rotates
        self.positions[0] = (self.positions[0] + 1) % 26
    
    def pass_through_plugboard(self, char):
        """Passes character through the Steckerbrett (plugboard)."""
        return self.plugboard.get(char, char)
    
    def encode_right_to_left(self, char, rotor_idx):
        """
        Encodes right to left through a rotor.
        (entry from the right side of the rotor)
        """
        rotor = self.rotor_wirings[rotor_idx]
        ring = self.ring_settings[rotor_idx]
        pos = self.positions[rotor_idx]
        
        # Apply offset for position and ring setting
        shift = pos - ring
        
        # Input
        char_pos = self.ALPHABET.index(char)
        
        # Apply shift
        char_pos = (char_pos + shift) % 26
        
        # Through rotor wiring
        char = rotor[char_pos]
        
        # Reverse shift
        char_pos = self.ALPHABET.index(char)
        char_pos = (char_pos - shift) % 26
        
        return self.ALPHABET[char_pos]
    
    def encode_left_to_right(self, char, rotor_idx):
        """
        Encodes left to right through a rotor.
        (entry from the left side of the rotor)
        """
        rotor = self.rotor_wirings[rotor_idx]
        ring = self.ring_settings[rotor_idx]
        pos = self.positions[rotor_idx]
        
        # Apply offset
        shift = pos - ring
        
        # Input
        char_pos = self.ALPHABET.index(char)
        
        # Apply shift
        char_pos = (char_pos + shift) % 26
        
        # Through rotor wiring (reverse)
        char = self.ALPHABET[rotor.index(self.ALPHABET[char_pos])]
        
        # Reverse shift
        char_pos = self.ALPHABET.index(char)
        char_pos = (char_pos - shift) % 26
        
        return self.ALPHABET[char_pos]
    
    def encode_reflector(self, char):
        """Passes character through the reflector (Umkehrwalze)."""
        char_pos = self.ALPHABET.index(char)
        return self.reflector[char_pos]
    
    def encrypt_char(self, char):
        """Encrypts a single character."""
        if char not in self.ALPHABET:
            return char
        
        # 1. Rotate rotors BEFORE encrypting
        self.rotate_rotors()
        
        # 2. Plugboard (Steckerbrett) - input
        char = self.pass_through_plugboard(char)
        
        # 3. Through rotors right to left
        char = self.encode_right_to_left(char, 0)  # Right rotor
        char = self.encode_right_to_left(char, 1)  # Middle rotor
        char = self.encode_right_to_left(char, 2)  # Left rotor
        
        # 4. Through reflector
        char = self.encode_reflector(char)
        
        # 5. Back through rotors left to right
        char = self.encode_left_to_right(char, 2)  # Left rotor
        char = self.encode_left_to_right(char, 1)  # Middle rotor
        char = self.encode_left_to_right(char, 0)  # Right rotor
        
        # 6. Plugboard (Steckerbrett) - output
        char = self.pass_through_plugboard(char)
        
        return char
    
    def encrypt(self, plaintext):
        """
        Encrypts a complete message.
        Text is converted to uppercase and spaces/special characters are removed.
        """
        plaintext = plaintext.upper()
        ciphertext = ''
        
        for char in plaintext:
            if char in self.ALPHABET:
                ciphertext += self.encrypt_char(char)
            elif char == ' ':
                ciphertext += ' '  # Keep spaces for readability
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """
        Decrypts a message.
        Due to Enigma's reciprocal nature, it's identical to encrypt().
        """
        return self.encrypt(ciphertext)
    
    def print_settings(self):
        """Displays the current machine configuration."""
        print("\n" + "="*60)
        print("CONFIGURACIÓN DE LA MÁQUINA ENIGMA")
        print("="*60)
        print(f"Reflector (Umkehrwalze):    {self.reflector_name}")
        print(f"Rotores (Walzen):           {' - '.join(self.rotor_names)}")
        print(f"                            (Izq - Med - Der)")
        print(f"Ring Settings (Ringstellung): {self.ring_settings[2]+1:02d} - {self.ring_settings[1]+1:02d} - {self.ring_settings[0]+1:02d}")
        print(f"Posición Inicial (Grundstellung): {self.get_position_letters()}")
        
        if self.plugboard:
            pairs = []
            added = set()
            for k, v in self.plugboard.items():
                if k not in added:
                    pairs.append(f"{k}{v}")
                    added.add(k)
                    added.add(v)
            print(f"Plugboard (Steckerbrett):   {' '.join(pairs)}")
        else:
            print(f"Plugboard (Steckerbrett):   (ninguno)")
        print("="*60 + "\n")


# Historical usage example
if __name__ == "__main__":
    print("\n" + "█"*60)
    print("██" + " "*56 + "██")
    print("██" + " "*17 + "ENIGMA M3" + " "*19 + "██")
    print("██" + " "*10 + "Wehrmacht Encryption Machine" + " "*10 + "██")
    print("██" + " "*56 + "██")
    print("█"*60)
    
    # Typical Wehrmacht configuration
    enigma = EnigmaMachine(
        reflector='B',
        rotors=('I', 'II', 'III'),
        ring_settings=(1, 1, 1),
        initial_positions='AAA',
        plugboard_pairs='AB CD EF GH IJ KL'
    )
    
    enigma.print_settings()
    
    # Example message
    plaintext = "HEIL HITLER"
    print(f"Mensaje original (Klartext):")
    print(f"  {plaintext}")
    print()
    
    # Encrypt
    ciphertext = enigma.encrypt(plaintext)
    print(f"Mensaje cifrado (Geheimtext):")
    print(f"  {ciphertext}")
    print(f"  Posición final de rotores: {enigma.get_position_letters()}")
    print()
    
    # To decrypt, reset to initial position
    enigma.reset()
    
    # Decrypt
    decrypted = enigma.decrypt(ciphertext)
    print(f"Mensaje desencriptado:")
    print(f"  {decrypted}")
    print(f"  Posición final de rotores: {enigma.get_position_letters()}")
    
    # Another example with different configuration
    print("\n" + "="*60)
    print("EJEMPLO 2: Configuración Naval (Kriegsmarine)")
    print("="*60 + "\n")
    
    enigma_naval = EnigmaMachine(
        reflector='B',
        rotors=('IV', 'V', 'VI'),
        ring_settings=(10, 5, 12),
        initial_positions='WXY',
        plugboard_pairs='AE BF CM DQ HU JN LX PR SZ VW'
    )
    
    enigma_naval.print_settings()
    
    message = "ATTACK AT DAWN"
    print(f"Mensaje: {message}")
    encrypted = enigma_naval.encrypt(message)
    print(f"Cifrado: {encrypted}")
    
    # Decrypt
    enigma_naval.reset()
    decrypted_naval = enigma_naval.decrypt(encrypted)
    print(f"Descifrado: {decrypted_naval}")
    
    # print("\n" + "█"*60)
    # print("██  NOTA: La seguridad del Enigma fue quebrada por       ██")
    # print("██  Alan Turing y el equipo de Bletchley Park           ██")
    # print("█"*60 + "\n")