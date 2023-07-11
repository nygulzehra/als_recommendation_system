import pyspark
import pandas as pd
from PyQt5.QtCore import QFile, QIODevice
import streamlit as st
from joblib import load
import pickle
import numpy as np

# Page Settings
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="",
    layout="centered",
    menu_items={
        "Get help": "mailto:nygulzehra@gmail.com",
        "About": "For More Information\n" + "https://github.com/nygulzehra"
    }
)


# ---------------load pickle files------------
# for book info
file = QFile('df_books.pkl')
if file.open(QIODevice.ReadOnly):
    f = io.BytesIO(file.readAll().data())
    df_books = pd.read_pickle(f, compression=None)

# for top100 books
file1 = QFile('top_100_books.pkl')
if file1.open(QIODevice.ReadOnly):
    f1 = io.BytesIO(file1.readAll().data())
    top_100_books = pd.read_pickle(f1, compression=None)
    

recommendation_tbl = pickle.load(open('recommendation_tbl.pkl','rb'))

# cosine_scores
cosine = pickle.load(open('cosine.pkl','rb'))

# euc_scores
euc = pickle.load(open('euc.pkl','rb'))

# mht_scores
mht = pickle.load(open('mht.pkl','rb'))

pivot = pickle.load(open('pivot.pkl','rb'))


# -------------------------User Interface------------------------------------------------------------------


home, pop, rec = st.tabs(["Home", "Popular Books", "Recommendations"])

with home:
    st.title("**:black[BookWorm : Book Recommendation System]**")
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("*:blue[Welcome to the Book Recommendation System!]*")
        
        st.markdown(
            "In the 1900's, it is estimated that around 18,000 to 20,000 new books were published worldwide in 1900. "
            "But today hundreds of thousands of new books are published each year. "
            "The International ISBN Agency, which assigns unique identifiers to books, reported over 2.2 million new ISBNs issued worldwide in 2020. "
            "It's worth noting that this number includes both print and digital publications across different genres and languages."
        )
    with col2:
        st.image("books.jpg", width=300)
    st.markdown("This recommendation system helps you to find the perfect books that you would love to read.")

# --------------------------Popular Boooks-------------------    

with pop:
    st.title("**:black[BookWorm : Book Recommendation System]**")
    st.divider()    

    st.subheader("*:blue[Top 100 Books for All Time]*")
    i = 0   
    for index, row in top_100_books.iterrows():
                
        book = int(row['book_id'])
        
        img = row['image_url']
        i += 1
        top = "#"+str(i)
        st.subheader(top)
        st.image(img, width=200)
        st.markdown(row['title'])
        st.markdown(row['authors'])

# -------------------------- Recommendation -------------------  
        
with rec:
    
    User, Guest = st.tabs(["User", "Guest"])
#     ----------------------for user --------------------
    
    with User:
        
        st.title("**:black[BookWorm : Book Recommendation System]**")
        st.divider()
        st.subheader("*:blue[Get personalized book recommendations!]*")
        st.markdown("We will help you to discover the perfect book for you.")

        text = st.text_input("Write your user id here")
        try:
            if st.button(key="Submit1", label="Submit"):
                st.subheader("Top 10 book recommendations for user: [ " + text + " ]")

                list1 = recommendation_tbl[recommendation_tbl.user_id == int(text)]
                i = 0  

                for index, row in list1.iterrows():

                    book = int(row['book_id'])

                    book_info = df_books[df_books.id == book ]

                    img = book_info['image_url'].values[0]
                    i += 1
                    top = "#"+str(i)
                    st.subheader(top)
                    st.image(img, width=200)
                    st.markdown(book_info['title'].values[0])
                    st.markdown(book_info['authors'].values[0])
        except:
            st.markdown("User Id is uncorrect. Please try again.")

   #     ----------------------for guest  -------------------- 
    
    with Guest:
        
        
        def recommend(book_name):
    
            # index fetch
            index = np.where(pivot.index==book_name)[0][0]
            similar_cosine = sorted(list(enumerate(cosine[index])),key=lambda x:x[1],reverse=True)[1:6]
            similar_euc = sorted(list(enumerate(euc[index])),key=lambda x:x[1],reverse=True)[1:6]
            similar_manh = sorted(list(enumerate(mht[index])),key=lambda x:x[1],reverse=True)[1:6]

            data = []
            for i in similar_cosine:
                data.append(pivot.index[i[0]])

            data2 = []
            for i in similar_euc:
                data2.append(pivot.index[i[0]])

            data3 = []
            for i in similar_manh:
                data3.append(pivot.index[i[0]])


            return  data,data2,data3
        
        
#  -----------------------------------       ---------------

        st.title("**:black[BookWorm : Book Recommendation System]**")
        st.divider()
        st.subheader("*:blue[Get personalized book recommendations!]*")
        st.markdown("We will help you to discover the perfect book for you.")

        book_name = st.text_input("Write your favorite book's name here")
        try:
            if st.button(key="Submit2", label="Submit"):
                st.subheader("If you like  [ " + book_name + " ], most likely you would like these : ")

                st.divider()
                col3, col4, col5 = st.columns(3)

                data, data2, data3 = recommend(book_name)


                with col3:
                    i = 0
                    st.subheader('Cosine Similarity :')
                    for index in range(0, len(data)):

                        book = data[index]

                        book_info = df_books[df_books.title == book ]

                        img = book_info['image_url'].values[0]
                        i += 1
                        top = "#"+str(i)
                        st.subheader(top)
                        st.image(img, width=200)
                        st.markdown(book_info['title'].values[0])
                        st.markdown(book_info['authors'].values[0])

                with col4:
                    i = 0
                    st.subheader('Euclidian Distance :')
                    for index in range(0, len(data2)):

                        book = data2[index]

                        book_info = df_books[df_books.title == book ]

                        img = book_info['image_url'].values[0]
                        i += 1
                        top = "#"+str(i)
                        st.subheader(top)
                        st.image(img, width=200)
                        st.markdown(book_info['title'].values[0])
                        st.markdown(book_info['authors'].values[0])


                with col5:
                    i = 0
                    st.subheader('Manhattan Distance :')
                    for index in range(0, len(data3)):

                        book = data3[index]

                        book_info = df_books[df_books.title == book ]

                        img = book_info['image_url'].values[0]
                        i += 1
                        top = "#"+str(i)
                        st.subheader(top)
                        st.image(img, width=200)
                        st.markdown(book_info['title'].values[0])
                        st.markdown(book_info['authors'].values[0])

        
        except:
            st.markdown("Book name is uncorrect. Please try again.")
        
        
        
        

