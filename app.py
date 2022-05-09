import sklearn
from flask import Flask
import joblib
import librosa
import numpy as np
import test

app = Flask(__name__)

# 모든 음성파일의 길이가 같도록 후위에 padding 처리
pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i - a.shape[1]))))


@app.route('/')
def hello_world():  # put application's code here

    return 'Hello World!'


@app.route('/test')
def audio_test():  # put application's code here
    load_audio("./test2.wav")
    return '성공 ! !'


if __name__ == '__main__':
    app.run()


def load_audio(audio_name):
    audio, sr = librosa.load(audio_name)
    mfcc = librosa.feature.mfcc(audio, sr=16000, n_mfcc=100, n_fft=400, hop_length=160)
    mfcc = sklearn.preprocessing.scale(mfcc, axis=1)
    # 모든 음성파일의 길이가 같도록 후위에 padding 처리
    padded_mfcc = pad2d(mfcc, 300)
    padded_mfcc = np.expand_dims(padded_mfcc, 0)
    # 파일로 저장된 모델 불러와서 예측
    clf_from_joblib = joblib.load('model/mfcc.pkl')
    result = clf_from_joblib.predict(padded_mfcc)
    print(result)
