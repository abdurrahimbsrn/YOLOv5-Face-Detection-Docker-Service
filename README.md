# YOLOv5 Face Detection Docker Service

A Docker-based face detection service using YOLOv5s-face model with ZeroMQ communication protocol.

## 🚀 Features

- **High Performance**: YOLOv5s-face model optimized for face detection
- **Docker Support**: Easy deployment with Docker containers
- **ZeroMQ Communication**: Fast and reliable messaging between client and server
- **Base64 Image Processing**: Simple image encoding/decoding
- **Real-time Detection**: Fast inference with GPU/CPU support
- **Client Examples**: Ready-to-use Python client with visualization

## 📋 Requirements

- Docker
- Python 3.10+
- NVIDIA Docker Runtime (optional, for GPU acceleration)

## 🏗️ Project Structure

```
yolov5-face/
├── Dockerfile              # Docker configuration
├── main.py                 # Face detection server
├── client.py               # Test client
├── requirements.txt        # Python dependencies
├── client_requirements.txt # Client dependencies
├── model/                  # Model files directory
│   └── yolov5s-face.pt    # YOLOv5s face detection model
└── README.md           # This file
```

## 🐳 Docker Setup

### Build Docker Image

```bash
git clone <your-repo-url>
cd yolov5-face
docker build -t ainextus/yolov5s-face .
```

### Run Container

```bash
docker run -p 5550:5555 ainextus/yolov5s-face
```

### With GPU Support

```bash
docker run --gpus all -p 5550:5555 ainextus/yolov5s-face
```

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `/models` | Path to model files |
| `MODEL_FILE` | `yolov5s-face.pt` | Model filename |
| `ZMQ_PORT` | `5555` | ZeroMQ server port |

Example with custom settings:

```bash
docker run -p 5550:5555 \
    -e MODEL_FILE=custom-face-model.pt \
    -e ZMQ_PORT=5555 \
    ainextus/yolov5s-face
```

## 📝 Client Usage

### Install Client Dependencies

```bash
pip install -r client_requirements.txt
```

### Basic Face Detection

```bash
python client.py --image test_image.jpg
```

### Save Results

```bash
python client.py --image test_image.jpg --output result.jpg
```

### Performance Benchmark

```bash
python client.py --image test_image.jpg --benchmark 50
```

### Command Line Options

```bash
python client.py -h
```

```
usage: client.py [-h] --image IMAGE [--host HOST] [--port PORT] 
                 [--output OUTPUT] [--benchmark BENCHMARK] [--no-visualize]

YOLOv5 Face Detection Client

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE, -i IMAGE
                        Input image path
  --host HOST           Server host (default: localhost)
  --port PORT, -p PORT  Server port (default: 5550)
  --output OUTPUT, -o OUTPUT
                        Output image path (optional)
  --benchmark BENCHMARK, -b BENCHMARK
                        Run benchmark with N requests
  --no-visualize        Skip visualization
```

## 🔌 API Reference

### Request Format

```json
{
    "image_base64": "base64_encoded_image_data"
}
```

### Response Format

#### Success Response

```json
{
    "detections": [
        {
            "xmin": 100.5,
            "ymin": 200.3,
            "xmax": 300.7,
            "ymax": 400.9,
            "confidence": 0.95,
            "class": 0,
            "name": "face"
        }
    ]
}
```

#### Error Response

```json
{
    "error": "Error message description"
}
```

## 🛠️ Development

### Custom Model

To use your own face detection model:

1. Place your model file in the `model/` directory
2. Set the `MODEL_FILE` environment variable
3. Rebuild the Docker image

```bash
docker build -t your-custom-face-detector .
docker run -p 5550:5555 -e MODEL_FILE=your-model.pt your-custom-face-detector
```

### Client Integration

```python
import zmq
import json
import base64

# Connect to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5550")

# Prepare request
with open("image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {"image_base64": img_b64}

# Send request
socket.send_string(json.dumps(payload))

# Receive response
response = json.loads(socket.recv_string())
detections = response.get("detections", [])

print(f"Found {len(detections)} faces")
```

## 📊 Performance

Typical performance metrics on different hardware:

| Hardware | Avg. Processing Time | Throughput |
|----------|---------------------|------------|
| CPU (Intel i7) | ~200ms | ~5 FPS |
| GPU (RTX 3080) | ~50ms | ~20 FPS |
| GPU (RTX 4090) | ~30ms | ~33 FPS |

*Performance may vary based on image size and complexity*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) for the base detection framework
- [YOLOv5-face](https://github.com/deepcam-cn/yolov5-face) for the face detection model
- [ZeroMQ](https://zeromq.org/) for high-performance messaging

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Create a new issue with detailed description
3. Provide logs and system information

## 🔄 Changelog

### v1.0.0
- Initial release
- Docker containerization
- ZeroMQ communication
- Python client with visualization
- Performance benchmarking tools
