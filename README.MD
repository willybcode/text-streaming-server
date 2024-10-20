# Streaming Server

This project implements a simple streaming server that streams a message word by word using HTTP `POST` requests. The server splits the provided message into individual words and sends them as JSON-encoded Server-Sent Events (SSE) to the client. The word-streaming speed, repetition, and duration can be customized using command-line arguments.

## Features

- Streams a message word by word over HTTP.
- Supports customizable word-per-second rate, message repetition, and total duration.
- Can read the message from a file or accept it as an argument.
- Simple and lightweight, using Python's built-in `http.server`.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of command-line usage.

### Installation
Clone this repository:
   ```bash
   git clone https://github.com/willybcode/text-streaming-server.git
   cd streaming-server
   ```

### Running the Server

You can start the server with various options to customize the stream:

```bash
python3 server.py [OPTIONS]
```

### Command-Line Options

| Option              | Description                                                                 | Default                           |
|---------------------|-----------------------------------------------------------------------------|-----------------------------------|
| `--text-file`        | Path to a text file to use as the message.                                  | `None`                            |
| `--message`          | Message to stream word by word.                                             | `"This is our test streaming server."` |
| `--words-per-second` | Number of words to stream per second.                                       | `2`                               |
| `--repeat-count`     | Number of times to repeat the message.                                      | `1`                               |
| `--stream-duration`  | Total streaming duration in seconds (overrides repeat count).               | `3600` (1 hour)                   |
| `--port`             | Port to run the server on.                                                  | `8000`                            |

### Example Usages

1. **Run with default settings:**
   ```bash
   python3 server.py
   ```
   This will stream the default message `"This is our test streaming server."` at 2 words per second for 1 hour on port 8000.

2. **Stream a custom message:**
   ```bash
   python3 server.py --message "Hello World! Welcome to the stream." --words-per-second 1 --repeat-count 3
   ```
   This will stream the message at 1 word per second and repeat it 3 times.

3. **Read the message from a file:**
   ```bash
   python3 server.py --text-file path/to/message.txt --words-per-second 2 --stream-duration 120
   ```
   This will read the message from the specified text file and stream it for 120 seconds.

### How It Works

- The server listens for HTTP `POST` requests on `/v1/chat/completions`.
- Once a request is received, it streams the message word by word as JSON objects using Server-Sent Events (SSE).
- The streaming speed, repetition, and duration can be customized via command-line arguments.

### Example Response

Each word is streamed as a JSON object in the following format:

```json
data: {"choices":[{"delta":{"content":"word "}}]}
```

### Customization Options

- **Message Source**: You can pass a message directly via `--message` or use `--text-file` to read from a file.
- **Streaming Rate**: Use `--words-per-second` to control how fast the words are streamed.
- **Repetition**: The `--repeat-count` flag allows you to specify how many times to repeat the message.
- **Duration**: Use `--stream-duration` to specify how long the stream should run (in seconds). It overrides the repetition count.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or improve the code.
