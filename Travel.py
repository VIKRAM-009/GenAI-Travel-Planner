# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 14:27:06 2025

@author: vicky
"""
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os

# Set Streamlit page configuration
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="centered")

# Secure API Key
API_KEY =  "****************************"
# UI Title & Description
st.title("🌍 AI-Powered Travel Planner")
st.write("📍 Enter your travel details to get estimated travel costs, durations, and recommendations for various travel modes!")

# Input fields
source = st.text_input("Source:")
destination = st.text_input("Destination:")

if st.button("🔍 Generate Travel Plan"):
    if source and destination:
        with st.spinner("🛠️ Compiling travel options... Please wait."):
            # Chat prompt setup
            chat_template = ChatPromptTemplate(messages=[
                ("system", """You are an AI-Powered Travel Planner assistant that provides users with the best travel options based on their requirements.
                 Given a source and destination, you must provide the distance and suggest the best travel options, including bike, cab, bus, train, and flight.
                 Each option should include estimated cost, travel time, distance, and relevant details such as stops or traffic conditions.
                 Additionally, provide information about the best local food items available along the route.
                 Present the results in a clear, easy-to-read format."""),

                ("human", f"Find travel options from {source} to {destination} with estimated costs and also suggest popular food stops along the route.")
                ])

            # Initialize Chat Model
            chat_model = ChatGoogleGenerativeAI(api_key=API_KEY, model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            chain = chat_template | chat_model | parser

            # Get response
            raw_input = {"source": source, "destination": destination}
            response = chain.invoke(raw_input)

            # Process response
            travel_modes = response.split("\n")

            st.success("🚀 Best Travel Options", icon="✅")

            # Display results in a structured way
            for mode in travel_modes:
                icon = ""  # Initialize empty icon

                if "Flight" in mode:
                    icon = "✈️"
                elif "Train" in mode:
                    icon = "🚆"
                elif "Bus" in mode:
                    icon = "🚌"
                elif "Cab" in mode:
                    icon = "🚖"
                elif "Bike" in mode:
                    icon = "🏍️"

                if icon:  # Only display icon if it's set
                    st.markdown(f"{icon} **{mode}**")
                else:
                    st.markdown(f"**{mode}**")

            st.divider()

    else:
        st.error("⚠️ Please enter both **Source** and **Destination** to generate travel options!")
