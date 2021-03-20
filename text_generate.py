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
st.text("Step 1: Select options")
st.text("Step 2: Input text")
st.text("Step 3: Automatically PlotBar/Genareted WordCloud")


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
            height=400,
            width=600,
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
            height=400,
            width=600,
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

    
    plt.xticks(rotation=90,size=16, fontproperties=font)
    plt.yticks(range(0,11))
    plt.title("Word Counts Plotting Bar")
    st.pyplot(fig)

        #image = Image.open("./data/jmap.jpg")
        #image = Image.open("./data/hear.jpg")
        #image = Image.open("./tenso_log.jpg")
def uploader():
    st.subheader("4. Upload image")
    option_button = st.selectbox(
        "Defalut image:",
        ("None","map of China")
    )
    
    if option_button == "map of China":
        image = Image.open("./data/china_map.jpg")
        image_array = np.asarray(image)
        st.write("Transformed matrics vecotor")
        try:
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
            st.image(image,caption="Outputed",use_column_width=True)
        except ValueError as err:
            st.text("Please input text first")
    
    
    else :
        uploaded_file = st.header("Upload the picture which is used to be backgrand of generated word img")
        uploaded_file = st.file_uploader(
        "Input Image file",
        type=["jpg","png"]
        )

        if uploaded_file is not None :
    
            image = Image.open(uploaded_file)
            image_array = np.asarray(image)
            st.write("Transformed matrics vecotor")

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

            st.image(image,caption="Outputed",use_column_width=True)

##### Main
### ラジオンボタン
st.subheader("1. Select options") 
option_button = st.selectbox(
    "Choose options:",

    ("Key frequency generation","Directly Text generation",
    "Plotting any pic of Text Key-Words")
)

### 単語の出現回数で可視化

if option_button == ("Key frequency generation"):
    st.subheader("2. Input text") 
    text = st.text_input(
        "Input text contain",
        max_chars=20000,
    )

    # Segmetation
    
    word_token_list(text)

    # Count words
    data = word_counter(text)

    # plot bar
    st.subheader("3. Show graph")
    option_button = st.checkbox("Show Count Bar")
    if option_button == True:
        plot_bar(data)

    # generate pic
    
    word_cloud(data)

### 入力テキストで直接可視化
if option_button == ("Directly Text generation"):
    st.subheader("2. Input text") 
    text = st.text_input(
        "Input text contain",
        max_chars=200,
    )

    
    if len((text)) != 0:
        word_text_cloud(text)

### 任意の写真を単語の頻度で可視化
if option_button == ("Plotting any pic of Text Key-Words"):
    st.subheader("2. Input text")
    text = st.text_input(
        "Input Large text",
        max_chars=30000
    )
    # word tokens 
    word_list = word_token_list(text)
    
    # count word dict
    data = word_counter(text) 

    # plot word counts
    st.subheader("3. Show graph")
    check_box = st.checkbox(
        "Click to Show bar graph",
    )
    if check_box == True:
        plot_bar(data)

    # uploder image 
    uploader()

    