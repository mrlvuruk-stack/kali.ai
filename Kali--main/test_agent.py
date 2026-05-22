from langchain_community.llms import Ollama
from langchain_experimental.tools import PythonREPLTool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="llama3", temperature=0.1)
tools = [PythonREPLTool()]

react_prompt = PromptTemplate.from_template("""You are an advanced Python coding assistant.
You have access to the following tools:

{tools}

You must ALWAYS use the exact format below to execute code. NEVER output anything else outside this format.

Question: the input question you must answer
Thought: you should always think about what to do next. Do I need to use a tool?
Action: the action to take, exactly one of [{tool_names}]
Action Input: the exact python code to run
Observation: the output of the python code
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have finished running the code and now know the final answer
Final Answer: the final answer to the original input question

Here is a strict example of how you MUST behave:
---
Question: draw a chart of the first 5 fibonacci numbers
Thought: I need to write a python script to calculate the numbers and save a chart.
Action: Python_REPL
Action Input: 
import matplotlib.pyplot as plt
fib = [0, 1, 1, 2, 3]
plt.bar(range(5), fib)
plt.savefig('chart.png')
Observation: 
Thought: I have finished running the code and now know the final answer.
Final Answer: Here is your chart!
---

CRITICAL INSTRUCTIONS:
- You MUST use the exact words 'Action:', 'Action Input:', and 'Final Answer:'
- If the user asks you to create a chart or graph, you MUST write python code that saves it to 'chart.png' using matplotlib. DO NOT use plt.show(). 
- NEVER hallucinate or say '[Insert chart]'. You MUST write and execute the python code!

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

agent = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)

try:
    response = agent_executor.invoke({"input": "draw the Fibonacci chart"})
    print("FINAL OUTPUT:", response["output"])
except Exception as e:
    print("ERROR:", e)
