#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 22:24:37 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Neighborhoods

## Opening real property data
neighborhoods = pd.read_csv("neighborhoods.csv")
neighborhoods = neighborhoods.drop(columns=["fid", "color_2", "geodata_eg", "created_da", 
                                            "last_edite", "last_edi_1", "shape_star","shape_stle", 
                                            "SHAPE__Length", "SHAPE__Area"])

