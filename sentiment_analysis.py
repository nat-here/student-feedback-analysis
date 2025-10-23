from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="Sentiment Analysis of Student Feedback",
    page_icon="🧠",
    layout="centered",
)

# ---- TITLE SECTION ----
st.title("🎓 Sentiment Analysis of Student Feedback")
st.markdown(
    """
    This AI-based web app analyzes **student reviews about teachers** using Natural Language Processing (NLP).  
    It identifies whether each comment expresses a **Positive**, **Negative**, or **Neutral** sentiment.  
    Upload your CSV file containing a `comment` column or enter `text` to get started.
    """
)
with st.expander('Analyze Text'):
    text = st.text_input('Text here: ')
    if text:
        analyzer=SentimentIntensityAnalyzer()
        polarity=analyzer.polarity_scores(text)
        if polarity['neg']>polarity['pos']:
            st.write(":red[NEGATIVE REVIEW]")
        elif polarity['pos']>polarity['neg']:
            st.write(":green[POSITIVE REVIEW]")
        else:
            st.write("NEUTRAL REVIEW")
with st.expander("### 📂 Upload Feedback File"):
    upl = st.file_uploader("Upload a CSV file containing student feedback", type=['csv'])

    analyzer = SentimentIntensityAnalyzer()

    def score(x):
        if isinstance(x, str):  
            polarity = analyzer.polarity_scores(x)
            return polarity['compound']     
    def analyze(x):
        if x >= 0.05:
            return 'Positive'
        elif x <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    def counts(x):
        p=0
        n=0
        ne=0
        if x=='Positive':
            p+=1
        elif x=="Negative":
            n+=1
        else:
            ne+=1
        return p,n,ne
    

    if upl:
        df = pd.read_csv(upl)

        
        if 'comment' not in df.columns:
            st.error("CSV must have a column named 'comment'")
        else:
            df['score'] = df['comment'].apply(score)
            df['sentiment'] = df['score'].apply(analyze)
            sentiments=df['sentiment'].apply(counts)
            p,n,ne=sentiments.apply(pd.Series).sum()
            st.write(df)
            

        st.markdown("### 📈 Sentiment Donut Chart")
        fig = go.Figure(data=[go.Pie(
        labels=['Positive', 'Negative', 'Neutral'],
        values=[p, n, ne],
        hole=0.4,
        marker=dict(colors=['#00cc96', '#EF553B', '#636EFA'])
        )])
        fig.update_layout(title_text='Chart Analysis')

        st.plotly_chart(fig)
        st.markdown("### 🧾 Summary Report")
        st.write(f"**Total Comments Analyzed:** {len(df)}")
        st.write(f"**Positive:** {p}")
        st.write(f"**Negative:** {n}")
        st.write(f"**Neutral:** {ne}")



            

  

