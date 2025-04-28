from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

def get_evaluation_prompt():
    system_message = SystemMessagePromptTemplate.from_template(
        """
        You are an expert debate evaluator. Your task is to evaluate a user's debate statement for factual accuracy and relevance to the given topic, considering the conversation history and the user's stance (in favor or against). Return a JSON response according to the provided format instructions. Use the conversation history to assess context, ensuring the statement responds appropriately to prior statements. For factual accuracy, provide a list of credible source URLs or references (e.g., scientific journals, reputable news, or reports) that support your evaluation. If specific URLs are unavailable, suggest authoritative sources (e.g., 'IPCC reports', 'WHO guidelines').

        {format_instructions}
        """
    )
    history_placeholder = MessagesPlaceholder(variable_name="history")
    human_message = HumanMessagePromptTemplate.from_template(
        """
        Topic: {topic}
        User {user_id} Statement: {statement}
        User Stance: {in_favour_string}

        Evaluate the statement and return the result in JSON format.
        """
    )
    return ChatPromptTemplate.from_messages([system_message, history_placeholder, human_message])