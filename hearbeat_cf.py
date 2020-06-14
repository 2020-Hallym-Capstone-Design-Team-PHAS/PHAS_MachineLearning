# Utility
import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm


# Audio
import librosa

# tensorflow
#import tensorflow.compat.v1 as tf

# Scikit learn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Keras
#import keras
from keras.models import load_model

class HeartbeatCF():

    def __new__(self):
        dataset = []
        for folder in ["./heartbeat-sounds/set_a/**","./heartbeat-sounds/set_b/**"]:
            for filename in glob.iglob(folder):
                if os.path.exists(filename):
                    label = os.path.basename(filename).split("_")[0]
                    # skip audio smaller than 4 secs
                    if librosa.get_duration(filename=filename)>=4:
                        if label not in ["Aunlabelledtest", "Bunlabelledtest"]:
                            dataset.append({
                                "filename": filename,
                                "label": label
                                })
        dataset = pd.DataFrame(dataset)
        dataset = shuffle(dataset, random_state=42)

        train, test = train_test_split(dataset, test_size=0.2, random_state=42)

        encoder = LabelEncoder()
        encoder.fit(train.label)

        self.model_load =  load_model('my_model.h5')

        self.num_rows = 40
        self.num_columns = 173
        self.num_channels = 1

    def extract_features(audio_path):
        base_dir = './heartbeat_cf_data/'
        y, sr = librosa.load(base_dir + audio_path, duration=4)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)        
        return mfccs




    def buat_prediction(self, file_name):
        #prediction_feature = extract_features(file_name)
        base_dir = './heartbeat_cf_data/'
        y, sr = librosa.load(base_dir + file_name, duration=4)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

        mfccs = mfccs.reshape(1, self.num_rows, self.num_columns, self.num_channels)

        predicted_vector = self.model_load.predict_classes(prediction_feature)
        predicted_class = encoder.inverse_transform(predicted_vector) 
        returnVal = dict()
        returnVal['predicted'] = predicted_class[0]
        #print("The predicted class is:", predicted_class[0], '\n') 

        predicted_proba_vector = self.model_load.predict_proba(prediction_feature) 
        predicted_proba = predicted_proba_vector[0]
        for i in range(len(predicted_proba)): 
            category = encoder.inverse_transform(np.array([i]))
            returnVal[category[0]] = predicted_proba[i]
            #print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )
        return returnVal


#filename = '/home/jovyan/work/capstone/heartbeat-sounds/set_a/murmur__201108222238.wav' 
#buat_prediction(filename)    
