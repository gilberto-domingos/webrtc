import asyncio
from aiortc import RTCPeerConnection, VideoStreamTrack
import cv2
import streamlit as st
from aiortc.contrib.media import MediaPlayer


class VideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        ret, frame = self.cap.read()
        if ret:
            return frame


async def create_offer():
    pc = RTCPeerConnection()

    video_track = VideoTrack()
    pc.addTrack(video_track)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    return pc, offer


async def main():
    pc, offer = await create_offer()

    st.title("WebRTC Offer")
    st.text("Oferta gerada pelo servidor:")
    st.text(offer.sdp)

    await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
