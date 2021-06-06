import streamlit as st
import io
import requests
import json
from PIL import Image
from PIL import ImageDraw

st.title('＜　顔検出アプリ　＞')

with open('people.jpeg', 'rb') as f:
  binary_img = f.read()

subscription_key = '848dfb4d8b36447ea6985474fd56c0f4'
assert subscription_key

face_api_url = 'https://20210601katsuki.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("Chose an image... ",type='jpeg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

#    img = Image.open('people.jpeg')
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()    #バイナリ取得

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        text = result['faceAttributes']['gender']+','+str(int(result['faceAttributes']['age']))+' ('+str(int(result['faceAttributes']['emotion']['happiness']*100))+'%)'

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='red', width=3)
        draw.text((rect['left']+5, rect['top']-10),text, fill='red', align='center', width=2)

    st.image(img, caption='uploaded image..', use_column_width=True)

