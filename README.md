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

## 🔄 Algoritmos

| Algoritmo | Encargado | Descripción | Estado |
|-----------|-----------|-------------|--------|
| Algoritmo 1 | David Luna | Calculadora simple | ✅ Actualizado según sugerencias |
| Algoritmo 2 | David Aragundy | Fibonacci iterativo | 🔄 En revisión de diseño |
| Algoritmo 3 | Gabriela Jiménez | Ordenamiento burbuja | ✅ Completado |

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.



