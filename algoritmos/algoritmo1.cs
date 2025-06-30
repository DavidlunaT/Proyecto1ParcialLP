using System;

class SimpleCalculator
{
    static void Main(string[] args)
    {
        Console.WriteLine("Simple Calculator - Add or Subtract");
        Console.Write("Enter first number: ");
        int num1 = Convert.ToInt32(Console.ReadLine());
        //int num1 = Convert.ToInt32(Console.ReadLine()); -> prueba de error con el semantico
        //num3 = Console.ReadLine(); 
        Console.Write("Enter second number: ");
        int num2 = Convert.ToInt32(Console.ReadLine());

        Console.Write("Choose operation (+ or -): ");
        string operation = Console.ReadLine();

        int result = 0;

        if (operation == "+")
        {
            result = num1 + num2;
        }
        else if (operation == "-")
        {
            result = num1 - num2;
        }
        else
        {
            Console.WriteLine("Invalid operation.");
            return;
        }

        Console.WriteLine("Result: " + result);
    }
}
