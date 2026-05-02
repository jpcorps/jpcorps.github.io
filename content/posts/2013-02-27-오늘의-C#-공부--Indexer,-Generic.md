---
title: "오늘의 C# 공부 : Indexer, Generic"
date: 2013-02-27T07:32:28Z
draft: false
---

////인덱서

//using System;  
//using System.Collections;

//namespace Indexer  
//{  
//    class MyList  
//    {  
//        private int[] array;  
          
//        public MyList()  
//        {  
//            array = new int[3];  
//        }  
          
//        public int this[int index]  
//        {  
//            get  
//            {  
//                return array[index];  
//            }

//            set  
//            {  
//                if (index >= array.Length)  
//                {  
//                    Array.Resize<int>(ref array, index + 1);  
//                    Console.WriteLine ("Array Resized : {0}",array.Length);  
//                }

//                array[index] = value;  
//            }  
//        }

//        public int Length  
//        {  
//            get   
//            {  
//                return array.Length;  
//            }  
//        }  
//    }

//    class jpcorp  
//    {  
//        static void Main(string[] args)  
//        {  
//            MyList list = new MyList();

//            for (int i = 0; i < 5; i++)  
//            {  
//                list[i] = i;  
//            }

//            for (int i = 0; i < list.Length; i++)  
//            {  
//                Console.WriteLine(list[i]);  
//            }  
//        }  
//    }  
//}

////foreach가 가능한 객체를 만들어 보자

//using System;  
//using System.Collections;

//namespace Enumerable  
//{  
//    class MyList : IEnumerable, IEnumerator  
//    {  
//        private int[] array;  
//        int position = -1;

//        public MyList()  
//        {  
//            array = new int[3];  
//        }

//        public int this[int index]  
//        {  
//            get  
//            {  
//                return array[index];  
//            }

//            set  
//            {  
//                if (index >= array.Length)  
//                {  
//                    Array.Resize<int>(ref array, index + 1);  
//                    Console.WriteLine("Array Resized : {0}", array.Length);  
//                }

//                array[index] = value;  
//            }  
//        }

//        public object Current  
//        {  
//            get  
//            {  
//                return array[position];  
//            }  
//        }

//        public bool MoveNext()  
//        {  
//            if (position == array.Length -1)  
//            {  
//                Reset();  
//                return false;  
//            }

//            position++;  
//            return (position < array.Length);  
//        }

//        public void Reset()  
//        {  
//            position = -1;  
//        }

//        public IEnumerator GetEnumerator()  
//        {  
//            for (int i = 0; i < array.Length; i++)  
//            {  
//                yield return (array[i]);  
//            }  
//        }

//        class jpcorp  
//        {  
//            static void Main(string[] args)  
//            {  
//                MyList list = new MyList();

//                for (int i = 0 ; i<5 ; i++)  
//                list[i] = i;

//                foreach ( int e in list)  
//                    Console.WriteLine(e);

//            }  
//        }

//    }  
//}

////일반화 프로그래밍

//using System;  
//namespace CopyingArray  
//{  
//    class jpcorp  
//    {  
//        static void CopyArray<T>(T[] source, T[] target)  
//        {  
//            for (int i = 0; i < source.Length; i++)  
//            {  
//                target[i] = source[i];  
//            }  
//        }

//        static void Main(string[] args)  
//        {  
//            int[] source = { 1, 2, 3, 4, 5 };  
//            int[] target = new int[source.Length];

//            CopyArray<int>(source, target);

//            foreach (int element in target)  
//                Console.WriteLine(element);

//            string[] source2 = { "하나", "둘", "셋", "넷", "다섯" };  
//            string[] target2 = new string[source2.Length];

//            CopyArray<string>(source2, target2);

//            foreach (string element in target2)  
//                Console.WriteLine(element);  
//        }

//    }  
//}

////일반화 클래스   
//using System;

//namespace Generic  
//{  
//    class MyList<T>  
//    {  
//        private T[] array;

//        public MyList()  
//        {  
//            array = new T[3];  
//        }

//        public T this[int index]  
//        {  
//            get  
//            {  
//                return array[index];  
//            }

//            set  
//            {  
//                if (index >= array.Length)  
//                {  
//                    Array.Resize<T>(ref array, index + 1);  
//                    Console.WriteLine("Array Resized : {0}", array.Length);  
//                }

//                array[index] = value;  
//            }  
//        }

