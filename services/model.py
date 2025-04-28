from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from services.prompt import get_evaluation_prompt
from config import Config
from models.pydantic_models import EvaluationResponse
from services.memory import MemoryManager
import logging


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DebateEvaluator:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3
        )
        self.prompt = get_evaluation_prompt()
        self.parser = PydanticOutputParser(pydantic_object=EvaluationResponse)
        
        self.chain = self.prompt | self.model | self.parser

    def evaluate_statement(self, topic: str, statement: str, user_id: int, memory: 'ConversationBufferWindowMemory',in_favour_string: str = None ,session_store = None,session_id : str =None) -> EvaluationResponse:
        try:
            # Invoke chain with memory's history
            response = self.chain.invoke({
                "topic": topic,
                "statement": statement,
                "user_id": user_id,
                "history": memory.load_memory_variables({})["history"],
                "format_instructions": self.parser.get_format_instructions(),
                "in_favour_string": in_favour_string
            })

            # Save statement and response to memory
            memory.save_context(
                inputs={"input": f"User {user_id}: {statement} (Stance: {in_favour_string})"},
                outputs={"output": response.json()}
            )
            
            #debug :
            logger.debug("*********************************************")
            MemoryManager.print_current_memory(session_store,session_id)
            logger.debug("*********************************************")
            
            return response
        except Exception as e:
            logger.error(f"Error evaluating statement: {str(e)}")
            raise Exception(f"Error evaluating statement: {str(e)}")