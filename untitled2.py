#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:30:29 2020

@author: vincentviguie
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

var_4 = 10

var_5 = 20

var_6 = var_4 + var_5

# %% This is a code cell

num = 10


if num == 10:

    print("num is equal to 10")



print("num is not equal to 10")


print("I am now outside the if block")



# %% This is a second code cell

val_1 = 10
val_2 = 20
str_1 = "any number of arguments"
print(val_1, val_2, str_1)

# %% numpy
import numpy as np

arr_row = np.array( [[1, 2, 3]] )

# %% list
lst_1 = [1, "b", 3.0]
for index, item in enumerate(lst_1):
    print(f"The index is {index} and the item is {item}")
    
a = np.sin(np.arange(10)[:, None])
b = np.random.randn(1, 10)
