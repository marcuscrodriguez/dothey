import glob
import os
import streamlit as st
import pandas as pd
from textblob import TextBlob
cwd = os.getcwd()
cwd
# Define a function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def main():
    
    # Custom CSS to set background color
    st.markdown(
    	"""
    	<style>
    	body {
    		background-color: #f6f0f0;
    	}
    	</style>
    	""",
    	unsafe_allow_html=True
    )
        
    st.title("Do They Love Me?")
    
    # Display image from file path
    st.image("do_they.webp", caption="Do they?", use_column_width=True)
    
    # Define questions and categories
    questions = [
        {"category": "Behavior", "question": "How often does your partner express affection towards you verbally or physically?"},
        {"category": "Behavior", "question": "How frequently does your partner prioritize spending quality time with you?"},
        {"category": "Behavior", "question": "How often does your partner go out of their way to do things to make you happy?"},
        {"category": "Behavior", "question": "How often does your partner show genuine interest in your life, including your interests, hobbies, and aspirations?"},
        {"category": "Behavior", "question": "When you're not together, does your partner make an effort to maintain communication and stay connected with you?"},
        {"category": "Behavior", "question": "How often does your partner set aside time to nurture and maintain the relationship?"},
        {"category": "Behavior", "question": "Does your partner respond positively to your achievements or successes?"},
        {"category": "Behavior", "question": "When faced with conflicts or disagreements, does your partner compromise?"},
        {"category": "Behavior", "question": "Does your partner make you feel special by attending to your individual needs and preferences?"},
        {"category": "Behavior", "question": "Does your partner respond sympathetically when you're going through a difficult time or facing challenges?"},
        {"category": "Emotion", "question": "Do you feel supported and understood by your partner when discussing your feelings?"},
        {"category": "Emotion", "question": "Are you comfortable discussing your vulnerabilities or fears with your partner?"},
        {"category": "Emotion", "question": "Reflecting on your overall relationship, do you feel valued and respected by your partner?"},
        {"category": "Emotion", "question": "Do you feel secure in your relationship with your partner?"},
        {"category": "Emotion", "question": "When thinking about the future, do you see your partner in it as a long-term companion?"},
        {"category": "Decision", "question": "Do you trust your partner to make an important decision that will affect both of you in the long run?"},
        {"category": "Decision", "question": "You are much older, sitting on the sand at the beach. You look over to the spot next to you. Do you visualize yourself with your partner?"}
    ]
    
    # Initialize dictionary to store responses
    responses = {}
    
    # Display questions and capture responses
    st.subheader("Instructions")
    st.write("Informed Consent - The data collected in this survey is completely anonymous. There isn't any personally identifiable information that will be collected and the information that you choose to provide cannot be traced back to you. Your participation is voluntary and you may choose not to participate or end your participation at any time without penalty. There isn't any compensation provided for participating in the survey. I have read, understand and consent to all of the terms provided and certify that I am 18 years old or older.")
    
    with st.form(key='love_questionnaire_form', clear_on_submit=True, border=True):
        consent = st.checkbox('By clicking this checkbox and/or Submit Response button, I indicate my willingness to voluntarily take part in this survey.', value=False, key='consent')
        
        gender = st.selectbox(
            'What is Your Gender Identity',
            ("Male", "Female", "Non-Binary", "Transgender", "Rather Not Say"))
            
        st.info("Questions & Answers: |-1 Never | 0 Sometimes | 1 Always|")
        
        for q in questions:
            response = st.slider(q["question"], -1.0, 1.0, 0.0, 0.1, key=f"{q['category']}_{questions.index(q) + 1}")
            responses[q["question"]] = response
        
        text = st.text_area('Write a few sentences that explains how you feel about your partner: 💔️💛️💚️')
        
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            # Calculate Sentiment Score Paragraph Add to DF
            sentiment_score = analyze_sentiment(text)
            #print("Sentiment Score:", "%.2f" % sentiment_score)
            # Create DataFrame from responses
            df = pd.DataFrame.from_dict(responses, orient='index', columns=['Response'])
            # Add consent and gender to DataFrame
            df.insert(0, 'Consent', consent)
            df.insert(1, 'Gender', gender)
            df.insert(2, 'Sentiment', "%.2f" % sentiment_score)
            # Store responses in a CSV file
            df.to_csv("do_they.csv", mode='a', header=False)
            st.success("Responses submitted successfully!")
            st.balloons()
            average = "%.2f" % ((df['Response'].sum() + (sentiment_score * 3)) / 20)
            st.subheader(f"Your Overall Score: {average}")
            # Display image from file path
            st.image("loveline.png", use_column_width=True)            
            st.write("This test explores the duality of positive and negative behavior (questions 1-10), emotions (questions 11-15), thoughts/decisions (questions 16,17) as well as utilizes AI to analyze sentiment giving you an overview of the overall strength of your relationship. Positive behavior (+1) represents the frequency and consistency of beneficial behaviors exhibited in the relationship. While a value closer to (-1) indicates the frequency and consistency of negative behaviors. Higher positive behavior scores indicate a healthier relationship dynamic, characterized by frequent displays of affection, prioritization of quality time, and mutual support. Conversely, higher negative behavior scores may indicate areas of concern such as lack of communication or conflict resolution. Positive (+1)  and negative (-1) emotion scores reflects the perceived level of emotional support and understanding within the relationship including the comfort level in expressing vulnerabilities and fears with your partner. Higher emotional scores suggest a strong emotional bond and mutual understanding. Lower scores may indicate a need for improved communication and empathy within the relationship. Thoughts/Decisions are also measured positively (+1) and negatively (-1) reflecting the perception of long-term compatibility as well as level of trust  impacting the confidence in the relationship's future and belief in your partner's decision-making ability. Lower scores may suggest uncertainty or lack of trust, which could benefit from open communication and reassurance. A higher positive sentiment analysis score suggests overall satisfaction and contentment within the relationship, while a higher negative sentiment analysis score may indicate dissatisfaction or concern.")
            
    # Contact
    st.write("🚥️ If you have any questions or concerns with respect to the survey you may contact marcuscrodriguez@outlook.com / www.marcusc.com.")

    ###st.download_button('do_they.csv', text_contents, 'text/csv')###
    
if __name__ == "__main__":
    main()

