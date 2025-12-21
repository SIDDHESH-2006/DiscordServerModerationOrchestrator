from langchain_openai import ChatOpenAI
from backend.validation import ExecutionPlan
from agent.prompts import PROMPT_TEMPLATE
from agent.utils import get_openai_api_key

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=get_openai_api_key()
)

planner_chain = PROMPT_TEMPLATE | llm.with_structured_output(ExecutionPlan)

async def generate_execution_plan(user_input: str, guild_id: int) -> ExecutionPlan:
    print(f"Agent Planning for: '{user_input}' (Guild: {guild_id})")
    try:
        plan = await planner_chain.ainvoke({
            "user_input": user_input,
            "guild_id": guild_id
        })
        return plan
    except Exception as e:
        print(f"Error generating plan: {e}")
        return ExecutionPlan(
            thought_process=f"An error occurred while generating the execution plan: {str(e)}",
            actions=[],
            final_response="I encountered an internal error while trying to understand your request."
        )
