using System;

class BubbleSortExample
{
    static void BubbleSort(int[] array)
    {
        int n = array.Length;
        for (int i = 0; i < n - 1; i++)
        {
            for (int j = 0; j < n - i - 1; j++)
            {
                if (array[j] > array[j + 1])
                {
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
            }
        }
    }

    static void Main(string[] args)
    {
        int[] numbers = { 5, 2, 9, 1, 5, 6 };
        Console.WriteLine("Original array:");
        foreach (int num in numbers)
        {
            Console.Write(num + " ");
        }

        BubbleSort(numbers);

        Console.WriteLine("\nSorted array:");
        foreach (int num in numbers)
        {
            Console.Write(num + " ");
        }
    }
}