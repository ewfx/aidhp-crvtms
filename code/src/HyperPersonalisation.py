import streamlit as st
import openai
import pandas as pd
import os
from langchain_groq import ChatGroq
# Function to load data
def load_data():
    try:
        customer_prof_individual = pd.read_excel('Customer_Profile_Individual.xlsx')
        customer_prof_organization = pd.read_excel('Customer_Profile_Organization.xlsx')
        social_media_sent = pd.read_excel('Social_Media_Sentiment.xlsx')
        transaction_history = pd.read_excel('Transaction_History.xlsx')
        return customer_prof_individual, customer_prof_organization, social_media_sent, transaction_history
    except PermissionError as e:
        st.error(f"Permission error: {e}")
        return None, None, None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None

# Function to create customer profile
def create_customer_profile(customer_id, merged_data):
    customer_row = merged_data[merged_data['Customer_Id'] == customer_id].iloc[0]
    profile = {
        'Customer_Id': customer_row.get('Customer_Id', 'N/A'),
        'Gender': customer_row.get('Gender', 'N/A'),
        'Location': customer_row.get('Location', 'N/A'),
        'Interests': customer_row.get('Interests', 'N/A'),
        'Preferences': customer_row.get('Preferences', 'N/A'),
        'Income per year': customer_row.get('Income per year', 'N/A'),
        'Education': customer_row.get('Education', 'N/A'),
        'Occupation': customer_row.get('Occupation', 'N/A'),
        'Post_Id': customer_row.get('Post_Id', 'N/A'),
        'Platform': customer_row.get('Platform', 'N/A'),
        'Content': customer_row.get('Content', 'N/A'),
        'Timestamp': customer_row.get('Timestamp', 'N/A'),
        'Sentiment_Score': customer_row.get('Sentiment_Score', 'N/A'),
        'Intent': customer_row.get('Intent', 'N/A'),
        'Product_Id': customer_row.get('Product_Id', 'N/A'),
        'Transaction Type': customer_row.get('Transaction Type', 'N/A'),
        'Category': customer_row.get('Category', 'N/A'),
        'Amount (In Dollars)': customer_row.get('Amount (In Dollars)', 'N/A'),
        'Purchase Date': customer_row.get('Purchase Date', 'N/A'),
        'Payment Mode': customer_row.get('Payment Mode', 'N/A'),
        'Industry': customer_row.get('Industry', 'N/A'),
        'Financial Needs': customer_row.get('Financial Needs', 'N/A'),
        'Revenue (in dollars)': customer_row.get('Revenue (in dollars)', 'N/A'),
        'No of employees': customer_row.get('No of employees', 'N/A')
    }
    return profile

# Function to get recommendations
def get_recommendations(prompt):
    try:
        messages=[
               {"role": "system", "content": "You are an AI-powered product recommendation assistant. Your task is to recommend the most relevant products to users based on their preferences, past behavior, and vector-based similarity scores from a vector database"},
                 {"role": "user", "content": prompt}
             ]
        #     max_tokens=150
        response = ChatGroq(model="qwen-2.5-32b").invoke(messages)
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     max_tokens=150
        # )
        # return response.choices[0].message['content'].strip()
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to refine recommendations
def refine_recommendations(recommendations):
    return recommendations.split('\n') if recommendations else []

# Streamlit app
st.title("Hyper Personal Recommendations")
os.environ["GROQ_API_KEY"] = st.text_input("Enter Groq Api Key",type="password")
# openai.api_key = st.text_input("Enter Open Api Key",type="password")
customer_id = st.text_input("Enter Customer ID")
if customer_id:
    customer_prof_individual, customer_prof_organization, social_media_sent, transaction_history = load_data()
    if customer_prof_individual is not None:
        merged_data_ind = pd.merge(customer_prof_individual, social_media_sent, on='Customer_Id', how='left')
        merged_data_ind = pd.merge(merged_data_ind, transaction_history, on='Customer_Id', how='left')
        
        profile = create_customer_profile(customer_id, merged_data_ind)
        
        prompt = (
            f"Customer_Id: {profile['Customer_Id']}\n"
            f"Gender: {profile['Gender']}\n"
            f"Location: {profile['Location']}\n"
            f"Interests: {profile['Interests']}\n"
            f"Preferences: {profile['Preferences']}\n"
            f"Income per year: {profile['Income per year']}\n"
            f"Education: {profile['Education']}\n"
            f"Occupation: {profile['Occupation']}\n"
            f"Post_Id: {profile['Post_Id']}\n"
            f"Platform: {profile['Platform']}\n"
            f"Content: {profile['Content']}\n"
            f"Timestamp: {profile['Timestamp']}\n"
            f"Sentiment_Score: {profile['Sentiment_Score']}\n"
            f"Intent: {profile['Intent']}\n"
            f"Product_Id: {profile['Product_Id']}\n"
            f"Transaction Type: {profile['Transaction Type']}\n"
            f"Category: {profile['Category']}\n"
            f"Amount (In Dollars): {profile['Amount (In Dollars)']}\n"
            f"Purchase Date: {profile['Purchase Date']}\n"
            f"Payment Mode: {profile['Payment Mode']}\n"
            f"Industry: {profile['Industry']}\n"
            f"Financial Needs: {profile['Financial Needs']}\n"
            f"Revenue (in dollars): {profile['Revenue (in dollars)']}\n"
            f"No of employees: {profile['No of employees']}\n\n"
            "generate hyper personalized recommendations for products, services, or content while also providing actionable insights for businesses to optimize customer engagement.Maximum 3 insights."
        )
        
        recommendations = get_recommendations(prompt)
        # st.write(recommendations)
        refined_recommendations = refine_recommendations(recommendations.content)
        
        st.subheader("Recommendations")
        for rec in refined_recommendations:
             st.write(rec)