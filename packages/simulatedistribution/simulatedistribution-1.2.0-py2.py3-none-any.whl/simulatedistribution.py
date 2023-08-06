#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:43:19 2018

@author: Christine
"""

import numpy as np

def simulate(size, distribution, parameter1, parameter2=0):    #parameter2 defaulted to zero as not required for poisson
   
    if distribution=="normal":      #uses parameter1 as mean and parameter2 as std to create samples from normal distribution
        return np.random.normal(loc=parameter1, scale=parameter2, size =size)
    
    if distribution=="poisson":      #uses parameter1 as lambda to create samples from poisson distribution
        return np.random.poisson(lam=parameter1, size=size)
    
    if distribution=="binomial":     #uses parameter1 as number of trials and parameter2 as probability of success to create samples from binomial distribution
        return np.random.binomial(parameter1, parameter2, size=size)

 