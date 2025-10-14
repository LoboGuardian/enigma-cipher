class EnigmaMachine:
    """
    A simplified implementation of the Enigma machine cipher.
    Includes rotors, reflector, and plugboard.
    """
    
    # Historical rotor wirings (I, II, III)
    ROTORS = {
        'I':   'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'II':  'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    }
    
    # Rotor notch positions (when to turn next rotor)
    NOTCHES = {
        'I':   'Q',
        'II':  'E',
        'III': 'V',
    }
    
    # Reflector wiring (B model)
    REFLECTOR = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
    
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, rotors=['I', 'II', 'III'], positions=[0, 0, 0], 
                 ring_settings=[0, 0, 0], plugboard=None):
        """
        Initialize Enigma machine.
        
        Args:
            rotors: List of 3 rotor names (e.g., ['I', 'II', 'III'])
            positions: Starting positions for each rotor (0-25)
            ring_settings: Ring settings for each rotor (0-25)
            plugboard: Dict of letter pairs to swap (e.g., {'A': 'B', 'B': 'A'})
        """
        self.rotors = [self.ROTORS[r] for r in rotors]
        self.rotor_names = rotors
        self.positions = positions.copy()
        self.ring_settings = ring_settings
        self.plugboard = plugboard or {}
        
    def rotate_rotors(self):
        """Rotate rotors according to Enigma stepping mechanism."""
        # Check if middle rotor is at notch (double-stepping)
        if self.ALPHABET[self.positions[1]] == self.NOTCHES[self.rotor_names[1]]:
            self.positions[1] = (self.positions[1] + 1) % 26
            self.positions[2] = (self.positions[2] + 1) % 26
        # Check if right rotor is at notch
        elif self.ALPHABET[self.positions[0]] == self.NOTCHES[self.rotor_names[0]]:
            self.positions[1] = (self.positions[1] + 1) % 26
        
        # Always rotate right rotor
        self.positions[0] = (self.positions[0] + 1) % 26
    
    def pass_through_plugboard(self, char):
        """Swap characters according to plugboard settings."""
        return self.plugboard.get(char, char)
    
    def pass_through_rotor(self, char, rotor_idx, reverse=False):
        """Pass character through a rotor."""
        rotor = self.rotors[rotor_idx]
        pos = self.positions[rotor_idx]
        ring = self.ring_settings[rotor_idx]
        
        if not reverse:
            # Forward through rotor
            shift = pos - ring
            char_idx = (self.ALPHABET.index(char) + shift) % 26
            new_char = rotor[char_idx]
            return self.ALPHABET[(self.ALPHABET.index(new_char) - shift) % 26]
        else:
            # Reverse through rotor
            shift = pos - ring
            char_idx = (self.ALPHABET.index(char) + shift) % 26
            new_char = self.ALPHABET[rotor.index(self.ALPHABET[char_idx])]
            return self.ALPHABET[(self.ALPHABET.index(new_char) - shift) % 26]
    
    def pass_through_reflector(self, char):
        """Pass character through reflector."""
        return self.REFLECTOR[self.ALPHABET.index(char)]
    
    def encrypt_char(self, char):
        """Encrypt a single character."""
        if char not in self.ALPHABET:
            return char
        
        # Rotate rotors before encryption
        self.rotate_rotors()
        
        # Through plugboard
        char = self.pass_through_plugboard(char)
        
        # Through rotors (right to left)
        for i in range(3):
            char = self.pass_through_rotor(char, i, reverse=False)
        
        # Through reflector
        char = self.pass_through_reflector(char)
        
        # Back through rotors (left to right)
        for i in range(2, -1, -1):
            char = self.pass_through_rotor(char, i, reverse=True)
        
        # Through plugboard again
        char = self.pass_through_plugboard(char)
        
        return char
    
    def encrypt(self, text):
        """Encrypt a text string."""
        text = text.upper().replace(' ', '')
        result = ''
        for char in text:
            if char in self.ALPHABET:
                result += self.encrypt_char(char)
            else:
                result += char
        return result
    
    def decrypt(self, text):
        """
        Decrypt a text string.
        Due to Enigma's reciprocal nature, decryption is the same as encryption
        when using the same initial settings.
        """
        return self.encrypt(text)


# Example usage
if __name__ == "__main__":
    print("=" * 50)
    print("ENIGMA MACHINE CIPHER")
    print("=" * 50)
    
    # Setup plugboard (swap pairs of letters)
    plugboard = {
        'A': 'R', 'R': 'A',
        'G': 'K', 'K': 'G',
        'O': 'X', 'X': 'O',
    }
    
    # Create Enigma machine with specific settings
    enigma_encrypt = EnigmaMachine(
        rotors=['I', 'II', 'III'],
        positions=[0, 0, 0],  # Starting position AAA
        ring_settings=[0, 0, 0],
        plugboard=plugboard
    )
    
    # Encrypt message
    plaintext = "HELLO WORLD"
    print(f"\nPlaintext:  {plaintext}")
    ciphertext = enigma_encrypt.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt message (reset to same initial settings)
    enigma_decrypt = EnigmaMachine(
        rotors=['I', 'II', 'III'],
        positions=[0, 0, 0],  # Same starting position
        ring_settings=[0, 0, 0],
        plugboard=plugboard
    )
    
    decrypted = enigma_decrypt.decrypt(ciphertext)
    print(f"Decrypted:  {decrypted}")
    
    print("\n" + "=" * 50)
    print("ANOTHER EXAMPLE")
    print("=" * 50)
    
    # Different settings
    enigma2 = EnigmaMachine(
        rotors=['III', 'II', 'I'],
        positions=[5, 12, 3],  # Starting position FMD
        ring_settings=[1, 1, 1]
    )
    
    message = "THEQUICKBROWNFOX"
    print(f"\nPlaintext:  {message}")
    encrypted = enigma2.encrypt(message)
    print(f"Ciphertext: {encrypted}")
    
    # Decrypt with same settings
    enigma2_decrypt = EnigmaMachine(
        rotors=['III', 'II', 'I'],
        positions=[5, 12, 3],
        ring_settings=[1, 1, 1]
    )
    decrypted2 = enigma2_decrypt.decrypt(encrypted)
    print(f"Decrypted:  {decrypted2}")
    print("\n" + "=" * 50)