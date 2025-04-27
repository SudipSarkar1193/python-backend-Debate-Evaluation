from services.prompt import get_evaluation_prompt
from langchain_core.output_parsers import PydanticOutputParser
from models.pydantic_models import EvaluationResponse


parser = PydanticOutputParser(pydantic_object=EvaluationResponse)

prompt = get_evaluation_prompt()

ip = {
    "topic": "Climate change is a global crisis",
    "statement": "Climate change is caused by only human activity",
    "user_id": 1,
    "history": [],
    "format_instructions": parser.get_format_instructions()
}

prompt_value = prompt.invoke(ip)
print("Prompt messages:")
print()
print(prompt_value)
print("")
print("_____________________________________")
print("")
for msg in prompt_value.messages:
    print(f"- {msg.__class__.__name__}: {msg.content}")