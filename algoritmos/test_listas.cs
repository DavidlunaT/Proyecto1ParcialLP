using System;
using System.Collections.Generic;

public class TestListas
{
    public static void Main()
    {
        // Declaración e inicialización de listas
        List<int> numeros = new List<int>();
        List<string> nombres = new List<string>{"Juan", "María", "Pedro"};
        List<int> valores = new List<int>(numeros);
        
        // Operaciones básicas con listas
        numeros.Add(10);
        numeros.Add(20);
        numeros.Add(30);
        
        // Acceso a elementos
        int primerElemento = numeros[0];
        Console.WriteLine(primerElemento);
        
        // Propiedades de lista
        int cantidad = numeros.Count;
        Console.WriteLine(cantidad);
        
        // Verificar si contiene un elemento
        bool contiene = numeros.Contains(20);
        if (contiene)
        {
            Console.WriteLine("La lista contiene el número 20");
        }
        
        // Remover elementos
        numeros.Remove(10);
        numeros.RemoveAt(0);
        
        // Insertar en posición específica
        numeros.Insert(0, 5);
        
        // Buscar índice de elemento
        int indice = numeros.IndexOf(30);
        
        // Limpiar lista
        nombres.Clear();
        
        // Recorrer lista
        foreach (int num in numeros)
        {
            Console.WriteLine(num);
        }
    }
}
