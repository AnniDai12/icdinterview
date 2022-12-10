using System;
using System.IO;
using System.IO.Pipes;

class PipeClient
{
    static void Main(string[] args)
    {
        var server = new NamedPipeServerStream("dataTransfer");

        Console.WriteLine("Waiting for connection...");
        server.WaitForConnection();

        Console.WriteLine("Connected.");
        var br = new BinaryReader(server);
        var bw = new BinaryWriter(server);

        while (true)
        {
            try
            {
                var len = (int)br.ReadUInt32();
                var str = new string(br.ReadChars(len));

                Console.WriteLine("{0}", str);

                // Replace "from client" with "from server" and send it back
                str = str.Replace("from client", "from server");

                var buf = System.Text.Encoding.ASCII.GetBytes(str);

                bw.Write((uint)buf.Length);
                bw.Write(buf);
            }
            catch (EndOfStreamException)
            {
                break;
            }
        }

        Console.WriteLine("Client disconnected.");
        server.Close();
        server.Dispose();
    }
}