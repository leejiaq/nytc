import cv2
import numpy as np
import onnxruntime as ort
import os

class onnxdetector:

    def __init__(self, model, label, confidence_thres=0.5, iou_thres=0.2):
        """
        Initializes an instance of the Yolov8 class.

        Args:
            onnx_model: Path to the ONNX model.
            input_image: Path to the input image.
            confidence_thres: Confidence threshold for filtering detections.
            iou_thres: IoU (Intersection over Union) threshold for non-maximum suppression.

        """
        self.loaded = False
        if os.path.isfile(model) and os.path.isfile(label):
            with open(label, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
                f.close()
                print(F"Labels are: {self.classes}")
            self.onnx_model = model
            # Create an inference session using the ONNX model and specify execution providers
            self.session = ort.InferenceSession(self.onnx_model, providers=['CPUExecutionProvider'])
            self.confidence_thres = confidence_thres
            self.iou_thres = iou_thres
            self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))
            # Get the model inputs
            self.model_inputs = self.session.get_inputs()
        # Store the shape of the input for later use
            self.input_shape = self.model_inputs[0].shape
            self.input_width = self.input_shape[2]
            self.input_height = self.input_shape[3]
            self.input_image = None
            print(F"Model loaded \n Loaded model name - input width/height: {self.input_width}/{self.input_height}")
            self.loaded = True
        else:
            print("model file or label file does not exist.")

        # Generate a color palette for the classes

    def draw_detections(self, img, box, score, class_id):
        """
        Draws bounding boxes and labels on the input image based on the detected objects.

        Args:
            img: The input image to draw detections on.
            box: Detected bounding box.
            score: Corresponding detection score.
            class_id: Class ID for the detected object.

        Returns:
            None
        """

        # Extract the coordinates of the bounding box
        x1, y1, w, h = box

        # Retrieve the color for the class ID
        color = self.color_palette[class_id]

        # Draw the bounding box on the image
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)

        # Create the label text with class name and score
        label = f'{self.classes[class_id]}: {score:.2f}'

        # Calculate the dimensions of the label text
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        # Calculate the position of the label text
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10

        # Draw a filled rectangle as the background for the label text
        cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color,
                      cv2.FILLED)

        # Draw the label text on the image
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self):
        """
        Preprocesses the input image before performing inference.

        Returns:
            image_data: Preprocessed image data ready for inference.
        """
        # Get the height and width of the input image
        [self.img_height, self.img_width,_] = self.img.shape

        # Convert the image color space from BGR to RGB
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        # Resize the image to match the input shape
        img = cv2.resize(img, (self.input_width, self.input_height))

        # Normalize the image data by dividing it by 255.0
        image_data = np.array(img) / 255.0

        # Transpose the image to have the channel dimension as the first dimension
        image_data = np.transpose(image_data, (2, 0, 1))  # Channel first

        # Expand the dimensions of the image data to match the expected input shape
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)

        # Return the preprocessed image data
        return image_data

    def postprocess(self, input_image, output):
        """
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.

        Args:
            input_image (numpy.ndarray): The input image.
            output (numpy.ndarray): The output of the model.

        Returns:
            numpy.ndarray: The input image with detections drawn on it.
        """

        # Transpose and squeeze the output to match the expected shape
        outputs = np.transpose(np.squeeze(output[0]))

        # Get the number of rows in the outputs array
        rows = outputs.shape[0]

        # Lists to store the bounding boxes, scores, and class IDs of the detections
        boxes = []
        scores = []
        class_ids = []

        # Calculate the scaling factors for the bounding box coordinates
        x_factor = self.img_width / self.input_width
        y_factor = self.img_height / self.input_height

        # Iterate over each row in the outputs array
        for i in range(rows):
            # Extract the class scores from the current row
            classes_scores = outputs[i][4:]

            # Find the maximum score among the class scores
            max_score = np.amax(classes_scores)

            # If the maximum score is above the confidence threshold
            if max_score >= self.confidence_thres:
                # Get the class ID with the highest score
                class_id = np.argmax(classes_scores)

                # Extract the bounding box coordinates from the current row
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

                # Calculate the scaled coordinates of the bounding box
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                # Add the class ID, score, and box coordinates to the respective lists
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        # Apply non-maximum suppression to filter out overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)

        # Iterate over the selected indices after non-maximum suppression
        for i in indices:
            # Get the box, score, and class ID corresponding to the index
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            x1, y1, w, h = box
            cx = (x1+ w) // 2
            cy = (y1 + h) // 2
            label = self.classes[class_id]
            current_detected_object = {'label':label,'score':score,'x':cx,'y':cy}
            self.detected_obj.append(current_detected_object)
            if score > self.highest_score:
                self.highest_score = score
                self.highest_detected_x = cx
                self.highest_detected_y = cy
                self.highest_score_obj = current_detected_object
            # Draw the detection on the input image
            self.draw_detections(input_image, box, score, class_id)

        # Return the modified input image
        return self.highest_score_obj, input_image

    def get_detected_obj(self):
        return self.detected_obj

    def detect(self,frame,confidence_level=0.5):
        """
        Performs inference using an ONNX model and returns the output image with drawn detections.

        Returns:
            output_img: The output image with drawn detections.
        """
        self.confidence_thres=confidence_level
        self.img = frame
        self.detected_obj = []
        self.highest_detected_label = ""
        self.highest_detected_x = 0
        self.highest_detected_y = 0
        self.highest_score = -1
        self.highest_score_obj = None
        # Preprocess the image data
        img_data = self.preprocess()

        # Run inference using the preprocessed image data
        outputs = self.session.run(None, {self.model_inputs[0].name: img_data})

        # Perform post-processing on the outputs to obtain output image.
        return self.postprocess(self.img, outputs)  # output image


if __name__ == '__main__':

    # Create an instance of the Yolov8 class with the specified arguments
    detection = onnxdetector("best-v8.onnx", confidence_thres=0.5, iou_thres=0.2)

    # Perform object detection and obtain the output image
    output_image = detection.detect()

    # Display the output image in a window
    cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
    cv2.imshow('Output', output_image)

    # Wait for a key press to exit
    cv2.waitKey(0)