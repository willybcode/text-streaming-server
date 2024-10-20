import json
import time
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Custom handler to manage streaming responses
class StreamHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, message="This is our test streaming server.", words_per_second=2, repeat_count=1, stream_duration=3600, **kwargs):
        self.message = message
        self.words_per_second = words_per_second
        self.repeat_count = repeat_count
        self.stream_duration = stream_duration
        super().__init__(*args, **kwargs)

    # Handle POST requests to stream word-by-word content
    def do_POST(self):
        if self.path == '/v1/chat/completions':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()

            words = self.message.split()  # Split message into individual words
            interval = 1 / self.words_per_second  # Calculate interval between words

            start_time = time.time()  # Track when streaming starts
            total_duration = self.stream_duration if self.stream_duration else (self.repeat_count * len(words) * interval)

            # Stream each word at specified interval
            while True:
                for word in words:
                    # Stop if duration is exceeded
                    if self.stream_duration and (time.time() - start_time >= self.stream_duration):
                        return
                    response_message = json.dumps({"choices": [{"delta": {"content": f"{word} "}}]})
                    self.wfile.write(f"data: {response_message}\n\n".encode('utf-8'))
                    self.wfile.flush()
                    time.sleep(interval)

                # Handle message repetition logic
                if self.repeat_count > 0:
                    self.repeat_count -= 1
                    if self.repeat_count == 0 and not self.stream_duration:
                        break  # Stop if repeat count is exhausted and no duration set
        else:
            self.send_error(404)  # Send 404 for invalid endpoints

# Function to run the streaming server
def run(server_class=HTTPServer, handler_class=StreamHandler, port=8000, message="This is our test streaming server.", words_per_second=2, repeat_count=1, stream_duration=3600):
    server_address = ('', port)
    # Pass the handler class with customized arguments
    handler = lambda *args, **kwargs: handler_class(*args, message=message, words_per_second=words_per_second, repeat_count=repeat_count, stream_duration=stream_duration, **kwargs)
    httpd = server_class(server_address, handler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    default_message = "This is our test streaming server."
    parser = argparse.ArgumentParser(description='Run a streaming server.')
    
    # Command-line arguments for message customization
    parser.add_argument('--text-file', type=str, help='Path to a text file to use as the message')
    parser.add_argument('--message', type=str, help='Message to stream word by word')
    parser.add_argument('--words-per-second', type=int, help='Words per second (default: 2)')
    parser.add_argument('--repeat-count', type=int, help='Number of times to repeat the message (default: 1)')
    parser.add_argument('--stream-duration', type=int, help='Total duration of the output in seconds')
    parser.add_argument('--port', type=int, default=8000, help='Port number for the server (default: 8000)')

    args = parser.parse_args()

    # Read message from text file if provided
    if args.text_file:
        try:
            with open(args.text_file, 'r') as f:
                message_to_stream = f.read().strip()  # Read and trim file content
        except Exception as e:
            print(f"Error reading file: {e}")
            message_to_stream = args.message or default_message  # Fallback to default message
    else:
        message_to_stream = args.message or default_message

    words_per_second = args.words_per_second or 2  # Default to 2 words per second
    repeat_count = args.repeat_count or 1  # Default to repeating the message once
    stream_duration = args.stream_duration  # Optional duration limit

    # If no specific args provided, default to a 1-hour stream
    if message_to_stream == default_message and not stream_duration and repeat_count == 1 and words_per_second == 2:
        stream_duration = 3600

    # Run the server with parsed arguments
    run(message=message_to_stream, words_per_second=words_per_second, repeat_count=repeat_count, stream_duration=stream_duration, port=args.port)
