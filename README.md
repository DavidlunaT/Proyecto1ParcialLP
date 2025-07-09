# 📦 ProyectoLP

Analizador léxico, sintáctico y semántico para el lenguaje C#, desarrollado con Python, PLY y Flet.

---

## 🛠️ Instrucciones de Configuración

### 📋 Prerrequisitos

- Python 3.7 o superior instalado en tu sistema

### 💻 Pasos de Instalación

1. **Clona el repositorio** (si aún no lo has hecho):

   ```bash
   git clone <repository-url>
   cd ProyectoLP
   ```

2. **Crea un entorno virtual**:

   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual**:

   - **Windows (Git Bash)**: `source venv/Scripts/activate`
   - **Windows (Command Prompt)**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. **Instala las dependencias requeridas**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta el analizador léxico (línea de comandos)**:

   ```bash
   python lex.py
   ```

6. **Ejecuta el analizador sintáctico o semántico (línea de comandos)**:

   ```bash
   python yacc.py
   ```

7. **🚀 Ejecuta la interfaz gráfica (GUI)**:
   ```bash
   python main.py
   ```

---

## 🖥️ Interfaz Gráfica

### 🚀 Cómo usar la interfaz gráfica

1. **Selecciona un algoritmo:** Usa el dropdown para cargar algoritmos predefinidos
2. **Edita el código:** Modifica el código en el editor integrado si es necesario
3. **Ejecuta análisis:**
   - Usa botones individuales para cada análisis
   - O usa "Run All" para análisis completo
4. **Revisa resultados:** Navega entre las pestañas de resultados
5. **Consulta logs:** Ve el progreso en la sección de logs en la parte inferior

### 🔌 Desactivar el Entorno Virtual

Cuando hayas terminado de trabajar, puedes desactivar el entorno virtual:

```bash
deactivate
```

## 🧮 Algoritmos

1. **Algoritmo 1**:
   - **Encargado:** David Luna
   - **Descripción:** Este algoritmo se encarga de funcionar como una calculadora simple.
   - **Nota:** Se actualizó el algoritmo en función de las sugerencias del profesor.
2. **Algoritmo 2**:
   - **Encargado:** David Aragundy
   - **Descripción:** Este algoritmo se encarga de calcular el número de Fibonacci de forma iterativa .
   - **Nota:** Hay algunas decisiones de diseño que se tomaron que aún no están del todo claras (como la de los tokens de operadores y los tipos de datos). Agradecemos cualquier sugerencia al respecto para un diseño más eficiente.
3. **Algoritmo 3**:
   - **Encargado:** Gabriela Jiménez
   - **Descripción:** Este algoritmo se encarga de ordenar una lista de números con el algoritmo de ordenamiento por burbuja.

---

## 📈 Segundo avance

### ✨ Resumen de cambios y mejoras

#### 🔍 Cambios clave en el analizador léxico (`lex.py`):

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

#### 🔧 Resumen de lo agregado en el analizador sintáctico (`yacc.py`):

- **Cobertura de estructuras de C#:**  
  El parser reconoce declaraciones de variables, arreglos, listas, diccionarios, funciones (con y sin parámetros, con retorno), clases, métodos, propiedades, y estructuras de control (`if`, `else`, `while`, `for`, `switch`).
- **Soporte para expresiones complejas:**  
  Manejo de operaciones aritméticas, lógicas, acceso a arreglos y diccionarios, llamadas a funciones y métodos estáticos.

#### Análisis Semántico y Estructuras:

- **Flujo de Análisis:**

  - El análisis semántico solo se ejecuta si el sintáctico pasa sin errores
  - Se utiliza el árbol de sintaxis abstracta (AST) según la documentación de PLY
  - Los logs muestran el árbol para facilitar la depuración

### 👥 Distribución del Trabajo

#### Estructuras de Datos

| Componente   | Responsable      | Detalles                                                                    |
| ------------ | ---------------- | --------------------------------------------------------------------------- |
| Arrays       | David Aragundy   | • Declaración e inicialización de arrays<br>• Acceso a elementos            |
| Listas       | David Luna       | • Manejo de listas dinámicas<br>• Operaciones de lista                      |
| Diccionarios | Gabriela Jiménez | • Implementación de Dictionary<K,V><br>• Acceso y modificación de elementos |

#### Análisis Semántico

| Componente                    | Responsable      | Detalles                                                                            |
| ----------------------------- | ---------------- | ----------------------------------------------------------------------------------- |
| Compatibilidad de Operaciones | David Aragundy   | • Validación de tipos en operaciones<br>• Detección de operaciones inválidas        |
| Asignaciones                  | David Luna       | • Verificación de tipos en asignaciones<br>• Control de inicialización de variables |
| Estructuras de Control        | Gabriela Jiménez | • Validación de condiciones booleanas<br>• Comprobación de tipos en bucles          |

### 🧪 Ejemplos de Prueba

Se incluyen ejemplos de cada funcionalidad en `test_errors.cs`, organizados por secciones:

- Variables no declaradas
- Compatibilidad de tipos en operaciones
- Asignaciones inválidas
- Estructuras de control (condiciones no booleanas)
- Operaciones con arrays y diccionarios

### Manejo de entrada/salida

Reconocimiento de instrucciones como `Console.WriteLine`, `Console.ReadLine` y conversiones de tipo (`Convert.ToInt32`).

### Registro de errores sintácticos

Los errores se registran con detalles y se guardan en archivos de log con marca de tiempo y nombre de usuario.

### Menú interactivo

Permite seleccionar el archivo de algoritmo a analizar y genera un log detallado del análisis sintáctico.

### Soporte para clases y métodos públicos/estáticos

Reconocimiento de clases públicas, métodos estáticos, métodos principales (`Main`) y propiedades con `get`/`set`.

### Extensible y modular

El parser está organizado por secciones responsables, facilitando la colaboración y el mantenimiento.
