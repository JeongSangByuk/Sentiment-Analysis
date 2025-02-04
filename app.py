import sklearn
from flask import Flask
from flask import request
import joblib
import librosa
import numpy as np
import os
import base64
import tensorflow
import json
import test
import question
import sentiment_text

app = Flask(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# 모든 음성파일의 길이가 같도록 후위에 padding 처리
pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i - a.shape[1]))))


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/analysis')
def analyze_self_introduction():
    text = ""
    result = question.get_keyword_summarizer(text)
    return str(question.chat(result))

@app.route('/bertmodel')
def get_bert_model():
    return sentiment_text.get_bert_model("상벽아 안녕")

@app.route('/audio-sentiment', methods=['POST'])
def audio_test():  # put application's code here

    # return load_audio("./test/happy.wav")
    base64data = request.get_json().get('base64data').split(',')[1]

    try:
        decode_string = base64.b64decode(base64data)

        wav_file = open("./test/data1.wav", "wb")
        wav_file.write(decode_string)

        return load_audio("./test/data1.wav")

    except Exception as e:
        print(str(e))
        return "error-1"

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

    l_list = {'p': str(int(result[0][0] * 100)), 'n': str(int(result[0][1] * 100))}
    jsonStr = json.dumps(l_list)
    return jsonStr

if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000', debug=True)





