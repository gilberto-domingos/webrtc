import asyncio
import websockets
from aiortc import RTCPeerConnection, VideoStreamTrack
import json
import cv2


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

    return offer.sdp


async def handle_client(websocket, path):
    # Cria a oferta
    offer = await create_offer()

    # Envia a oferta para o cliente via WebSocket
    await websocket.send(json.dumps({"offer": offer}))

    print("Oferta enviada para o cliente")

    # Mantenha a conexão aberta
    await websocket.wait_closed()

# Inicia o servidor WebSocket


async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
