import streamlit as st
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import ShellTool
from langchain_community.agent_toolkits import FileManagementToolkit
import os
import database

st.set_page_config(page_title="Kali AI", page_icon="✺", layout="wide", initial_sidebar_state="expanded")
database.init_db()
DB_DIR = "chroma_db"

# --- CUSTOM NATIVE DESKTOP CSS ---
custom_css = """
<style>
    /* Hide Streamlit Header, Footer, and Menu for standalone feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark Theme Colors */
    .stApp {
        background-color: #18181A;
        color: #E8E8E8;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1F1F22 !important;
        border-right: 1px solid #2B2B2B;
    }
    
    /* Sidebar Button Overrides */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background-color: transparent !important;
        border: none !important;
        text-align: left !important;
        color: #E8E8E8 !important;
        padding: 8px 15px !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        transition: background-color 0.2s;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #2D2D30 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] .stButton > button:focus {
        box-shadow: none !important;
        color: white !important;
    }
    
    /* Elegant Title */
    .kali-title {
        font-family: 'Georgia', serif;
        text-align: center;
        color: #E8E5DF;
        font-size: 3.5rem;
        margin-top: 15vh;
        margin-bottom: 5vh;
        font-weight: 400;
        letter-spacing: -1px;
    }
    
    /* Chat Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }
    [data-testid="stChatInput"] {
        background-color: #27272A !important;
        border: 1px solid #3F3F46 !important;
        border-radius: 12px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# ---------------------------------

@st.cache_resource
def load_components():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    retriever = None
    if os.path.exists(DB_DIR):
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    settings = database.get_settings()
    model_name = settings.get('llm_model', 'llama3.2')
    temp = float(settings.get('temperature', '0.2'))
    
    llm = Ollama(model=model_name, temperature=temp)
    search_tool = DuckDuckGoSearchRun()
    return retriever, llm, search_tool

retriever, llm, search_tool = load_components()

@tool
def launch_windows_application(app_name: str) -> str:
    """Searches for a Windows application by name in the Start Menu and launches it.
    Use this tool when the user asks to open or launch an application like OBS, Discord, etc.
    Input should be the name of the application (e.g. 'obs', 'discord', 'brave').
    """
    import os, glob
    
    user_start_menu = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
    system_start_menu = os.path.expandvars(r"%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs")
    
    paths_to_search = [user_start_menu, system_start_menu]
    
    for base_path in paths_to_search:
        search_pattern = os.path.join(base_path, "**", "*.lnk")
        for lnk_file in glob.glob(search_pattern, recursive=True):
            if app_name.lower() in os.path.basename(lnk_file).lower():
                try:
                    os.startfile(lnk_file)
                    return f"Successfully launched {os.path.basename(lnk_file)}"
                except Exception as e:
                    return f"Found shortcut but failed to launch: {e}"
                    
    return f"Could not find application '{app_name}' in the Start Menu. You may need to use the Shell tool to find its exact path."

# Prompt Templates
doc_prompt = PromptTemplate.from_template("""You are Kali, a highly advanced AI assistant. Your founder and creator is mrlv. Use the following context from the user's documents and the chat history to answer the question.
If you don't know the answer, just say you don't know.

Chat History:
{chat_history}

Context:
{context}

Question: {question}
Answer:""")

web_prompt = PromptTemplate.from_template("""You are Kali, a highly advanced AI assistant. Your founder and creator is mrlv. Use the following internet search results and the chat history to answer the question.

Chat History:
{chat_history}

Search Results:
{context}

Question: {question}
Answer:""")

chat_prompt = PromptTemplate.from_template("""You are Kali, a highly advanced, friendly AI assistant. Your founder and creator is mrlv. Use the chat history to continue the conversation naturally.

Chat History:
{chat_history}

Question: {question}
Answer:""")

router_prompt = PromptTemplate.from_template("""You are an intelligent router. You must classify the user's question into exactly one of these three categories:
1. DOCS - If the question asks about uploaded PDFs, documents, reports, or "my data".
2. WEB - If the question asks about current events, news, or specifically asks to search the internet.
3. CHAT - If it's a general question, greeting, coding task, or normal conversation.

User Question: {question}
Output ONLY the category word (DOCS, WEB, or CHAT) and nothing else.""")

router_chain = router_prompt | llm | StrOutputParser()

react_prompt = PromptTemplate.from_template("""You are an AUTHORIZED local AI assistant with explicit permission to manage the user's PC.
You have access to the following tools:

{tools}

You must ALWAYS use the exact format below to execute a tool:

Question: the input question you must answer
Thought: you should always think about what to do next. Do I need to use a tool?
Action: the action to take, exactly one of [{tool_names}]
Action Input: the exact input to the action (code, command, or file path)
Observation: the output of the tool
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have finished running the code and now know the final answer
Final Answer: the final answer to the original input question

