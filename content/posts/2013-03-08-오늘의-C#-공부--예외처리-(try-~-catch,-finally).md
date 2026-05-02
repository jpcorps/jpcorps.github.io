---
layout: post
title: "오늘의 C# 공부 : 예외처리 (try ~ catch, finally)"
date: 2013-03-08 07:35:50
categories: [이글루스 백업, "2013-03"]
---

{% raw %}
////예외처리 실습  
//using System;

//namespace TryCatch  
//{  
//    class jpcorp  
//    {  
//        static void Main(string[] args)  
//        {  
//            int[] arr = { 1, 2, 3 };

//            try  
//            {  
//                for (int i = 0; i < 5; i++)  
//                {  
//                    Console.WriteLine(arr[i]);  
//                }  
//            }

//            catch (IndexOutOfRangeException e)  
//            {  
//                Console.WriteLine("예외가 발생했지롱 : {0}", e.Message);  
//            }

//            Console.WriteLine("종료");  
//        }  
//    }  
//}

////예외 던지기  
//using System;

//namespace Throw  
//{  
//    class jpcorp  
//    {  
//        static void DoSomething(int arg)  
//        {  
//            if (arg < 10)  
//                Console.WriteLine("arg : {0}", arg);  
//            else  
//                throw new Exception("arg가 10보다 큽니다");  
//        }

//        static void Main(string[] args)  
//        {  
//            try  
//            {  
//                DoSomething(1);  
//                DoSomething(2);  
//                DoSomething(3);  
//                DoSomething(4);  
//                DoSomething(5);  
//                DoSomething(11);  
//                DoSomething(31);//예외가 발생해서 실행되지 않음.

//            }

//            catch (Exception e)  
//            {  
//                Console.WriteLine(e.Message);  
//            }  
//        }  
//    }  
//}

////try ~ catch와 finally

//using System;

//namespace Finally  
//{  
//    class jpcorp  
//    {  
//        static int Divide(int divisor, int divided)  
//        {  
//            try  
//            {  
//                Console.WriteLine("Divide() 시작");  
//                return divisor / divided;  
//            }

//            catch (DivideByZeroException e)  
//            {  
//                Console.WriteLine("Divide() 예외발생 :  0으로 나눴네  ");  
//                //throw e; //throw를 이용하는 경우가 뭔가?  : 메소드 밖으로 에러 메세지 객체인 e 를 빼기 위해서다.  
//                 //즉 0으로 나눴다는 객체를 뺀다.

//                //Console.WriteLine("Divide() 예외발생 :  0으로 나눴네  : {0}", e.Message);  
//                return 0;  
//            }

//            finally  
//            {  
//                Console.WriteLine("Divide() 끝");  
//            }  
//        }

//        static void Main(string[] args)  
//        {  
//            //try  
//            //{  
//            Console.Write("제수를 입력하세요 ");  
//            String temp = Console.ReadLine();  
//            int divisor = Convert.ToInt32(temp);

//            Console.Write("피제수를 입력하세요");  
//            temp = Console.ReadLine();  
//            int divided = Convert.ToInt32(temp);

//            Console.WriteLine(" {0}/{1} = {2}", divisor, divided, Divide(divisor, divided));  
//            //}

//            //catch (FormatException e)  
//            //{  
//            //    Console.WriteLine("에러 : ", e.Message);  
//            //}

//            //catch (DivideByZeroException e)  
//            //{  
//            //    Console.WriteLine("에러 : ", e.Message);  
//            //}

//            //finally  
//            //{  
//            //    Console.WriteLine("프로그램을 종료합니다");  
//            //}  
//        }  
//    }  
//}

////사용자 정의 예외 클래스 만들기

//using System;  
//namespace MyException  
//{  
//    class InvalidArguementException : Exception //이 부분을 어떻게 쓰는지 체크하자.   
//    {  
//        public InvalidArguementException()  
//        {  
//        }

//        public InvalidArguementException(string message)  
//            : base(message)  
//        {  
//        }

//        public object Argument  
//        {  
//            get;  
//            set;  
//        }  
//        public string Range  
//        {  
//            get;  
//            set;  
//        }  
//    }

//    class MainApp  
//    {  
//        static uint MergeARGB(uint alpha, uint red, uint green, uint blue)  
//        {  
//            uint[] args = new uint[] { alpha, red, green, blue };

//            foreach (uint arg in args)  
//            {  
//                if (arg > 255)  
//                    throw new InvalidArguementException()  
//                    {  
//                        Argument = arg,  
//                        Range = "0~255"//왜 쉼표를 쓰는가?   
//                    };  
//            }

//            return (alpha << 24 & 0xFF000000) |  
//                     (red << 16 & 0x00FF0000) |  
//                    (green << 8 & 0x0000FF00) |  
//                    (blue & 0x000000FF); //이부분 다시 체크하자.  
//        }

//        static void Main(string[] args)  
//        {  
//            try  
//            {  
//                Console.WriteLine("0x{0:X}", MergeARGB(255, 111, 111, 111));  
//                Console.WriteLine("0x{0:X}", MergeARGB(1, 65, 192, 128));  
//                Console.WriteLine("0x{0:X}", MergeARGB(0, 255, 255, 300));  
//            }

//            catch (InvalidArguementException e)  
//            {  
//                Console.WriteLine(e.Message);  
//                Console.WriteLine("Argument : {0}, Range:{1}", e.Argument, e.Range);  
//            }  
//        }  
//    }  
//}

//예외 처리 다시 생각해 보기

//using System;  
//namespace MainApp  
//{  
//    class jpcorp  
//    {  
//        static void Main(string[] args)  
//        {  
//            try  
//            {  
//                int a = 1;  
//                Console.WriteLine(3 / --a); //여기서 예외 처리가 발생한다  
//            }

//            catch (DivideByZeroException e)  
//            {  
//                Console.WriteLine(e.StackTrace);//stacktrace를 하면 어디서 문제가 발생했는지 찾아준다.   
//            }  
//        }  
//    }  
//}
{% endraw %}