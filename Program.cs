using System;
using System.IO;
using System.IO.Pipes;

class PipeClient
{
    static void Main(string[] args)
    {
        using (NamedPipeClientStream pipeClient =
               new NamedPipeClientStream(".", "CSServer", PipeDirection.In))
        {

            // Connect to the pipe
            //Console.Write("Attempting to connect to pipe");
            pipeClient.Connect();

            Console.WriteLine("Connected to pipe.");
            Console.WriteLine("There are currently {0} pipe server instances open.", pipeClient.NumberOfServerInstances);
            
            using (StreamReader sr = new StreamReader(pipeClient))
            {
                // Display the read text
                double[] tempArray = new double[5];
                string tempString;
                int numberofValues = 0;
                Boolean endSession = false;
                while (!endSession)
                {
                    // first receive the number of values to be sent
                    numberofValues = Convert.ToInt32(sr.ReadLine());
                    if (numberofValues == 0)
                    {
                        endSession = true;
                    }
                    else
                    {
                        // receive the values
                        for (int i = 0; i < numberofValues; i++)
                        {
                            tempString = sr.ReadLine();
                            tempArray[i] = Convert.ToDouble(tempString);
                        }

                        Console.WriteLine("Received values:");
                        for (int i = 0; i < numberofValues; i++)
                        {
                            Console.WriteLine(tempArray[i]);
                        }
                        endSession = true;
                    }
                   
                }

                Console.WriteLine("Received from server: {0}", tempArray);
            }
            
            
        }
        Console.Write("Press Enter to continue");
        Console.ReadLine();
    }
    

}