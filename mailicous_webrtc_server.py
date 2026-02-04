import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay
pcs = set()
relay = MediaRelay()
async def index(request):
    content = open("streamer.html", "r").read()
    return web.Response(content_type="text/html", text=content)
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pcs.add(pc)
    @pc.on("track")
    def on_track(track):
        print(f"🔹 Track {track.kind} received")
        if track.kind in ["video", "audio"]:
            pc.addTrack(relay.subscribe(track))
        @track.on("ended")
        async def on_ended():
            print(f"🔹 Track {track.kind} ended")
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })
async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()
app = web.Application()
app.on_shutdown.append(on_shutdown)
app.router.add_get("/", index)
app.router.add_post("/offer", offer)
web.run_app(app, port=8455)