# enigma-cipher

Una implementación en Python de la máquina de cifrado Enigma M3, utilizada por la Wehrmacht alemana durante la Segunda Guerra Mundial.

![Enigma](https://img.shields.io/badge/Enigma-M3-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ⚠️ Disclaimer Histórico

Este proyecto utiliza terminología y ejemplos históricos con fines puramente educativos y de precisión histórica. Las referencias a organizaciones militares nazis (Wehrmacht, Kriegsmarine) y la inclusión de frases históricas se utilizan exclusivamente para:

- Mantener la fidelidad histórica de la implementación
- Proporcionar contexto educativo sobre la Segunda Guerra Mundial
- Demostrar el uso real de la máquina Enigma en su época

**Este proyecto condena firmemente el nazismo, el fascismo y todas las ideologías de odio.** El objetivo es preservar la historia de la criptografía y honrar el trabajo de los criptógrafos aliados que ayudaron a derrotar al régimen nazi.

## 📜 Descripción

Este proyecto recrea fielmente el funcionamiento de la legendaria máquina Enigma, incluyendo:

- **8 rotores históricos** con cableados auténticos (I, II, III, IV, V, VI, VII, VIII)
- **5 reflectores reales** (A, B, C, B-Thin, C-Thin)
- **Plugboard (Steckerbrett)** con hasta 10 pares de intercambios
- **Ring settings (Ringstellung)** configurables
- **Double-stepping mechanism** - El defecto mecánico histórico del Enigma
- Terminología alemana original

## 🚀 Características

- [X] Implementación históricamente precisa del Enigma M3
- [X] Rotores con muescas auténticas (incluidos rotores de doble muesca)
- [X] Reflectores usados por Wehrmacht y Kriegsmarine
- [X] Mecanismo de stepping correcto (incluido el double-stepping)
- [X] Configuración mediante libro de códigos estilo militar
- [X] Reciprocidad total: encriptar = desencriptar con misma configuración

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/LoboGuardian/enigma-cipher.git
cd enigma-cipher

# No se requieren dependencias externas - solo Python 3.6+
```

## 💻 Uso Básico

```python
from enigma import EnigmaMachine

# Crear máquina Enigma con configuración
enigma = EnigmaMachine(
    reflector='B',                    # Reflector B (más común)
    rotors=('I', 'II', 'III'),       # Rotores izq-medio-der
    ring_settings=(1, 1, 1),         # Ringstellung (1-26)
    initial_positions='AAA',          # Grundstellung
    plugboard_pairs='AB CD EF GH'    # Steckerbrett
)

# Encriptar mensaje
plaintext = "HELLO WORLD"
ciphertext = enigma.encrypt(plaintext)
print(f"Cifrado: {ciphertext}")

# Desencriptar (reiniciar a posición inicial)
enigma.reset()
decrypted = enigma.decrypt(ciphertext)
print(f"Descifrado: {decrypted}")
```

## 🎯 Ejemplos

### Ejemplo 1: Configuración Wehrmacht Estándar

```python
enigma = EnigmaMachine(
    reflector='B',
    rotors=('I', 'II', 'III'),
    ring_settings=(1, 1, 1),
    initial_positions='AAA',
    plugboard_pairs='AB CD EF GH IJ KL'
)

mensaje = "ATTACK AT DAWN"
cifrado = enigma.encrypt(mensaje)  # Output: "KFZAJH BU CTMV"
```

### Ejemplo 2: Configuración Kriegsmarine (Naval)

```python
enigma_naval = EnigmaMachine(
    reflector='B',
    rotors=('IV', 'V', 'VI'),        # Rotores navales
    ring_settings=(10, 5, 12),
    initial_positions='WXY',
    plugboard_pairs='AE BF CM DQ HU JN LX PR SZ VW'
)

mensaje = "THE QUICK BROWN FOX"
cifrado = enigma_naval.encrypt(mensaje)
```

### Ejemplo 3: Uso de la Interfaz de Configuración

```python
enigma = EnigmaMachine(
    reflector='C',
    rotors=('VII', 'VI', 'VIII'),
    ring_settings=(15, 20, 3),
    initial_positions='XYZ',
    plugboard_pairs='AQ BW CE DR FT GU HY IZ JX KV'
)

# Mostrar configuración actual
enigma.print_settings()

# Cambiar posición durante operación
enigma.set_positions('ABC')

# Obtener posición actual
current_pos = enigma.get_position_letters()
print(f"Posición actual: {current_pos}")
```

## 🔧 Configuración

### Reflectores Disponibles

| Reflector | Uso Histórico |
|-----------|---------------|
| A | Wehrmacht (temprano) |
| B | Wehrmacht (más común) |
| C | Wehrmacht (tardío) |
| B-Thin | Kriegsmarine M4 |
| C-Thin | Kriegsmarine M4 |

### Rotores Disponibles

| Rotor | Muesca | Uso |
|-------|--------|-----|
| I | Q | Wehrmacht estándar |
| II | E | Wehrmacht estándar |
| III | V | Wehrmacht estándar |
| IV | J | Wehrmacht/Kriegsmarine |
| V | Z | Wehrmacht/Kriegsmarine |
| VI | Z, M | Kriegsmarine (doble muesca) |
| VII | Z, M | Kriegsmarine (doble muesca) |
| VIII | Z, M | Kriegsmarine (doble muesca) |

### Parámetros de Configuración

- **reflector**: String - Nombre del reflector ('A', 'B', 'C', 'B-Thin', 'C-Thin')
- **rotors**: Tuple - 3 rotores en orden (izquierda, medio, derecha)
- **ring_settings**: Tuple - Ajuste de anillos, rango 1-26 para cada rotor
- **initial_positions**: String - Posición inicial de 3 letras (ej: 'AAA')
- **plugboard_pairs**: String - Pares de letras separados por espacio (ej: 'AB CD EF')

## 📚 Conceptos del Enigma

### Terminología Alemana

- **Umkehrwalze**: Reflector - Refleja la señal de vuelta a través de los rotores
- **Walzen**: Rotores - Discos giratorios que realizan la sustitución
- **Ringstellung**: Ring Settings - Desplazamiento del anillo del alfabeto
- **Grundstellung**: Posición Inicial - Posición de inicio de los rotores
- **Steckerbrett**: Plugboard - Panel de intercambio de letras
- **Klartext**: Texto Plano - Mensaje sin cifrar
- **Geheimtext**: Texto Cifrado - Mensaje encriptado

### ¿Cómo Funciona?

1. **Antes de cada letra**: Los rotores avanzan según el mecanismo de stepping
2. **Entrada**: La letra pasa por el plugboard
3. **Rotores (→)**: La señal atraviesa los 3 rotores de derecha a izquierda
4. **Reflector**: La señal se refleja (¡por eso Enigma es recíproco!)
5. **Rotores (←)**: La señal regresa por los 3 rotores de izquierda a derecha
6. **Salida**: La letra pasa nuevamente por el plugboard
7. **Resultado**: Se ilumina la letra cifrada

### Double-Stepping

El Enigma tenía un "defecto" mecánico: cuando el rotor medio alcanzaba su muesca, avanzaba dos veces seguidas (una vez solo y otra con el rotor izquierdo). Este comportamiento está correctamente implementado y fue una de las debilidades que ayudó a Alan Turing a descifrar Enigma.

## 🔐 Seguridad Histórica

### Fortalezas
- Aproximadamente 159 quintillones (159 × 10¹⁸) de configuraciones posibles
- Reciprocidad: misma configuración para cifrar y descifrar
- Cambio de clave diaria mediante libro de códigos

### Debilidades (Explotadas en Bletchley Park)
- Una letra nunca se cifra como ella misma
- El double-stepping creaba patrones predecibles
- Uso de mensajes con formato estándar (como partes meteorológicos)
- Errores humanos en la elección de configuraciones

## 🧪 Testing

```python
# Test básico de reciprocidad
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

assert original == decrypted, "¡Error en reciprocidad!"
print("✅ Test pasado: El mensaje se cifró y descifró correctamente")
```

## 📖 Historia

La máquina Enigma fue inventada por el ingeniero alemán Arthur Scherbius al final de la Primera Guerra Mundial. Durante la Segunda Guerra Mundial, fue utilizada extensivamente por las fuerzas armadas alemanas para proteger comunicaciones militares.

El criptoanálisis de Enigma por parte de los Aliados en Bletchley Park, liderado por Alan Turing, fue uno de los logros intelectuales más importantes del siglo XX y acortó significativamente la duración de la guerra.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Alan Turing y el equipo de Bletchley Park por su increíble trabajo
- Los historiadores y criptógrafos que han documentado las especificaciones técnicas del Enigma
- La comunidad de código abierto

## 📚 Referencias

- [Enigma Machine - Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine)
- [Technical Details of the Enigma Machine](https://www.cryptomuseum.com/crypto/enigma/)
- [Breaking the Enigma Code](https://www.iwm.org.uk/history/how-alan-turing-cracked-the-enigma-code)
- [The Enigma Cipher Machine](https://www.codesandciphers.org.uk/enigma/)

## ⚠️ Aviso Legal

Este proyecto es solo para fines educativos e históricos. No debe usarse para cifrado real de datos sensibles, ya que el algoritmo Enigma fue descifrado hace décadas y no es seguro según los estándares modernos.

---

**Desarrollado con fines educativos y de preservación histórica** 🎖️