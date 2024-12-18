# Import the required libraries
import streamlit as st
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools

# Set up the Streamlit app
st.title("AI Investment Agent 📈🤖")
st.caption("This app allows you to compare the performance of two stocks and generate detailed reports.")

# Sidebar for user inputs
st.sidebar.header("Stock Input Panel")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
stock1 = st.sidebar.text_input("Enter the first stock symbol", placeholder="e.g., AAPL")
stock2 = st.sidebar.text_input("Enter the second stock symbol", placeholder="e.g., MSFT")

# Main Page Content
if openai_api_key:
    # Create an instance of the Assistant
    assistant = Assistant(
        llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
            )
        ],
        show_tool_calls=True,
    )

    # Validate input and display results
    if stock1 and stock2:
        st.subheader(f"Comparing **{stock1}** and **{stock2}**")
        with st.spinner("Fetching data and generating reports..."):
            query = f"Compare {stock1} to {stock2}. Use every tool you have."
            response = assistant.run(query, stream=False)
        st.success("Here is your comparison report:")
        st.write(response)
    elif not stock1 or not stock2:
        st.warning("Please enter both stock symbols in the sidebar.")
else:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
