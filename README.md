# 🧮 Text-to-Math Problem Solver using LangChain + Groq

This project implements an intelligent **Text-to-Math Problem Solver** that can **understand mathematical problems written in natural language** and provide accurate solutions using **LangChain**, **Groq**, and a built-in **Calculator Tool**.

It combines the reasoning ability of **LLMs (Large Language Models)** with the precision of a mathematical calculator — enabling users to type any math-related query in plain English and get both **step-by-step reasoning** and the **final numerical answer**.

---

## 🚀 Features

- 🧠 Converts **natural language math problems** into solvable expressions.
- ⚙️ Uses **LangChain (v0.2+)** for modular AI architecture.
- ⚡ Powered by **Groq API** (ultra-fast inference with Llama 3.3).
- 🧮 Integrates a **custom Calculator Tool** for accurate arithmetic.
- 💬 Supports **interactive chat** for multi-turn problem-solving.
- 🧾 Outputs both **reasoning steps** and **final answers** clearly.

---

## 🧩 Example Interactions

```bash
User: I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. 
      Then I buy a dozen apples and 2 packs of blueberries (25 each). 
      How many total pieces of fruit do I have?

AI: You now have 69 pieces of fruit.

---

User: What is the area of a square with one side length = 4 cm?

AI: The area of the square is 16 square centimeters.

🧰 Core Components
🧩 1. LangChain

Used for building the agent and tool management pipeline.

⚙️ 2. Groq Model

High-speed Llama-3.3 model that processes reasoning efficiently:

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

🧮 3. Calculator Tool

Safely evaluates mathematical expressions provided by the LLM:

Tool(
    name="Calculator",
    func=lambda expression: eval(expression),
    description="Use this tool to perform arithmetic operations."
)

🧠 4. Create Agent

Manages conversation flow, reasoning, and tool calls

🧑‍💻 Author

Jayant Deshwal
Department of Computer Science and Engineering
Galgotias College of Engineering and Technology
📧 jayant.deshwal.56@gmail.com

🪪 License

This project is open-source and distributed under the MIT License.
