from fastapi import FastAPI
import httpx
import traceback
from backend.validation import ExecutionPlan, Action, UserRequest
from agent.planner import generate_execution_plan
from backend import execution

app = FastAPI(title="Discord Agent Orchestrator")

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Discord Orchestrator Backend"}

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return {"test": "success", "message": "Backend API is working!"}

@app.post("/execute-simple", response_model=ExecutionPlan)
async def execute_command_simple(request: UserRequest):
    """
    Simple test endpoint - bypasses AI to test the flow
    """
    print(f"\n📨 [SIMPLE] Received request: {request.content}")
    
    return ExecutionPlan(
        thought_process="Simple test - no AI involved",
        actions=[],
        final_response=f"✅ Received your request: '{request.content}'. Simple endpoint test successful!"
    )

@app.post("/execute", response_model=ExecutionPlan)
async def execute_command(request: UserRequest):
    """
    Receives a natural language command from the bot, 
    processes it via the Agent, 
    and executes the resulting plan.
    """
    print(f"\n📨 Received request from {request.user_id} in {request.guild_id}: {request.content}")

    try:
        # 1. Call Agent to get ExecutionPlan
        print("🤖 Calling AI Agent to generate plan...")
        plan = await generate_execution_plan(request.content, request.guild_id)
        print(f"✅ Plan generated: {plan.thought_process}")
        print(f"📋 Actions to execute: {len(plan.actions)}")
        
        # 2. Execute Actions in the Plan (if any)
        if plan.actions:
            async with httpx.AsyncClient() as client:
                for action in plan.actions:
                    try:
                        print(f"⚙️  Executing action: {action.action_type}")
                        print(f"    Action details: {action}")
                        await execute_action(action, request.guild_id, client)
                        print(f"✅ Action completed: {action.action_type}")
                    except Exception as e:
                        error_msg = f"Failed to execute action {action.action_type}: {str(e)}"
                        print(f"❌ {error_msg}")
                        import traceback
                        traceback.print_exc()
        else:
            print("ℹ️  No actions to execute")

        print(f"✅ Request completed. Response: {plan.final_response}\n")
        return plan

    except Exception as e:
        error_msg = f"Backend error: {str(e)}"
        print(f"❌ {error_msg}")
        traceback.print_exc()
        
        # Return error response
        return ExecutionPlan(
            thought_process=f"Backend error occurred: {str(e)}",
            actions=[],
            final_response=f"⚠️ Error processing your request: {str(e)}"
        )

# Helper to map actions to execution functions
async def execute_action(action: Action, guild_id: int, client):
    print(f"\n   🔍 Processing action type: {action.action_type}")
    
    try:
        if action.action_type == "create_role":
            print(f"   📋 Creating role: {action.name}")
            result = await execution.create_role(guild_id, action.dict(include={"name", "color", "permissions", "hoist", "mentionable"}), client)
            print(f"   ✅ Role created: {result}")
        elif action.action_type == "create_channel":
            print(f"   📋 Creating channel: {action.name}")
            result = await execution.create_channel(guild_id, action.dict(include={"name", "type", "topic", "category"}), client)
            print(f"   ✅ Channel created: {result}")
        elif action.action_type == "delete_role":
            await execution.delete_role(guild_id, action.name, client)
        elif action.action_type == "delete_channel":
            await execution.delete_channel(guild_id, action.name, client)
        elif action.action_type == "create_invite":
            await execution.create_invite(guild_id, action.channel_name, action.max_uses, action.expires_in_minutes, client)
        elif action.action_type == "kick_user":
            await execution.remove_user(guild_id, action.user_id, client)
        elif action.action_type == "ban_user":
            await execution.ban_user(guild_id, action.user_id, client)
        elif action.action_type == "unban_user":
            await execution.unban_user(guild_id, action.user_id, client)
        elif action.action_type == "mute_user":
            await execution.mute_user(guild_id, action.user_id, True, client)
        elif action.action_type == "unmute_user":
            await execution.mute_user(guild_id, action.user_id, False, client)
        else:
            print(f"   ⚠️  Unknown action type: {action.action_type}")
    except Exception as e:
        print(f"   ❌ Error executing {action.action_type}: {str(e)}")
        raise