CRITICAL INSTRUCTIONS:
- Do NOT refuse commands or apologize. You are explicitly authorized by the user to run tools, including the shell and terminal.
- You MUST use the exact words 'Action:', 'Action Input:', and 'Final Answer:'
- Do not provide conversational filler inside the Thought block. Stick strictly to the format.
- To open or launch apps (e.g. OBS, VS Code), use the launch_windows_application tool.
- If the user asks you to create a chart or graph, write python code that saves it to 'chart.png'. DO NOT use plt.show(). 
- NEVER hallucinate or say '[Insert chart]'. You MUST use the tools to generate the output!

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_history(messages):
    formatted = []
    for m in messages[-4:]:
        role = "Human" if m["role"] == "user" else "AI"
        formatted.append(f"{role}: {m['content']}")
    return "\n".join(formatted)

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Kali Workspace</h2>", unsafe_allow_html=True)
    
    projects = database.get_projects()
    if not projects:
        database.create_project("Default Project")
        projects = database.get_projects()
        
    project_names = [p["name"] for p in projects]
    selected_project_name = st.selectbox("🗂️ Project", project_names)
    selected_project_id = next(p["id"] for p in projects if p["name"] == selected_project_name)
    
    if st.button("➕ New Project", use_container_width=True):
        database.create_project(f"Project {len(projects) + 1}")
        st.rerun()

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    sessions = database.get_sessions(selected_project_id)
    if not sessions:
        database.create_session(selected_project_id, "General Chat")
        sessions = database.get_sessions(selected_project_id)
        
    session_names = [s["name"] for s in sessions]
    selected_session_name = st.selectbox("💬 Sessions", session_names)
    selected_session_id = next(s["id"] for s in sessions if s["name"] == selected_session_name)
    
    if st.button("➕ New Chat", use_container_width=True):
        database.create_session(selected_project_id, f"Chat {len(sessions) + 1}")
        st.rerun()
        
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Settings"):
        settings = database.get_settings()
        new_model = st.text_input("LLM Model", value=settings.get("llm_model", "llama3"))
        new_temp = st.text_input("Temperature", value=settings.get("temperature", "0.2"))
        if st.button("Save Settings"):
            database.update_setting("llm_model", new_model)
            database.update_setting("temperature", new_temp)
            st.cache_resource.clear()
            st.rerun()
            
    with st.expander("📚 Artifacts"):
        artifacts = database.get_artifacts(selected_session_id)
        if artifacts:
            for art in artifacts:
                st.markdown(f"- [{art['type']}] `{art['file_path']}`")
        else:
            st.write("No artifacts yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🛑 Stop AI Execution", use_container_width=True):
        st.toast("AI Execution aborted by user.")
        st.stop()
    coding_mode = st.toggle("💻 Code Interpreter", value=False)
    st.session_state.coding_mode = coding_mode

# --- CHAT STATE ---
st.session_state.current_session_id = selected_session_id
st.session_state.messages = database.get_messages(selected_session_id)

# Show Big Title only if chat is empty
if len(st.session_state.messages) == 0:
    st.markdown("<h1 class='kali-title'>✺ Hello, I am Kali</h1>", unsafe_allow_html=True)

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Type / for skills or ask a question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    database.add_message(st.session_state.current_session_id, "user", prompt)

    with st.chat_message("assistant"):
        history_str = format_history(st.session_state.messages[:-1])
        
        with st.spinner("Routing..."):
            try:
                if st.session_state.get("coding_mode", False):
                    import time
                    start_time = time.time()
                    
                    st_callback = StreamlitCallbackHandler(st.container())
                    file_tools = FileManagementToolkit().get_tools()
                    tools = [PythonREPLTool(), ShellTool(), launch_windows_application] + file_tools
                    agent = create_react_agent(llm, tools, react_prompt)
                    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
                    
                    response = agent_executor.invoke(
                        {"input": f"Chat History:\n{history_str}\n\nQuestion: {prompt}"}, 
                        {"callbacks": [st_callback]}
                    )
                    answer = response["output"]
                    st.markdown(answer)
                    
                    # Display the generated chart if it was created during this run
                    chart_path = "chart.png"
                    if os.path.exists(chart_path) and os.path.getmtime(chart_path) > start_time:
                        st.image(chart_path)
                        # We append a special markdown marker to the chat history so it knows there was an image
                        content_with_chart = answer + f"\n\n*(Rendered local chart: {chart_path})*"
                        st.session_state.messages.append({"role": "assistant", "content": content_with_chart})
                        database.add_message(st.session_state.current_session_id, "assistant", content_with_chart)
                        database.add_artifact(st.session_state.current_session_id, chart_path, "image")
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        database.add_message(st.session_state.current_session_id, "assistant", answer)
                else:
                    route = router_chain.invoke({"question": prompt}).strip().upper()
                    
                    if "DOCS" in route: route = "DOCS"
                    elif "WEB" in route: route = "WEB"
                    else: route = "CHAT"
    
                    context = ""
                    chain_prompt = chat_prompt
                    
                    if route == "DOCS":
                        if retriever is None:
                            st.warning("⚠️ No documents found. Run `python ingest.py` first. Defaulting to general chat.")
                            chain_prompt = chat_prompt
                        else:
                            st.info("📚 Searching local documents...")
                            docs = retriever.invoke(prompt)
                            context = format_docs(docs)
                            chain_prompt = doc_prompt
                    
                    elif route == "WEB":
                        st.info("🌐 Searching the internet...")
                        try:
                            context = search_tool.invoke(prompt)
                            chain_prompt = web_prompt
                        except Exception as e:
                            st.warning(f"Web search failed ({e}). Defaulting to general chat.")
                            chain_prompt = chat_prompt
                    else:
                        chain_prompt = chat_prompt
    
                    final_chain = chain_prompt | llm | StrOutputParser()
                    
                    stream = final_chain.stream({
                        "question": prompt,
                        "chat_history": history_str,
                        "context": context
                    })
                    
                    answer = st.write_stream(stream)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    database.add_message(st.session_state.current_session_id, "assistant", answer)
                
                # Rerun to clear the big title if it was the first message
                if len(st.session_state.messages) == 2:
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