//        public int Length  
//        {  
//            get { return array.Length; }  
//        }  
//    }

//    class jpcorp  
//    {  
//        static void Main(string[] args)  
//        {  
//            MyList<string> str\_list = new MyList<string>();

//            str\_list[0] = "abc";  
//            str\_list[1] = "def";  
//            str\_list[2] = "ghi";  
//            str\_list[3] = "jkl";  
//            str\_list[4] = "mno";

//            for (int i = 0; i < str\_list.Length; i++)  
//                Console.WriteLine(str\_list[i]);

//            Console.WriteLine();

//            MyList<int> int\_list = new MyList<int>();

//            int\_list[0] = 0;  
//            int\_list[1] = 1;  
//            int\_list[2] = 2;  
//            int\_list[3] = 3;  
//            int\_list[4] = 4;  
//            int\_list[5] = 5;

//            for (int i = 0; i < int\_list.Length; i++)  
//                Console.WriteLine(int\_list[i]);  
//        }

//    }  
//}

//// 형식 매개 변수 예약하기

//using System;  
//namespace ConstraintsOnTypeParameters  
//{  
//    class StructArray<T> where T : struct  
//    {  
//        public T[] Array{get;set;}  
//        public StructArray(int size)  
//        {  
//            Array = new T[size];  
//        }  
//    }

//    class RefArray<T> where T : class  
//    {  
//        public T[] Array { get; set; }  
//        public RefArray(int size)  
//        {  
//            Array = new T[size];  
//        }  
//    }

//    class Base { }  
//    class Derived : Base { }  
//    class BaseArray<U> where U : Base  
//    {  
//        public U[] Array { get; set; }  
//        public BaseArray(int size)  
//        {  
//            Array = new U[size];  
//        }

//        public void CopyArray<T> ( T[] Source) where T : U  
//        {  
//            Source.CopyTo(Array, 0);  
//        }  
              
//    }

//    class MainApp  
//    {  
//        public static T CreateInstance<T>() where T : new()  
//        {  
//            return new T();  
//        }

//        static void Main(string[] args)  
//        {  
//            StructArray<int> a = new StructArray<int>(3);  
//            a.Array[0] = 0;  
//            a.Array[1] = 1;  
//            a.Array[2] = 2;

//            RefArray<StructArray<double>> b = new RefArray<StructArray<double>>(3);  
//            b.Array[0] = new StructArray<double>(5);  
//            b.Array[1] = new StructArray<double>(10);  
//            b.Array[2] = new StructArray<double>(1005);

//            BaseArray<Base> c = new BaseArray<Base>(3);  
//            c.Array[0] = new Base();  
//            c.Array[1] = new Derived();  
//            c.Array[2] = CreateInstance<Base>();

//            BaseArray<Derived> d = new BaseArray<Derived>(3);  
//            d.Array[0] = new Derived();  
//            d.Array[1] = CreateInstance<Derived>();  
//            d.Array[2] = CreateInstance<Derived>();

//            BaseArray<Derived> e = new BaseArray<Derived>(3);  
//            e.CopyArray<Derived>(d.Array);  
//        }  
//    }  
//}

////일반화 컬렉션  
////List<T>

//using System;  
//using System.Collections.Generic;

//namespace UsingGenericList  
//{  
//    class MainApp  
//    {  
//        static void Main(string[] args)  
//        {  
//            List<int> list = new List<int>();  
//            for (int i = 0; i < 5; i++)  
//                list.Add(i);

//            foreach (int element in list)  
//                Console.Write("{0} ", element);  
//            Console.WriteLine();

//            list.RemoveAt(2);

//            foreach (int element in list)  
//                Console.Write("{0} ", element);  
//            Console.WriteLine();

//            list.Insert(2, 2);

//            foreach (int element in list)  
//                Console.Write("{0} ", element);  
//            Console.WriteLine();  
//        }  
//    }  
//}

////Queue<T>

//using System;  
//using System.Collections.Generic;

//namespace UsingGenericQueue  
//{  
//    class MainApp  
//    {  
//        static void Main(string[] args)  
//        {  
//            Queue<int> queue = new Queue<int>();

//            queue.Enqueue(1);  
//            queue.Enqueue(2);  
//            queue.Enqueue(3);  
//            queue.Enqueue(4);  
//            queue.Enqueue(5);

//            while (queue.Count > 0)  
//                Console.WriteLine("{0}", queue.Dequeue());  
//        }  
//    }  
//}