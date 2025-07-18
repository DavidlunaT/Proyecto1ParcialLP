using System;

class TestErrors
{
    static void Main()
    {
        // ========== ERRORES DE VARIABLES NO DECLARADAS ==========
        Console.WriteLine("=== Testing undeclared variables ===");
        
        // Variables no declaradas en expresiones
        int result1 = x + y;
        
        // Variable no declarada en comparación
        if (undeclaredVar > 5)
        {
            Console.WriteLine("This won't work");
        }
        
        // Asignación a variable no declarada
        notDeclared = 42;
        
        
        // ========== ERRORES DE COMPATIBILIDAD DE TIPOS ==========
        Console.WriteLine("=== Testing type compatibility ===");
        
        // Declaraciones correctas para las pruebas
        int number = 10;
        string text = "Hello";
        float decimal_num = 3.14f;
        bool flag = true;
        
        // Operaciones aritméticas incompatibles
        int badResult1 = number + flag;
        int badResult2 = text * number;
        float badResult3 = decimal_num / text;
        
        // Comparaciones incompatibles 
        bool badComp1 = text > number;
        bool badComp2 = flag < decimal_num;
        
        
        // ========== ERRORES DE ASIGNACIONES ==========
        Console.WriteLine("=== Testing assignment errors ===");
        
        // Asignaciones de tipos incompatibles
        int wrongInt = "not a number";
        string wrongString = 123;
        bool wrongBool = 5;
        float wrongFloat = flag;
        
        // ========== ERRORES EN ESTRUCTURAS DE CONTROL ==========
        Console.WriteLine("=== Testing control structure errors ===");
        
        // IF con condición no booleana - usando comparación válida pero con variable no declarada
        if (nonExistentVar == 10)
        {
            Console.WriteLine("Using undeclared variable in condition");
        }
        
        
        // ========== ERRORES CON ARRAYS ==========
        Console.WriteLine("=== Testing array errors ===");
        
        // Array no declarado
        int element = nonExistentArray[0];
        
        // Índice de array con tipo incorrecto
        int[] validArray = {1, 2, 3, 4, 5};
        int badElement1 = validArray[text];
        int badElement2 = validArray[flag];
        int badElement3 = validArray[decimal_num];
        
        // ========== ERRORES DE DICCIONARIOS ==========
        Console.WriteLine("=== Testing dictionary errors ===");
        
        // Declaración correcta de diccionario
        Dictionary<string, int> scores = new Dictionary<string, int>();
        
        // Error: Tipo de clave incorrecto
        scores[42] = 100;  // Error: la clave debe ser string
        
        // Error: Tipo de valor incorrecto
        scores["John"] = "A+";  // Error: el valor debe ser int
        
        // Error: Usar valor de diccionario como condición
        if (scores["John"] > 0) { }  // Error: no se puede usar int como condición
        
        // Error: Acceder a diccionario no declarado
        Dictionary<int, string> undeclaredDict;
        undeclaredDict[1] = "test";
        
        // Error: Inicialización con tipos incorrectos
        Dictionary<string, int> wrongInit = new Dictionary<string, int>();
        wrongInit[42] = "wrong";  // Error: clave debe ser string, valor debe ser int
        wrongInit["ok"] = false;  // Error: valor debe ser int
        
        // Asignación a variable no declarada
        unknownVariable = text;
        
        // ========== ERRORES CON FUNCIONES ==========
        Console.WriteLine("=== Testing function call errors ===");
        
        // Llamada a función no declarada
        UndeclaredFunction(number);
        
        
        // ========== CASOS MIXTOS COMPLEJOS ==========
        Console.WriteLine("=== Testing complex mixed errors ===");
        
        // Múltiples errores en una expresión
        int complexError = undeclaredA + undeclaredB;
        
        // Error en condición con variables no declaradas
        if (missingX > missingY)
        {
            wrongTarget = number;
        }
        
        Console.WriteLine("End of error testing");
    }
} 