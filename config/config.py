from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompt import Prompt
from dotenv import load_dotenv
load_dotenv()


class Agent:

    def __init__(self):
        self.models = {
            "gemini-flash": ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        }
        self.output_parser = {
            "json": JsonOutputParser()
        }

    def classify_query(self, user_input: str, user_data: str, model_name="gemini-flash", parser_name="json"):
        prompt = Prompt()

        # Build prompt parts
        system_input = prompt.system_prompt()
        user_prompt = prompt.user_prompt(user_data, user_input)

        # Get model and parser
        llm = self.models[model_name]
        parser = self.output_parser[parser_name]

        # Prompt formatting
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{system_input}"),
            ("user", "{user_prompt}")
        ])
        formatted_prompt = prompt_template.invoke({
            "system_input": system_input,
            "user_prompt": user_prompt
        })

        # Invoke LLM and parse output
        response = llm.invoke(formatted_prompt)
        content = response.content

        parsed_output = parser.parse(content)
        return parsed_output

    def model_list(self):
        return list(self.models.keys())

    def output_parser_list(self):
        return list(self.output_parser.keys())
