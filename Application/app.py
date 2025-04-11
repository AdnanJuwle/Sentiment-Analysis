import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px

# App title
st.title("Sentiment Analysis Tool")
st.subheader("Analyze product reviews and video comments")

# Input options
analysis_type = st.radio("Choose analysis type:", 
                        ("Single Text", "Batch Analysis (CSV Upload)"))

if analysis_type == "Single Text":
    # Single text analysis
    user_input = st.text_area("Enter text to analyze (review, comment, etc.):")
    
    if user_input:
        # Perform sentiment analysis
        analysis = TextBlob(user_input)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Display results
        st.subheader("Analysis Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sentiment Polarity", f"{polarity:.2f}", 
                     help="Range from -1 (negative) to +1 (positive)")
        with col2:
            st.metric("Subjectivity", f"{subjectivity:.2f}", 
                     help="Range from 0 (objective) to 1 (subjective)")
        
        # Visual indicator
        if polarity > 0.1:
            st.success("Overall Positive Sentiment")
        elif polarity < -0.1:
            st.error("Overall Negative Sentiment")
        else:
            st.info("Overall Neutral Sentiment")
            
else:
    # Batch analysis
    uploaded_file = st.file_uploader("Upload CSV file with text to analyze:", 
                                   type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        text_column = st.selectbox("Select the column containing text to analyze:", 
                                 df.columns)
        
        if st.button("Analyze Sentiment"):
            # Analyze each row
            df['polarity'] = df[text_column].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            df['subjectivity'] = df[text_column].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
            df['sentiment'] = df['polarity'].apply(
                lambda x: 'positive' if x > 0.1 else ('negative' if x < -0.1 else 'neutral'))
            
            # Show results
            st.subheader("Analysis Results")
            
            # Sentiment distribution
            fig1 = px.pie(df, names='sentiment', title='Sentiment Distribution')
            st.plotly_chart(fig1)
            
            # Polarity distribution
            fig2 = px.histogram(df, x='polarity', title='Polarity Score Distribution')
            st.plotly_chart(fig2)
            
            # Download results
            st.download_button(
                label="Download Results as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='sentiment_analysis_results.csv',
                mime='text/csv'
            )

# Instructions
st.sidebar.markdown("""
### How to Use:
1. Select analysis type (single text or batch)
2. For single text: Enter your text and see results
3. For batch: Upload a CSV file with one column containing text
4. View and download results

### Interpretation:
- **Polarity**: -1 (negative) to +1 (positive)
- **Subjectivity**: 0 (fact-based) to 1 (opinionated)
""")