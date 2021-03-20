import numpy as np 
import jieba 
import numpy as np 
import matplotlib.pyplot as plt
import streamlit as st
import time

from streamlit import uploaded_file_manager

from PIL import Image
from wordcloud import WordCloud

##### __init__

font_path = r"./data/SimHei.ttf"

with open("./data/stopwords.txt", "r") as f:
    stopwords = [word.strip() for word in f] # strip関数で左右改行を削除(replacedでも可能)

##### 使用方法の説明
st.title("3 steps to genarete word picture!")
st.text("Step 1: Input Text")
st.text("Step 2: Upload Picture")
st.text("Step 3: One click to Generate word Picture")


#### テキストを入力   
st.header("Generate text key word on Pincture")
text = st.text_input(
    "Input text contain",
    max_chars=10000,
)


##### 分かち書き
seg_list = jieba.cut(text,cut_all=True)
word_list = [word for word in seg_list if len(word) >= 2]
st.text("Sepration Word")
st.write(word_list)

## 単語をカウント
data = {}

for word in word_list:
    if not data.__contains__(word):
        data[word] = 0

    else:
        data[word] +=1

st.text("Frequency word")
st.write(data)




##### ファイルをアップロード
uploaded_file = st.header("Upload the pic which is used to be backgrand of generated word img")
uploaded_file = st.file_uploader(
    "Input Image file",
    type="jpg"
)

if uploaded_file is not None :
    
    image = Image.open(uploaded_file)
    image_array = np.asarray(image)
    st.write("Transformed 2 dimentons vecotor")

    my_wordcloud = WordCloud(
    background_color= "white",
    max_words=400,
    font_path= font_path,
    mask= image_array,
    height=1000,
    width=1000,
    stopwords= stopwords
).generate_from_frequencies(data)

    #my_wordcloud.to_file('result.jpg')
    image = my_wordcloud.to_image()
    
    # time 
    latest_iteration = st.empty()
    bar = st.progress(0)
    
    st.image(image,caption="Outputed",use_column_width=True)