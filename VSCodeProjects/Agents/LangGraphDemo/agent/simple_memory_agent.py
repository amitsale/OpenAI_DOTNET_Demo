from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

class ConversationalAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAIKEY")
        self.llm = ChatOpenAI(temperature=0, model="gpt-4",openai_api_key=self.openai_api_key)

        # ✅ Step 1: Define memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # ✅ Step 2: Define tool
        def echo_tool(text):
            return f"Echo: {text}"

        self.tools = [
            Tool(
                name="EchoTool",
                func=echo_tool,
                description="Useful for echoing the input string."
            )
        ]

        # ✅ Step 3: Define a custom prompt that includes {chat_history}
        self.prompt = PromptTemplate(
            input_variables=["input", "chat_history"],
            template="""
                        You are a helpful assistant. Use the conversation history to answer the user's question.

                        Chat History:
                        {chat_history}

                        User: {input}
                        Assistant:
                        """
        )

        # ✅ Step 4: Initialize agent with memory + prompt
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )

    def ask(self, question: str):
        return self.agent.run(question)


# ✅ Testing the class
if __name__ == "__main__":
    assistant = ConversationalAgent()
    print("\n--- Round 1 ---")
    print(assistant.ask("What is your name?"))

    print("\n--- Round 2 ---")
    print(assistant.ask("What did I just ask you?"))  # Should use memory