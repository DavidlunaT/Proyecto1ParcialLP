using System;

class Program
{
    static void Fibonacci(int count)
    {
        int a = 0, b = 1;
        Console.Write("Fibonacci: ");
        for (int i = 0; i < count; i++)
        {
            Console.Write(a + " ");
            int temp = a;
            a = b;
            b = temp + b;
        }
    }

    static void Main()
    {
        Fibonacci(7); // Output: 0 1 1 2 3 5 8
    }
}