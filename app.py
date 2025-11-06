import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.chains import LLMMathChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
from langchain_classic.tools import Tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Streamlit app setup
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar key input
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

# Tools setup
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned"
)

math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expression needs to be provided."
)

prompt = """
You're an agent tasked with solving users' mathematical questions.
Logically arrive at the solution and provide a detailed, point-wise explanation.

Question: {question}
Answer:
"""
prompt_template = PromptTemplate(input_variables=["question"], template=prompt)
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

system_prompt_string = """You are a helpful and professional research assistant.
Your job is to answer the user's question using the tools provided.

Follow these rules:
1. Analyze the user's question and chat history.
2. Decide if a tool is needed.
3. Use the single best tool (calculator, Wikipedia, or reasoning tool).
4. Combine the tool's results into a clear, human-readable answer.
5. Never output tool calls or raw JSON — only plain text results.
"""

assistant_agent = create_agent(
    model=llm,
    tools=[wikipedia_tool, calculator, reasoning_tool],
    system_prompt=system_prompt_string
)

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input section
question = st.text_area(
    "Enter your question:",
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries (25 each). How many total pieces of fruit do I have?"
)

if st.button("Find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.invoke({"messages": st.session_state.messages}, callbacks=[st_cb])
            ##response_text = response.get("output", str(response))
            content = response["messages"][-1].content

            st.session_state.messages.append({'role': 'assistant', 'content': content})
            st.write("### Response:")
            st.success(content)
    else:
        st.warning("Please enter a question.")
