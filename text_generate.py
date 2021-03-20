import numpy as np 
import jieba 
import numpy as np 
import matplotlib.pyplot as plt
plt.style.use("ggplot")

import streamlit as st


from matplotlib.font_manager import FontProperties
from collections import Counter
from streamlit import uploaded_file_manager

from PIL import Image
from wordcloud import WordCloud

##### __init__

font_path = r"./data/SimHei.ttf"
font = FontProperties(fname= font_path, size=16)

#### load stopwords
with open("./data/stopwords.txt", "r") as f:
    stopwords = [word.strip() for word in f] # strip関数で左右改行を削除(replacedでも可能)

##### 使用方法の説明
st.title("3 steps to genarete word picture!")
st.text("Step 1: Input Text")
st.text("Step 2: Chouse option key gen or text gen ")
st.text("Step 3: One click to Generate Cloud Picture")


#### テキストを入力   
st.header("Generate text key word on Pincture")



##### 関数
### 分かち書き
def word_token_list(text):

    seg_list = jieba.cut(text,cut_all=True)
    word_list = [word for word in seg_list if len(word) >= 2]
    st.text("Sepration Word")
    st.write(word_list)

    
### 単語をカウント  
def word_counter(text):
    seg_list = jieba.cut(text,cut_all=True)
    word_list = [word for word in seg_list if len(word) >= 2]
    
    data = {}
    data = dict(Counter(word_list))

    st.text("Frequency word")
    st.write(data)

    return data


def word_cloud(data):
    
    if len(data)  != 0:
        try:
            my_wordcloud = WordCloud(
            background_color= "PAPAYAWHIP",
            max_words=400,
            font_path= font_path,
            mask= None, #image_array,
            height=1000,
            width=1000,
            stopwords= stopwords,
        ).generate_from_frequencies(data)
        except ImportError as err:
            print(err)

        #my_wordcloud.to_file('result.jpg')
        image = my_wordcloud.to_image()
            
        # Show image 
        st.image(image,caption="Outputed",use_column_width=True)
        
    else:
        st.text("Please inputting text")

def word_text_cloud(text="我是外星人"):
    if len(text) != 0:
        
        my_wordcloud = WordCloud(
            background_color= "PAPAYAWHIP",
            contour_color='PAPAYAWHIP',
            relative_scaling='auto',
            max_words=200,
            font_path= font_path,
            mask= None, #image_array,
            height=1000,
            width=1000,
            stopwords= stopwords,
        ).generate_from_text(text)

        # my_wordcloud.to_file('result.jpg')
        image = my_wordcloud.to_image()
            
        # Show image 
        st.image(image,caption="Outputed",use_column_width=True)
    else:
        st.text("Please input at least one sentence")

def plot_bar(data):
    # data is type of dictionary 
    x = data.keys()
    y = data.values()
    st.write(type(data))

    fig, ax = plt.subplots(figsize=(12,8))
    ax.bar(x,y)
    
    ax.set_xlabel("Word",size=16)
    ax.set_ylabel("Count",size=16)

    
    plt.xticks(rotation=65,size=16, fontproperties=font)
    plt.yticks(range(0,11))
    plt.title("Word Counts Plotting Bar")
    st.pyplot(fig)







##### Main
### ラジオンボタン
option_button = st.selectbox(
    "Choose options:",

    ("Key frequency generation","Directly Text generation")
)

if option_button == ("Key frequency generation"):
    
    text = st.text_input(
        "Input text contain",
        max_chars=20000,
    )

    # Segmetation 
    word_token_list(text)

    # Count words
    data = word_counter(text)

    # plot bar
    option_button = st.checkbox("Show Count Bar")
    if option_button == True:
        plot_bar(data)

    # generate pic 
    word_cloud(data)

if option_button == ("Directly Text generation"):
    
    text = st.text_input(
        "Input text contain",
        max_chars=200,
    )

    
    if len((text)) != 0:
        word_text_cloud(text)

    
