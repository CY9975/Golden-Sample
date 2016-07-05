# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:45:15 2016

@author: E_W7
"""

import os
stream=os.popen("speedtest-cli").read()
print(stream)


print("Complete!")
