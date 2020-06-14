# Utility
import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm


# Audio
import librosa

# tensorflow
import tensorflow as tf

# Scikit learn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Keras
import keras

class HeartbeatCF():
    
    def __init__(self):
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
        
        x_train, x_test = [], []
        
        for idx in tqdm(range(len(train))):
            x_train.append(extract_features(train.filename.iloc[idx]))

        for idx in tqdm(range(len(test))):
            x_test.append(extract_features(test.filename.iloc[idx]))
            
        x_test = np.asarray(x_test)
        x_train = np.asarray(x_train)

        encoder = LabelEncoder()
        encoder.fit(train.label)

        model_load =  keras.models.load_model('my_model.h5')

        num_rows = 40
        num_columns = 173
        num_channels = 1

        
    def extract_features(audio_path):
        y, sr = librosa.load(audio_path, duration=4)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)        
        return mfccs

    
    

    def buat_prediction(file_name):
        prediction_feature = extract_features(file_name) 
        prediction_feature = prediction_feature.reshape(1, num_rows, num_columns, num_channels)

        predicted_vector = model_load.predict_classes(prediction_feature)
        predicted_class = encoder.inverse_transform(predicted_vector) 
        returnVal = dict()
        returnVal['predicted'] = predicted_class[0]
        #print("The predicted class is:", predicted_class[0], '\n') 

        predicted_proba_vector = model_load.predict_proba(prediction_feature) 
        predicted_proba = predicted_proba_vector[0]
        for i in range(len(predicted_proba)): 
            category = encoder.inverse_transform(np.array([i]))
            returnVal[category[0]] = predicted_proba[i]
            #print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )
        return returnVal


#filename = '/home/jovyan/work/capstone/heartbeat-sounds/set_a/murmur__201108222238.wav' 
#buat_prediction(filename)    
