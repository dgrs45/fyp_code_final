from flask import Flask, request
from flask_cors import CORS
import numpy as np
import torch


model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 
app = Flask(__name__)
CORS(app)

@app.route('/camera', methods=["POST","GET"])
def get_frame():
    try:
        frm = request.data
        frame = np.array(frm)
        results = model(frame)
        classes_detected = []
        for bbox in results.xyxy[0]:
            xmin, ymin, xmax, ymax, confidence, class_id = bbox.tolist()
            class_name = model.names[int(class_id)]
            classes_detected.append(class_name)
            print(class_name)
        if len(classes_detected) != 0:
                return {"main_class_detected": str(classes_detected[0])}
        else:
            return {"main_class_detected": "No classes detected"}
    except KeyboardInterrupt:
        pass
    return "hi"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
