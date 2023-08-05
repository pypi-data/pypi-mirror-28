# -*- coding: utf-8 -*-



# 1
def setscore(num):
    if(num>=90):
        print("A")
    if(num>=60 and num<=89):
        print("B")
    if(num<=60):
        print("C")
        
setscore(90)        



# 2
# def setsqua(a):
#     for i in range(0,a):
#         print(" "*(a-1-i),end="")
#         print("*"*((i*2)+1))
#     
#     for i in range(a-2,-1,-1):
#         print(" "*(a-1-i),end="")
#         print("*"*((i*2)+1))
# 
# setsqua(4)



# 3
# for i in range(2,100):
#     num=i
#     buff=0
#     for j in range(2,i):
#         if(num%j==0):
#             buff=1
#             break;
#     if(buff==0):
#         print("素数:%d"%(num))





# 4
# def f(n):
#     if(n==1):
#         return 10
#     return f(n-1)+2    
# print(f(5))







# 5
# arr=[28,3,21,34,65,35,26]
# def Swaparr():
#     min=0
#     max=0
#     for i in range(0,len(arr)):
#         if(arr[max]<arr[i]):
#             max=i
#         if(arr[min]>arr[i]):
#             min=i      
#     arr[len(arr)-1],arr[min]=arr[min],arr[len(arr)-1]
#     arr[0],arr[max]=arr[max],arr[0]
# 
# 
# Swaparr()
# print(arr)



# 6
# def setlen(str):
#     print(len(str))
#         
# str=input("请输入字符串")
# setlen(str)



# 7
# person = {"li":18,"wang":50,"zhang":20,"sun":22}
# name=""
# max=0
# for i in person:
#     # print(type(person[i]))
#     if(person[i]>max):
#        name=i
#        max=person[i]
#     
# print(name+" "+str(max))





# 8
# def f(num):
#     if(num==1 or num==2):
#         return 1
#     return f(num-1)+f(num-2)
#     
# for i in range(1,10):
#     print("%d"%f(i),end=" ")



