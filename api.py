from flask import Flask, request
from flask_cors import CORS
import numpy as np




app = Flask(__name__)
CORS(app)

@app.route('/camera', methods=["POST","GET"])
def get_frame():
    try:
        cap = acapture.open(0) # /dev/video0
        while True:
            check,frame = cap.read() # non-blocking
            print(check)
            if check:
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                cv2.imshow("test",frame)
                results = model(frame)
                print('\n\nresult', type(results))
                classes_detected = []
                for bbox in results.xyxy[0]:
                    xmin, ymin, xmax, ymax, confidence, class_id = bbox.tolist()
                    class_name = model.names[int(class_id)]
                    classes_detected.append(class_name)
                    print(class_name)
                cv2.waitKey(1)
                if len(classes_detected) != 0:
                        return {"main_class_detected": str(classes_detected[0])}
                else:
                    return {"main_class_detected": "No classes detected"}
    except KeyboardInterrupt:
        pass
    return "hi"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
