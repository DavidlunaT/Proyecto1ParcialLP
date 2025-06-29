<div align="center">

# 🎯 Analizador Léxico, Sintáctico y Semántico para C#

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PLY](https://img.shields.io/badge/PLY-4.0-green.svg)](https://www.dabeaz.com/ply/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📋 Contenido

- [Instalación](#-instalación)
- [Uso](#-uso)
- [Equipo](#-equipo)
- [Características](#-características)
- [Ejemplos](#-ejemplos)

## 🚀 Instalación

### Prerrequisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Proyecto1ParcialLP
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # Crear entorno
   python -m venv venv

   # Activar entorno
   # Windows (Git Bash)
   source venv/Scripts/activate
   # Windows (CMD)
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. **Ejecutar analizador léxico**
   ```bash
   python lex.py
   ```

2. **Ejecutar analizador sintáctico y semántico**
   ```bash
   python yacc.py
   ```

## 👥 Equipo

### Estructuras de Datos

| Miembro | Responsabilidad | Descripción |
|---------|----------------|-------------|
| David Aragundy | Arrays | Declaración, inicialización y acceso |
| David Luna | Listas | Manejo de listas dinámicas |
| Gabriela Jiménez | Diccionarios | Implementación de Dictionary<K,V> |

### Análisis Semántico

| Miembro | Responsabilidad | Descripción |
|---------|----------------|-------------|
| David Aragundy | Compatibilidad | Validación de tipos en operaciones |
| David Luna | Asignaciones | Verificación de tipos en asignaciones |
| Gabriela Jiménez | Control | Validación de condiciones booleanas |

## ✨ Características

### Análisis Léxico
- 🔍 79 palabras reservadas de C#
- 🎯 27 palabras clave contextuales
- 🔢 Soporte para literales numéricos avanzados
- 📝 Manejo de cadenas y caracteres

### Análisis Sintáctico
- 🏗️ Construcción de AST
- 📊 Estructuras de control
- 📦 Declaraciones de variables
- 🔧 Expresiones y operaciones

### Análisis Semántico
- ✅ Validación de tipos
- 🔄 Comprobación de declaraciones
- 🚦 Validación de condiciones
- 📝 Registro detallado de errores

## 📝 Ejemplos

Encontarás ejemplos detallados en `test_errors.cs` que cubren:

- Variables no declaradas
- Compatibilidad de tipos
- Asignaciones inválidas
- Estructuras de control
- Arrays y diccionarios

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

### Resumen de cambios y mejoras

#### Cambios clave en el analizador léxico (`lex.py`):

- **Cobertura total de palabras reservadas:**  
  Se añadieron las 79 palabras reservadas y las 27 palabras clave contextuales de C#, organizadas alfabéticamente para facilitar el mantenimiento.
- **Manejo avanzado de números:**  
  Soporte para literales de punto flotante con exponentes y sufijos de tipo, enteros hexadecimales (`0x...`), binarios (`0b...`) y separadores de guion bajo.
- **Definición estricta de operadores:**  
  Se definieron los 48 operadores y signos de puntuación de C#, ordenados de mayor a menor longitud para un reconocimiento correcto, incluyendo operadores especiales como nullable y lambda.
- **Mejoras en manejo de cadenas:**  
  Soporte para cadenas verbatim (`@""`) con comillas escapadas y manejo adecuado de secuencias de escape en cadenas y caracteres.
- **Identificación de nombres de clase:**  
  Token especial `CLASS_NAME` para identificadores que inician con mayúscula, diferenciándolos de otros identificadores.
- **Manejo de comentarios:**  
  Soporte para comentarios de una y varias líneas, actualizando correctamente los números de línea.
- **Manejo de errores:**  
  Registro de errores con número de línea y omisión de caracteres inválidos sin detener el análisis.
- **Soporte Unicode:**  
  Decodificación adecuada de secuencias de escape y compatibilidad con UTF-8, cumpliendo la especificación de C#.
- **Cobertura completa:**  
  El lexer ahora reconoce todos los elementos léxicos de C#, incluyendo palabras clave, operadores, literales, comentarios, nombres de clase y manejo robusto de errores.

#### Resumen de lo agregado en el analizador sintáctico (`yacc.py`):

- **Cobertura de estructuras de C#:**  
  El parser reconoce declaraciones de variables, arreglos, listas, diccionarios, funciones (con y sin parámetros, con retorno), clases, métodos, propiedades, y estructuras de control (`if`, `else`, `while`, `for`, `switch`).
- **Soporte para expresiones complejas:**  
  Manejo de operaciones aritméticas, lógicas, acceso a arreglos y diccionarios, llamadas a funciones y métodos estáticos.

#### Análisis Semántico y Estructuras:

- **Flujo de Análisis:**
  - El análisis semántico solo se ejecuta si el sintáctico pasa sin errores
  - Se utiliza el árbol de sintaxis abstracta (AST) según la documentación de PLY
  - Los logs muestran el árbol para facilitar la depuración

- **Distribución del Trabajo:**

  **Estructuras de Datos:**
  - **Arrays:** David Aragundy
    - Declaración e inicialización de arrays
    - Acceso a elementos

  - **Listas:** David Luna
    - Manejo de listas dinámicas
    - Operaciones de lista

  - **Diccionarios:** Gabriela Jiménez
    - Implementación de Dictionary<K,V>
    - Acceso y modificación de elementos

  **Análisis Semántico:**
  - **Compatibilidad de Operaciones:** David Aragundy
    - Validación de tipos en operaciones
    - Detección de operaciones inválidas

  - **Asignaciones:** David Luna
    - Verificación de tipos en asignaciones
    - Control de inicialización de variables

  - **Estructuras de Control:** Gabriela Jiménez
    - Validación de condiciones booleanas
    - Comprobación de tipos en bucles

- **Ejemplos de Prueba:**
  Se incluyen ejemplos de cada funcionalidad en `test_errors.cs`, organizados por secciones:
  - Variables no declaradas
  - Compatibilidad de tipos en operaciones
  - Asignaciones inválidas
  - Estructuras de control (condiciones no booleanas)
  - Operaciones con arrays y diccionarios
- **Manejo de entrada/salida:**  
  Reconocimiento de instrucciones como `Console.WriteLine`, `Console.ReadLine` y conversiones de tipo (`Convert.ToInt32`).
- **Registro de errores sintácticos:**  
  Los errores se registran con detalles y se guardan en archivos de log con marca de tiempo y nombre de usuario.
- **Menú interactivo:**  
  Permite seleccionar el archivo de algoritmo a analizar y genera un log detallado del análisis sintáctico.
- **Soporte para clases y métodos públicos/estáticos:**  
  Reconocimiento de clases públicas, métodos estáticos, métodos principales (`Main`) y propiedades con `get`/`set`.
- **Extensible y modular:**  
  El parser está organizado por secciones responsables, facilitando la colaboración y el mantenimiento.

