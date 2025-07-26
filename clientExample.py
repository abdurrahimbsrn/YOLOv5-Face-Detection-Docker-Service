import zmq
import json
import base64
import cv2
import numpy as np
import argparse
import time
from pathlib import Path

class YOLOv5FaceClient:
    def __init__(self, server_host="localhost", server_port=5550):
        """
        YOLOv5 Face Detection Client
        
        Args:
            server_host: Docker container'ın çalıştığı host
            server_port: Docker container'da expose edilen port
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{server_host}:{server_port}")
        print(f"Connected to YOLOv5 server at {server_host}:{server_port}")
    
    def encode_image(self, image_path):
        """Resmi base64 formatına encode et"""
        try:
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                img_b64 = base64.b64encode(img_data).decode('utf-8')
                return img_b64
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None
    
    def detect_faces(self, image_path):
        """Face detection işlemini gerçekleştir"""
        print(f"📷 Processing image: {image_path}")
        
        # Resmi encode et
        img_b64 = self.encode_image(image_path)
        if not img_b64:
            return None
        
        # Request payload hazırla
        payload = {
            "image_base64": img_b64
        }
        
        try:
            # Request gönder
            start_time = time.time()
            self.socket.send_string(json.dumps(payload))
            
            # Response al
            response = self.socket.recv_string()
            end_time = time.time()
            
            result = json.loads(response)
            
            if "error" in result:
                print(f"Server error: {result['error']}")
                return None
            
            detections = result.get("detections", [])
            processing_time = end_time - start_time
            
            print(f"Detection completed in {processing_time:.2f}s")
            print(f"Found {len(detections)} faces")
            
            return detections, processing_time
            
        except Exception as e:
            print(f"Client error: {e}")
            return None
    
    def visualize_results(self, image_path, detections, output_path=None):
        """Sonuçları görselleştir"""
        if not detections:
            return
        
        # Resmi yükle
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not load image: {image_path}")
            return
        
        # Her face için bounding box çiz
        for i, detection in enumerate(detections):
            x1 = int(detection['xmin'])
            y1 = int(detection['ymin'])
            x2 = int(detection['xmax'])
            y2 = int(detection['ymax'])
            confidence = detection['confidence']
            
            # Bounding box çiz
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Confidence score yaz
            label = f"Face {i+1}: {confidence:.2f}"
            cv2.putText(img, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Sonucu kaydet veya göster
        if output_path:
            cv2.imwrite(output_path, img)
            print(f"Result saved to: {output_path}")
        else:
            cv2.imshow("YOLOv5 Face Detection", img)
            print("Press any key to close the window...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def benchmark_test(self, image_path, num_requests=10):
        """Performance testi"""
        print(f"🚀 Running benchmark with {num_requests} requests...")
        
        times = []
        success_count = 0
        
        for i in range(num_requests):
            print(f"Request {i+1}/{num_requests}", end=" - ")
            result = self.detect_faces(image_path)
            
            if result:
                detections, processing_time = result
                times.append(processing_time)
                success_count += 1
            
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n Benchmark Results:")
            print(f"   Success Rate: {success_count}/{num_requests} ({success_count/num_requests*100:.1f}%)")
            print(f"   Average Time: {avg_time:.3f}s")
            print(f"   Min Time: {min_time:.3f}s")
            print(f"   Max Time: {max_time:.3f}s")
            print(f"   Throughput: {1/avg_time:.1f} requests/second")
    
    def close(self):
        """Connection'ı kapat"""
        self.socket.close()
        self.context.term()

def main():
    parser = argparse.ArgumentParser(description="YOLOv5 Face Detection Client")
    parser.add_argument("--image", "-i", required=True, help="Input image path")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", "-p", type=int, default=5550, help="Server port (default: 5550)")
    parser.add_argument("--output", "-o", help="Output image path (optional)")
    parser.add_argument("--benchmark", "-b", type=int, help="Run benchmark with N requests")
    parser.add_argument("--no-visualize", action="store_true", help="Skip visualization")
    
    args = parser.parse_args()
    
    # Image path kontrolü
    if not Path(args.image).exists():
        print(f"Image file not found: {args.image}")
        return
    
    # Client oluştur
    client = YOLOv5FaceClient(args.host, args.port)
    
    try:
        if args.benchmark:
            # Benchmark testi
            client.benchmark_test(args.image, args.benchmark)
        else:
            # Tek detection
            result = client.detect_faces(args.image)
            
            if result:
                detections, processing_time = result
                
                # Detections bilgilerini yazdır
                print(f"\nDetection Details:")
                for i, detection in enumerate(detections):
                    print(f"   Face {i+1}:")
                    print(f"     Coordinates: ({detection['xmin']:.1f}, {detection['ymin']:.1f}) - ({detection['xmax']:.1f}, {detection['ymax']:.1f})")
                    print(f"     Confidence: {detection['confidence']:.3f}")
                    print(f"     Class: {detection['name']}")
                
                # Görselleştir
                if not args.no_visualize:
                    client.visualize_results(args.image, detections, args.output)
    
    finally:
        client.close()
        print("Client closed.")

if __name__ == "__main__":
    main()