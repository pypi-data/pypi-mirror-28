from asyncio import shield
import websockets

import logging
logger = logging.getLogger(__name__)

from s2clientprotocol import sc2api_pb2 as sc_pb

from .data import Status
from .player import Computer

class ProtocolError(Exception):
    pass

class Protocol(object):
    def __init__(self, ws):
        assert ws
        self._ws = ws
        self._status = None

    async def __request(self, request):
        logger.debug(f"Sending request: {request !r}")
        await self._ws.send(request.SerializeToString())
        logger.debug(f"Request sent")

        response = sc_pb.Response()
        try:
            response_bytes = await self._ws.recv()
        except websockets.exceptions.ConnectionClosed:
            logger.exception("Connection already closed.")
            raise ProtocolError("Connection already closed.")
        response.ParseFromString(response_bytes)
        logger.debug(f"Response received")
        return response

    async def _execute(self, **kwargs):
        assert len(kwargs) == 1, "Only one request allowed"

        request = sc_pb.Request(**kwargs)

        response = await shield(self.__request(request))

        new_status = Status(response.status)
        if new_status != self._status:
            logger.info(f"Client status changed to {new_status} (was {self._status})")
        self._status = new_status

        if response.error:
            if response.HasField("error_details"):
                logger.debug(f"Response contained an error: {response.error}: {response.error_details}")
            else:
                logger.debug(f"Response contained an error: {response.error}")
            raise ProtocolError(f"{response.error}")

        return response

    async def ping(self):
        result = await self._execute(ping=sc_pb.RequestPing())
        return result

    async def leave(self):
        try:
            await self._execute(leave_game=sc_pb.RequestLeaveGame())
        except websockets.exceptions.ConnectionClosed:
            pass

    async def quit(self):
        try:
            await self._execute(quit=sc_pb.RequestQuit())
        except websockets.exceptions.ConnectionClosed:
            pass
