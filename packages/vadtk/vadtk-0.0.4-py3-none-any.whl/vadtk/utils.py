"""
Description:
    utils module for VADKit
"""

import os
import math

from scipy.io import wavfile
import numpy as np
import resampy #TODO: from scipy import signal, signal.resample may be better


# TODO: this way of init may not be good enough 
class SpeechLabel(object):
    def __init__(self,timeLabels,**kwargs):
        self.__time_lables = timeLabels
        self.shift_time = kwargs.get('shift_time',None)
        self.frame_time = kwargs.get('frame_time',None)
        self.sample_rate = kwargs.get('sample_rate',None)
        self.sample_size = kwargs.get('sample_size',None)
        self.frame_len = None
        self.shift_len = None
        self.frames_count = None
        self.__frame_labels = None
        self.__point_labels = None
        __calculate_none_var(self)

    def __calculate_none_var(self):
        if self.frame_time == None or self.shift_time or self.sample_size == None or self.sample_rate == None:
            return
        self.frame_len = int(self.frame_time * self.sample_rate)
        self.shift_len = int(self.shift_time * self.sample_rate)
        self.frames_count = math.floor((self.sample_size - self.frame_len) / self.shift_len + 1)  # number of frames
        # calculate self.__frame_labels and self.__point_labels
        self.__frame_labels = np.zeros(self.frames_count,dtype=np.int)
        self.__point_labels = np.zeros(self.sample_size,dtype=np.int)
        for time_label in self.__time_lables:
            start_time = time_label[0]
            duration = time_label[1]
            start_frame = int(start_time / self.shift_time)
            end_frame = int(np.ceil((start_frame + duration) / self.shift_time))
            start_point = int(start_time * self.sample_rate)
            end_point = int(np.ceil((start_time + duration) * self.sample_rate))
            if start_frame >= 0 and start_frame < end_frame and end_frame < self.frames_count:
                self.__frame_labels[start_frame:end_frame] = 1
            else:
                self.__frame_labels = None
                self.__point_labels = None
                return
            if start_point >= 0 and start_point < end_point and end_point < self.sample_size:
                self.__point_labels[start_point:end_point] = 1
            else:
                self.__frame_labels = None
                self.__point_labels = None
                return

    def get_time_labels(self):
        return self.__timeLabels
    
    def get_frame_labels(self):
        return self.__frameLabels
    
    def get_point_labels(self):
        return self.__pointLabels
    
    def update(self,**kwargs):
        self.shift_time = kwargs.get('shift_time',self.shift_time)
        self.frame_time = kwargs.get('frame_time',self.frame_time)
        self.sample_rate = kwargs.get('sample_rate',self.sample_rate)
        self.sample_size = kwargs.get('sample_size',self.sample_size)
        __calculate_none_var(self)
        
def vec2frames(vec, frame_len, shift_len):
    """
    Splits signal into overlapped frames using indexing.

    Parameters:
    ----------
    vec : np.array:input vector
    frame_len : int:frame length (in samples)
    shift_len : int:frame shift (in samples)

    Returns:
    -------
    frames : np.array: the output matrix of frames

    Notes:
    -------
    Padding is not considered.
    """
    # Input validation
    if vec.size == 0 or frame_len <= 0 or shift_len <= 0:
        raise Exception('input size must be non-zero')
    assert vec.ndim == 1, 'input must be an 1-d array'

    framesNum = math.floor( (vec.size - frame_len) / shift_len + 1)  # number of frames

    # Compute index matrix
    indf = shift_len * np.arange(framesNum, dtype=np.int)[:, np.newaxis]  # indexes for frames, shape:(framesNum,1)
    inds = np.arange(frame_len, dtype=np.int)  # indexes in frame
    inds.resize((1, inds.size)) # shape:(1,frame_len)

    # using broadcast
    indexes = indf + inds # shape:(framesNum,frame_len), along the first dimension is a frame
    #indexs = index.T

    # divide the input signal into frames using indexing
    frames = vec[indexes]
    return frames

class audio(object):
    def __init__(self,src,target_fs=16000):
        if isinstance(src,audio):
            self.data = scale_vector_power_to(src.data)
            self.sample_rate = src.sample_rate
            update_power(self)
        elif isinstance(src,np.ndarray):
            self.data = scale_vector_power_to(src)
            self.sample_rate = target_fs
            update_power(self)
        elif isinstance(src,str):
            sample_rate, data = wavfile.read(src)
            # now we need to convert the data to float type, if not we may encounter the overflow problem
            data = data / np.max(np.absolute(data))
            
            if data.ndim == 2:
                # data = np.mean(data, axis=1) # we take the mean data of two channel
                data = data[:,0] # we just take the first channel
            elif data.ndim == 1:
                pass
            else:
                raise NotImplementedError('Error')
            
            if sample_rate != target_fs and target_fs > 0:
                data = resampy.resample(data,sample_rate,target_fs)
            
            data = scale_vector_power_to(data)
            self.data = data
            self.sample_rate = target_fs
            update_power(self)
        else:
            self.data = None
            self.sample_rate = None
            self.power = None
    
    def update_power(self):
        if self.data != None:
            self.power = np.sum(self.data**2) / self.data.size

    def __add__(self, other):
        if self.data == None or self.sample_rate == None or other.data == None or other.sample_rate == None:
            return audio(None)
        if self.data.size != other.data.size or self.sample_rate != other.sample_rate:
            return audio(None)
        data = self.data + other.data
        return audio(data,self.sample_rate)
    
    def add_speech(self,speech,mix_point,dB=0):
        if mix_point < 0 or mix_point + speech.data.size > self.data.size:
            return None
            # raise NotImplementedError('can not mix because the mxipoint and data size')
        if speech.sample_rate != self.sample_rate:
            return None
            # raise NotImplementedError('can not mix because the sample rate not equal')
      
        snr = 10**(dB/10.0)
        speech = scale_vector_power_to(speech.data)
        noise = scale_vector_power_to(self.data)
        noisy_speech = noise.copy()
        noisy_speech[mix_point:mix_point+speech.size] = noise[mix_point:mix_point+speech.size] + speech * np.sqrt(snr)
        return audio(noisy_speech,speech.sample_rate)
    
    def mix_speech(self,speech,dB):
        if self.data.size <= 2 * speech.data.size:
            return None
        mix_point = np.random.randint(self.data.size - speech.data.size + 1)
        return add_speech(self,speech,mix_point,dB),mix_point,speech.data.size
    
    def save(self,saveto):
        wav_ratio = 30000
        vector = scale_vector_power_to(self.data)
        vectorInt16 = vector * wav_ratio / np.max(np.absolute(vector))
        vectorInt16 = vectorInt16.astype('int16')
        wavfile.write(saveto,fs,vectorInt16)


def scale_vector_power_to(vector,desired_power=1.):
    if vector.ndim != 1:
        raise NotImplementedError("input vector should be a one dimension array")
    ori_power = np.sum(vector**2) / vector.size
    return vector / np.sqrt(desired_power/ori_power)

def prolong_vector(vector, dest_len, gap = 0):
    """
    """

    if vector.ndim != 1:
        raise NotImplementedError("input vector should be a one dimension vector")
    if gap > 0:
        gaps = np.zeros(gap);
        vector = np.append(vector,gaps)
    
    times = int(np.ceil(desLen / vector.size))
    return np.tile(vector,times)


def test():
    print("no test")


if __name__ == '__main__':        
    test();
    
