#!/usr/bin/python3

import random
import utilities

class PreProcessor:
    def __init__(self, n):
        self.n = n
    
    def split_task(self):
        return random.sample(range(10), self.n)
