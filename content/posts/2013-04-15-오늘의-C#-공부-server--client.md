---
layout: post
title: "오늘의 C# 공부 :server / client"
date: 2013-04-15 07:21:25
categories: [이글루스 백업, "2013-04"]
---

{% raw %}
/////////// server  
  
  
using System;  
using System.Diagnostics;  
using System.Net;  
using System.Net.Sockets;  
using System.Text;

namespace EchoServer  
{  
    class MainApp  
    {  
        static void Main(string[] args)  
        {  
            if (args.Length < 1)  
            {  
                Console.WriteLine("사용법 :{0} <Bind IP>", Process.GetCurrentProcess().ProcessName);  
                return;  
            }

            string bindIp = args[0];  
            const int bindfort = 5425;  
            TcpListener server = null;

            try  
            {  
                IPEndPoint localAddress =  
                    new IPEndPoint(IPAddress.Parse(bindIp), bindfort);

                server = new TcpListener(localAddress);

                server.Start();

                Console.WriteLine("메아리 서버 시작...");

                while (true)  
                {  
                    TcpClient client = server.AcceptTcpClient();  
                    Console.WriteLine("클라이언트 접속 :{0}", ((IPEndPoint)client.Client.RemoteEndPoint).ToString());

                    NetworkStream stream = client.GetStream();

                    int length;  
                    string data = null;  
                    byte[] bytes = new byte[256];

                        while ((length = stream.Read(bytes,0,bytes.Length)) != 0)  
                        {  
                            data = Encoding.Default.GetString(bytes, 0, length);  
                            Console.WriteLine (String.Format("수신{0}",data)) ;  
                            byte[] msg = Encoding.Default.GetBytes(data);  
                            stream.Write(msg, 0, msg.Length);

                            Console.WriteLine(String.Format("송신: {0}", data));  
                        }

                        stream.Close();  
                        client.Close();  
                }

            }

            catch (SocketException e)  
            {  
                Console.WriteLine(e);  
            }

            finally  
            {  
                server.Stop();  
            }

            Console.WriteLine("서버를 종료합니다");

        }  
    }  
}  
  
  
  
  
  
  
  
  
  
  
  
//////Client  
  
using System;  
using System.Diagnostics;  
using System.Net;  
using System.Net.Sockets;  
using System.Text;

namespace jpClient  
{  
    class MainApp  
    {  
        static void Main(string[] args)  
        {  
             Console.WriteLine("args={0}",args.Length);  
            if (args.Length < 4)  
            {  
                Console.WriteLine(  
                    "사용법 : {0} <Bind IP> <Bind Port><Server IP> <Message>", Process.GetCurrentProcess().ProcessName);  
                return;  
            }

            string bindIP = args[0];  
            int bindPort = Convert.ToInt32(args[1]);  
            string serverIP = args[2];  
            const int serverPort = 5425;  
            string message = args[3];

            try  
            {  
                IPEndPoint clientAddress =  
                    new IPEndPoint(IPAddress.Parse(bindIP), bindPort);  
                IPEndPoint serverAddress =  
                    new IPEndPoint(IPAddress.Parse(serverIP), serverPort);

                Console.WriteLine("클라이언트 : {0} , 서버 : {1}", clientAddress.ToString(), serverAddress.ToString());

                TcpClient client = new TcpClient(clientAddress);

                client.Connect(serverAddress);

                byte[] data = System.Text.Encoding.Default.GetBytes(message);

                NetworkStream stream = client.GetStream();

                stream.Write(data, 0, data.Length);

                Console.WriteLine("송신 :{0}", message);

                data = new byte[256];

                string responseData = "";

                int bytes = stream.Read(data, 0, data.Length);

                responseData = Encoding.Default.GetString(data, 0, bytes);

                Console.WriteLine("수신 :{0}", responseData);

                stream.Close();  
                client.Close();  
            }

            catch (SocketException e)  
            {  
                Console.WriteLine(e);  
            }

            Console.WriteLine("클라이언트를 종료합니다");

        }  
    }  
}
{% endraw %}