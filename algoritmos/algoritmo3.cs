using System;

class FactorialCalculator
{
    static int Factorial(int n)
    {
        if (n <= 1)
        {
            return 1;
        }
        else
        {
            return n * Factorial(n - 1);
        }
    }

    static void Main(string[] args)
    {
        Console.Write("Enter a number: ");
        int number = Convert.ToInt32(Console.ReadLine());
        int result = Factorial(number);
        Console.WriteLine($"Factorial of {number} is {result}");
    }
}
