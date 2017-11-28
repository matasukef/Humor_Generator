import os
import sys
import argparse

from img_sim.img_predict import img_sim
from word_sim.word_predict import word_sim

class img_word_sim(cnn_model_type='ResNet', lang='jp', word_dict='jp_wiki', gpu_id=-1):
    def __init__(self):
        
        self.img_model = img_sim(model=cnn_model_type, lang=lang, gpu_id=gpu_id)
        self.word_model = word_sim(word_dict=word_dict)

   def get_T


