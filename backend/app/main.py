from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.webrtc import handle_webrtc
from app.vision import predict_component
from app.audio_stt import transcribe_audio
from app.langchain_flow import graph
from app.schemas import SDP

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/offer")
async def offer(sdp: SDP):
    """
    Receive SDP offer from client, return SDP answer.
    """
    answer = await handle_webrtc(sdp.dict())
    return {"sdp": answer.sdp, "type": answer.type}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """
    Receive binary video/audio chunks, process, and send back JSON results.
    """
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_bytes()
            # Simple protocol: assume video chunk first then audio chunk.
            # For illustration, treat all binary as video.
            component_id = predict_component(msg)
            steps = graph.run(component_id)
            await ws.send_json({"overlay": steps})
    except WebSocketDisconnect:
        pass
