from fastapi import APIRouter
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole


router = APIRouter()

pcs = set()

def create_local_tracks():
    options = {"framerate": "30", "video_size": "680x480"}
    webcam = MediaPlayer("video=OBS Virtual Camera", format="dshow", options=options)
    relay = MediaRelay()
    return None, relay.subscribe(webcam.video)

### OFFER
from pydantic import BaseModel
class Offer(BaseModel):
    sdp: str
    type: str
    video_transform: str = None


@router.post("/offer")
async def offer(params: Offer):
    
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)
    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    audio, video = create_local_tracks()

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


async def on_shutdown(router):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()