from __future__ import print_function, division, unicode_literals
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import ffmpeg
import sys
from pprint import pprint 
import sidpy
from PIL import Image, ImageOps
import h5py

class AVIReader(sidpy.Reader):
    
    def  __init__(self, input_file_path, add_dict=None):
        self._input_file_path = input_file_path
        self.add_dict = add_dict
    
    def read(self):
        
        frames = []
        cap = cv2.VideoCapture(self._input_file_path)
        ret = True
        while ret:
            ret, img = cap.read() # read one frame from the 'capture' object; img is (H, W, C)
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if ret:
                frames.append(img)
        
        video = np.stack(frames, axis=0) # dimensions (T, H, W, C)    
        
         # Extract meta data embedded in the file
        parm_dict = dict()
        parm_dict = ffmpeg.probe(self._input_file_path)["streams"][0]
        
        # Extract meta data from a dictionary passed to the reader
        if self.add_dict == None:
            meta_dict = dict()
        else:
            meta_dict = self.add_dict
        
        complete_meta = {**parm_dict,**meta_dict}
        
        # Defining the dimensions of the data set
        num_frames = int(complete_meta['nb_frames'])
        video_duration  = float(complete_meta['duration'])
        time_vec = np.linspace(0, video_duration, num_frames, endpoint=True)

        x_vec = np.linspace(0, int(complete_meta['width']), int(complete_meta['width']), endpoint=True)
        y_vec = np.linspace(0, int(complete_meta['height']), int(complete_meta['height']), endpoint=True)  
        BGR = np.array([0,1,2])
        
        data_set = sidpy.Dataset.from_array(video)
        data_set.set_dimension(0, sidpy.Dimension(time_vec, name='t',units='seconds',
                                                  quantity='Time',
                                                  dimension_type='temporal'))
        data_set.set_dimension(1, sidpy.Dimension(y_vec, name='y', units='pixel',
                                                  quantity='Length',
                                                  dimension_type='spatial'))
        data_set.set_dimension(2, sidpy.Dimension( x_vec, name='x',
                                                  quantity='Length',
                                                  dimension_type='spatial'))
        data_set.set_dimension(3, sidpy.Dimension(BGR,name='Color Channel'))
                                                  

        data_set.data_type = sidpy.DataType.IMAGE_STACK
        data_set.metadata = complete_meta
        
        return data_set
    