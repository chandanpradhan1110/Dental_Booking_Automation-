"""
Dental Appointment System — Flask Web Application
Powered by LangGraph + Grok-4 (xAI)
"""
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from langchain_core.messages import HumanMessage, AIMessageChunk, AIMessage
import json
import traceback

from dental_agent.agent import dental_graph

app = Flask(__name__)

# In-memory session history (for single-user local use)
# For multi-user, use Flask sessions or a DB
conversation_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    conversation_history.append(HumanMessage(content=user_input))

    def generate():
        global conversation_history
        final_messages = None
        buffer = []

        try:
            for event_type, event_data in dental_graph.stream(
                {"messages": conversation_history},
                stream_mode=["messages", "values"],
                config={"recursion_limit": 20},
            ):
                if event_type == "messages":
                    chunk, meta = event_data
                    if (
                        isinstance(chunk, AIMessageChunk)
                        and chunk.content
                        and not getattr(chunk, "tool_calls", None)
                    ):
                        token = chunk.content
                        buffer.append(token)
                        yield f"data: {json.dumps({'token': token})}\n\n"

                elif event_type == "values":
                    final_messages = event_data.get("messages", [])

        except Exception as exc:
            conversation_history.pop()
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
            return

        if final_messages:
            conversation_history = final_messages

        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)