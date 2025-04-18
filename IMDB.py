import streamlit as st
import mysql.connector  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',      
            user='root',           
            password='$elva_30',   
            database='imdb'        
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def run_query(query):
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()  
    try:
        result = pd.read_sql(query, conn)
        conn.close()
        return result
    except Exception as e:
        st.error(f"Error running the query: {e}")
        return pd.DataFrame()  

st.sidebar.title('Dashboard Navigation')
dashboard_options = st.sidebar.radio("Select a Section", ('Overview', 'Visualizations', 'Details','Filtering'))


st.title('Movie Data Dashboard')

query = '''
SELECT Title, Duration, Rating, Voting, Genre 
FROM imdb_movies
ORDER BY Rating DESC
LIMIT 10
'''  

movie_data = run_query(query)

if movie_data.empty:
    st.error("No data found. Please check the database connection or query.")
else:
    
    if dashboard_options == 'Overview':
        st.subheader('Overview of Top 10 Movies')
        st.write("This section provides an overview of the top 10 movies with the highest ratings.")
        st.dataframe(movie_data)  

    elif dashboard_options == 'Visualizations':
        st.subheader('Visualizations')
        
        # Plotting Movie Ratings vs Votes (Top 10)
        st.subheader('Rating vs Voting')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(movie_data['Rating'], movie_data['Voting'], color='blue', alpha=0.7, s=100)
        ax.set_xlabel('Rating', fontsize=14)
        ax.set_ylabel('Number of Votes', fontsize=14)
        ax.set_title('Top 10 Movie Ratings vs Number of Votes', fontsize=16)
        ax.grid(True)
        st.pyplot(fig)

        # Bar Chart of Top 10 Movie Duration
        st.subheader('Top 10 Movie Duration')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(movie_data['Title'], movie_data['Duration'], color='green', alpha=0.7)
        ax.set_xlabel('Movie Title', fontsize=14)
        ax.set_ylabel('Duration (minutes)', fontsize=14)
        ax.set_title('Top 10 Movie Duration', fontsize=16)
        plt.xticks(rotation=45, ha="right", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)

        # Bar Chart of Top 10 Movie Ratings
        st.subheader('Top 10 Movie Ratings')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(movie_data['Title'], movie_data['Rating'], color='orange', alpha=0.7)
        ax.set_xlabel('Movie Title', fontsize=14)
        ax.set_ylabel('Rating', fontsize=14)
        ax.set_title('Top 10 Movie Ratings', fontsize=16)
        plt.xticks(rotation=45, ha="right", fontsize=12)
        ax.grid(axis='y')
        st.pyplot(fig)

        # Genre Distribution for Top 10 Movies - Pie Chart
        st.subheader('Top 10 Genre Distribution')
        genre_counts = movie_data['Genre'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90, 
               colors=sns.color_palette("Set3", n_colors=len(genre_counts)))
        ax.axis('equal')  
        ax.set_title('Genre Distribution of Top 10 Movies', fontsize=16)
        st.pyplot(fig)
    elif(dashboard_options=='Filtering'):
       
        options=st.sidebar.radio("Select your Filters",["Selection","Rating","Voting"])
        if(options=='Selection'):
            st.title("select your data filter")
        if(options=='Rating'):
            st.title("Rating Based Filtering")
            conn = mysql.connector.connect(
            host='127.0.0.1',      
            user='root',           
            password='$elva_30',   
            database='imdb')     
            query=conn.cursor()
            options=st.selectbox("Select your Choice",["select","<5","5-6","6-7","7-8","8-9",">9"])
            if(options=="<5"):
                query.execute("select * from imdb_movies where Rating<=5.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="5-6"):
                query.execute("select * from imdb_movies where Rating>=5.0 and Rating<=6.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="6-7"):
                query.execute("select * from imdb_movies where Rating>=6.0 and Rating<=7.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="7-8"):
                query.execute("select * from imdb_movies where Rating>=7.0 and Rating<=8.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="8-9"):
                query.execute("select * from imdb_movies where Rating>=8.0 and Rating<=9.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options==">9"):
                query.execute("select * from imdb_movies where Rating>=9.0")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
        if(options=='Voting'):
            st.title("Voting Based Filtering")
            conn = mysql.connector.connect(
            host='127.0.0.1',      
            user='root',           
            password='$elva_30',   
            database='imdb')     
            query=conn.cursor()
            options=st.selectbox("Select your Choice",["select","<50000","50000-60000","60000-70000","70000-80000","80000-90000",">90000"])
            if(options=="<50000"):
                query.execute("select * from imdb_movies where Voting<=50000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="50000-60000"):
                query.execute("select * from imdb_movies where Voting>=50000 and Voting<=60000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="60000-70000"):
                query.execute("select * from imdb_movies where Voting>=60000 and Voting<=70000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="70000-80000"):
                query.execute("select * from imdb_movies where Voting>=70000 and Voting<=80000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options=="80000-90000"):
                query.execute("select * from imdb_movies where Voting>=80000 and Voting<=90000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)
            if(options==">90000"):
                query.execute("select * from imdb_movies where Voting>=90000")
                data=query.fetchall()
                dataset=pd.DataFrame(data,columns=["Movie","Duration","Rating","Voting","Genre"])
                st.dataframe(dataset)

    
    elif dashboard_options == 'Details':
        st.subheader('Detailed Information on Movies')
        st.write("Here you can explore more details about the movies, including ratings, genre, duration, and voting.")
        
        st.dataframe(movie_data)  
    