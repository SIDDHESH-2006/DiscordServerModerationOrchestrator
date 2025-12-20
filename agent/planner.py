from langchain_openai import ChatOpenAI
from backend.validation import ExecutionPlan
from agent.prompts import PROMPT_TEMPLATE
from agent.utils import get_openai_api_key

# Initialize LLM
# We use a temperature of 0 for deterministic, reliable action planning.
llm = ChatOpenAI(
    model="gpt-4-turbo",  # Or gpt-3.5-turbo if cost is a concern, but 4 is better for planning
    temperature=0,
    api_key=get_openai_api_key()
)

# Create the structured chain
# with_structured_output forces the LLM to adhere to the Pydantic schema
planner_chain = PROMPT_TEMPLATE | llm.with_structured_output(ExecutionPlan)

async def generate_execution_plan(user_input: str, guild_id: int) -> ExecutionPlan:
    """
    Generates a structured execution plan from natural language input.
    """
    print(f"Agent Planning for: '{user_input}' (Guild: {guild_id})")
    
    try:
        # Invoke the chain
        plan = await planner_chain.ainvoke({
            "user_input": user_input, 
            "guild_id": guild_id
        })
        return plan
    except Exception as e:
        # Fallback error handling
        print(f"Error generating plan: {e}")
        return ExecutionPlan(
            thought_process=f"An error occurred while planning: {str(e)}",
            actions=[],
            final_response="I encountered an internal error while trying to process your request."
        )
