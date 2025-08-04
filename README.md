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
git clone <https://github.com/abdurrahimbsrn/YOLOv5-Face-Detection-Docker-Service.git>
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
pip install -r client_requirement.txt
```

### Basic Face Detection

```bash
python client.py --image test.jpg
```

### Save Results

```bash
python client.py --image test.jpg --output result.jpg
```

### Performance Benchmark

```bash
python client.py --image test.jpg --benchmark 50
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
