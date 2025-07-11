# -*- coding=utf-8 -*-
r"""

"""
import struct
import asyncio
import typing as t


__all__ = ['ScanResult', 'AsyncReadableBuffer', 'ClamAVError', 'ClamAVConnectionError', 'ClamAVScanError', 'ClamAVAsyncClient']


class ScanResult(t.NamedTuple):
    save: bool
    virus_name: t.Optional[str]


@t.runtime_checkable
class AsyncReadableBuffer(t.Protocol):
    async def read(self, size: int) -> bytes: ...


class ClamAVError(Exception):
    pass


class ClamAVConnectionError(ClamAVError, ConnectionError):
    pass


class ClamAVScanError(ClamAVError):
    pass


class ClamAVAsyncClient:
    def __init__(self, host: str = "localhost", port: int = 3310):
        self._host: str = host
        self._port: int = port
        self.chunk_size = 1024 * 64  # 64 KB

    async def scan_abuffer(self, buffer: AsyncReadableBuffer) -> ScanResult:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port), timeout=3.0,
            )
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
            raise ClamAVConnectionError(f"Failed to connect to ClamAV at {self._host}:{self._port}") from e

        try:
            # Send INSTREAM command
            writer.write(b'nINSTREAM\n')
            await writer.drain()

            while True:
                chunk = await buffer.read(self.chunk_size)
                if not chunk:
                    break

                writer.write(struct.pack('!I', len(chunk)) + chunk)
                await writer.drain()

            # End of stream
            writer.write(struct.pack('!I', 0))
            await writer.drain()

            # Await response
            response_line = await asyncio.wait_for(reader.readline(), timeout=5.0)
            response = response_line.decode().strip()

            # Example: "stream: OK" or "stream: Eicar-Test-Signature FOUND"
            if not response.startswith("stream:"):
                raise ClamAVScanError(f"Unexpected response from ClamAV: {response}")

            _, result = response.split(":", 1)
            result = result.strip()

            if result == "OK":
                return ScanResult(save=True, virus_name=None)
            elif result.endswith("FOUND"):
                virus_name = result.replace("FOUND", "").strip()
                return ScanResult(save=False, virus_name=virus_name)
            else:
                raise ClamAVScanError(f"ClamAV returned an unrecognized response: {result}")

        finally:
            writer.close()
            await writer.wait_closed()
