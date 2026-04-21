from flask import Flask, request, jsonify
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio

app = Flask(__name__)

APP_ID = ""
APP_PASSWORD = ""

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)


async def bot_logic(turn_context: TurnContext):
    text = turn_context.activity.text
    await turn_context.send_activity(f"Echo: {text}")


@app.route("/api/messages", methods=["POST"])
def messages():
    print("🔥 REQUEST RECEIVED")

    if "application/json" not in request.headers.get("Content-Type", ""):
        return "Unsupported Media Type", 415

    activity = Activity().deserialize(request.json)
    auth_header = request.headers.get("Authorization", "")

    async def aux_func(turn_context):
        await bot_logic(turn_context)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        adapter.process_activity(activity, auth_header, aux_func)
    )

    return jsonify({})


@app.route("/")
def home():
    return "Bot is running!"