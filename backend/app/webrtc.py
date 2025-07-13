import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole

pcs = set()

async def handle_webrtc(offer: dict):
    """
    Create RTCPeerConnection, accept offer, return answer.
    """
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("track")
    async def on_track(track):
        # We receive tracks but actual frame handling is in /ws
        media_blackhole = MediaBlackhole()
        await media_blackhole.start(track)

    # set remote and local descriptions
    await pc.setRemoteDescription(RTCSessionDescription(sdp=offer["sdp"], type=offer["type"]))
    for t in pc.getTransceivers():
        pc.addTransceiver(t.kind, direction="recvonly")
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    # cleanup after 5 minutes
    asyncio.get_event_loop().call_later(300, lambda: asyncio.ensure_future(pc.close()))
    return pc.localDescription
