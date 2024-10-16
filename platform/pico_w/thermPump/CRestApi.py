import asyncio
import json

class RestMethods():
    GET = "GET"
    POST = "POST"

class CRestApi:
    def __init__(self, port=80):
        self.port = port
        self.routes = {}
        self.server = None
        self.server_task = None

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    async def parse_request(self, reader):
        request_line = await reader.readline()
        method, path, _ = request_line.decode().strip().split()

        headers = {}
        while True:
            header_line = await reader.readline()
            if header_line == b"\r\n":
                break
            header_key, header_value = header_line.decode().strip().split(": ", 1)
            headers[header_key] = header_value

        content_length = int(headers.get("Content-Length", 0))
        body = await reader.read(content_length) if content_length > 0 else b""

        return method, path, headers, body

    async def handle_client(self, reader, writer):
        try:
            method, path, headers, body = await self.parse_request(reader)
            handler = self.routes.get((method, path))

            if handler:
                response = {}
                if method == RestMethods.POST:
                    try:
                        data = json.loads(body.decode())
                        response = handler(data)
                        status_code = 200
                    except json.JSONDecodeError:
                        response = {"error": "Invalid JSON format"}
                        status_code = 400
                elif method == RestMethods.GET:
                    response = handler()
                    status_code = 200
                else:
                    response = {"error": f"Method {method} not allowed"}
                    status_code = 405

                response_body = json.dumps(response).encode()

                writer.write(f'HTTP/1.1 {status_code} OK\r\n'.encode() if status_code == 200 else f'HTTP/1.1 {status_code} {self._http_status_message(status_code)}\r\n'.encode())
                writer.write(b'Content-Type: application/json\r\n')
                writer.write(f'Content-Length: {len(response_body)}\r\n\r\n'.encode())
                writer.write(response_body)
            else:
                writer.write(b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n')

            await writer.drain()
        except Exception as e:
            print(f"Error handling request: {e}")
            writer.write(b'HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n')
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    def _http_status_message(self, status_code):
        """
        Returns a default HTTP status message for the given status code.
        """
        messages = {
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        return messages.get(status_code, "Unknown Status")

    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, "0.0.0.0", self.port)
        print(f'Server is listening at port {self.port}')

        self.server_task = asyncio.create_task(self._run_server())

    async def _run_server(self):
        async with self.server:
            while True:
                await asyncio.sleep(1)

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        if self.server_task:
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass