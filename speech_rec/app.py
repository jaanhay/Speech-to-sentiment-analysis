from flask import Flask, request,render_template
import joblib
import librosa
import soundfile
import os, glob, pickle
import numpy as np
model=joblib.load('sentiment_model.pkl')
def extract_feature(file_name,mfcc,chroma,mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X= sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        result=np.array([])
        if chroma:
            stft=np.abs(librosa.stft(X))
            chroma_feat=np.mean(librosa.feature.chroma_stft(S=stft,sr=sample_rate).T,axis=0)
            result=np.hstack((result,chroma_feat))
       
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X,sr=sample_rate,n_mfcc=40).T,axis=0)
            result=np.hstack((result,mfccs))
        if mel:
            mel_spec=np.mean(librosa.feature.melspectrogram(y=X,sr=sample_rate).T,axis=0)
            result=np.hstack((result,mel_spec))
    return result




app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/',methods=['POST'])
def upload_file():
    file_fin=request.files['file']
    feature=extract_feature(file_fin,mfcc=True,chroma=True,mel=True)

    y=model.predict(feature.reshape(1,-1))
    result = str(y[0])
    return result


if __name__ == '__main__':
    app.run(debug=True,)

