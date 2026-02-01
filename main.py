import streamlit as st, time
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

st.set_page_config(page_title="LAGmate", layout="wide")
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="You are a helpful assistant and your name is LAGmate")]

st.title(":orange[LAGmate]")
st.divider()
with st.sidebar:
    st.header(":green[Mohammad Miraz Ali]")
    st.write(":green[Dept. of EEE]\n\n:green[University of Dhaka]")

try:
    model = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key not found! Please set GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

for m in st.session_state.messages:
    if not isinstance(m, SystemMessage):
        with st.chat_message("user" if isinstance(m, HumanMessage) else "assistant"):
            st.markdown(m.content)

if user_input := st.chat_input("Say...something ??"):
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.chat_message("user").markdown(user_input)
    
    with st.chat_message("assistant"):
        asst_box, full_reply = st.empty(), ""
        try:
            response = model.invoke(st.session_state.messages).content
            for char in response:
                full_reply += char
                asst_box.markdown(full_reply + "▌")
                time.sleep(0.005)
            asst_box.markdown(response)
            st.session_state.messages.append(AIMessage(content=response))
        except Exception as e:
            st.error(f"Error: {e}")
