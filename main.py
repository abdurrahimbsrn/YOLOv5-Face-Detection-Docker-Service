import os
import zmq
import torch
import logging
import json
import cv2
import base64
import numpy as np

# ----------------------------
# Configs
# ----------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "/models")
MODEL_FILE = os.getenv("MODEL_FILE", "yolov5s-face.pt")
PORT = int(os.getenv("ZMQ_PORT", 5555))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("YOLOv5FaceServer")

# ----------------------------
# Load Model
# ----------------------------
def load_model():
    model_full_path = os.path.join(MODEL_PATH, MODEL_FILE)
    try:
        logger.info(f"Loading YOLOv5 model from {model_full_path} ...")
        
        # Trust repo parametresi eklendi
        model = torch.hub.load("ultralytics/yolov5", "custom", 
                              path=model_full_path, 
                              force_reload=False,
                              trust_repo=True)
        
        model.to(DEVICE).eval()
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise e

model = load_model()

# ----------------------------
# ZeroMQ
# ----------------------------
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{PORT}")
logger.info(f"🔌 ZeroMQ listening on port {PORT}...")

# ----------------------------
# Inference Loop
# ----------------------------
while True:
    try:
        raw_message = socket.recv_string()
        payload = json.loads(raw_message)

        image_b64 = payload.get("image_base64")
        if not image_b64:
            raise ValueError("Missing 'image_base64' in payload")

        img_data = base64.b64decode(image_b64)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = model(img, size=640)
        detections = results.pandas().xyxy[0].to_dict(orient="records")

        logger.info(f"[DETECTIONS] {len(detections)} faces detected")

        socket.send_string(json.dumps({
            "detections": detections
        }))

    except Exception as e:
        logger.error(f"[ERROR] {str(e)}")
        socket.send_string(json.dumps({
            "error": str(e)}
        ))
