from agent.planner import generate_execution_plan
import backend.execution as execution
# import logging 

app = FastAPI(title="Discord Agent Orchestrator")

# Setup logging (basic)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Discord Orchestrator Backend"}

@app.post("/execute", response_model=ExecutionPlan)
async def execute_command(request: UserRequest):
    """
    Receives a natural language command from the bot, 
    processes it via the Agent, 
    and executes the resulting plan.
    """
    print(f"Received request from {request.user_id} in {request.guild_id}: {request.content}")

    # 1. Call Agent to get ExecutionPlan
    plan = await generate_execution_plan(request.content, request.guild_id)
    
    # 2. Execute Actions in the Plan (if any)
    # We pass the client implicitly or need to manage a global client session? 
    # For now, let's assume one-off requests or shared client.
    # execution.py functions normally take a 'client' arg.
    # We should create a client content context for this request.
    import httpx
    async with httpx.AsyncClient() as client:
        for action in plan.actions:
            try:
                await execute_action(action, request.guild_id, client)
            except Exception as e:
                print(f"Failed to execute action {action}: {e}")
                # We might want to append errors to the final response?

    return plan

# Helper to map actions to execution functions
async def execute_action(action: Action, guild_id: int, client):
    if action.action_type == "create_role":
        await execution.create_role(guild_id, action.dict(include={"name", "color", "permissions", "hoist", "mentionable"}), client)
    elif action.action_type == "create_channel":
        await execution.create_channel(guild_id, action.dict(include={"name", "type", "topic", "category"}), client)
    elif action.action_type == "delete_role":
        await execution.delete_role(guild_id, action.name, client)
    elif action.action_type == "delete_channel":
        await execution.delete_channel(guild_id, action.name, client)
    elif action.action_type == "create_invite":
        await execution.create_invite(guild_id, action.channel_name, action.max_uses, action.expires_in_minutes, client)
    # TODO: Add moderation actions

