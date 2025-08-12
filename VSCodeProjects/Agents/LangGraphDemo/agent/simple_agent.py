from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import tool
import os
import re

class SimpleAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAIKEY"))
        self.tools = [
            Tool.from_function(
                func=self.addition_tool,
                name="addition_tool",
                description="Add two numbers. Usage: addition_tool(number1, number2)"
            ),
            Tool.from_function(
                func=self.subtraction_tool,
                name="subtraction_tool",
                description="Subtract two numbers. Usage: subtraction_tool(number1, number2)"
            ),
            Tool.from_function(
                func=self.multiplication_tool,
                name="multiplication_tool",
                description="Multiply two numbers. Usage: multiplication_tool(number1, number2)"
            ),
            Tool.from_function(
                func=self.division_tool,
                name="division_tool",
                description="Divide two numbers. Usage: division_tool(number1, number2). Returns error if dividing by zero."
            )
        ]
        self.agent = self.initialize_agent()

    @tool
    def addition_tool(self, number1: str, number2: str) -> int:
        """Add two numbers."""
        try:
            num1 = int(number1)
            num2 = int(number2)
            return num1 + num2
        except ValueError:
            return "Error: Inputs must be valid integers."

    @tool
    def subtraction_tool(self, number1: str, number2: str) -> int:
        """Subtract two numbers."""
        try:
            num1 = int(number1)
            num2 = int(number2)
            return num1 - num2
        except ValueError:
            return "Error: Inputs must be valid integers."

    @tool
    def multiplication_tool(self, number1: str, number2: str) -> int:
        """Multiply two numbers."""
        try:
            num1 = int(number1)
            num2 = int(number2)
            return num1 * num2
        except ValueError:
            return "Error: Inputs must be valid integers."

    @tool
    def division_tool(self, number1: str, number2: str) -> str:
        """Divide two numbers."""
        try:
            num1 = int(number1)
            num2 = int(number2)
            if num2 == 0:
                return "Division by zero is not allowed."
            return str(num1 / num2)
        except ValueError:
            return "Error: Inputs must be valid integers."

    def initialize_agent(self):
        system_message = (
            "You are a math assistant. From the input question, extract exactly two numbers and identify the operation (add, subtract, multiply, divide). "
            "Call the appropriate tool with the two numbers as separate parameters: number1 and number2. "
            "For example, for 'What is 5 plus 3?', call addition_tool(number1='5', number2='3'). "
            "Ensure the numbers are passed as strings and the tool handles conversion to integers."
        )
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={"system_message": system_message}
        )

    def preprocess_question(self, question: str) -> str:
        """Preprocess the question to help the agent extract numbers."""
        # Replace common number words with digits
        number_words = {
            "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
            "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
        }
        question = question.lower()
        for word, digit in number_words.items():
            question = question.replace(word, digit)
        
        # Normalize common patterns (e.g., "2, 2" to "2 and 2")
        question = re.sub(r'(\d+),\s*(\d+)', r'\1 and \2', question)
        
        return question

    def ask(self, question: str):
        """Preprocess the question before passing it to the agent."""
        processed_question = self.preprocess_question(question)
        return self.agent.run(processed_question)