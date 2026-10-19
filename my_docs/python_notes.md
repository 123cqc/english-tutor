# Python 基础笔记

## 变量与数据类型

Python 是动态类型语言，变量不需要声明类型。

常见数据类型：
- int：整数，比如 10, -5, 100
- float：浮点数，比如 3.14, -0.5
- str：字符串，比如 "hello", 'world'
- bool：布尔值，只有 True 和 False
- list：列表，比如 [1, 2, 3]
- dict：字典，比如 {"name": "Tom", "age": 18}

## 条件判断

用 if、elif、else 实现条件判断。

语法：
if 条件:
    代码块
elif 条件:
    代码块
else:
    代码块

注意：Python 用缩进表示代码块，通常用 4 个空格。

## 循环

for 循环用于遍历序列：
for i in range(5):
    print(i)

while 循环用于条件循环：
while 条件:
    代码块

break 用于跳出循环，continue 用于跳过本次循环。

## 函数

用 def 定义函数：
def add(a, b):
    return a + b

函数可以接受参数，用 return 返回结果。

## 列表

列表是有序的可变序列：
nums = [1, 2, 3]
nums.append(4)      # 添加元素
nums.remove(1)      # 删除元素
print(nums[0])      # 访问元素

## 字典

字典是键值对的集合：
person = {"name": "Tom", "age": 18}
print(person["name"])       # 访问值
person["age"] = 20          # 修改值
person["city"] = "Beijing"  # 添加键值对

## 文件读写

读文件：
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

写文件：
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("hello")

## 异常处理

用 try、except 捕获异常：
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")

## 模块导入

用 import 导入模块：
import os
from openai import OpenAI

## 常用内置函数

len()     返回长度
range()   生成数字序列
print()   打印输出
input()   接收用户输入
type()    返回数据类型