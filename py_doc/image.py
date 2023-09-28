import cv2
import pytesseract
from py_doc.yolov7.document_detection import detect_document
from py_doc import utils
import os
import fitz

class Image:
    """
    A class for representing an image.

    :param name: The name of the image.
    :type name: str
    """

    def __init__(self, name):
        self.name = name
        self.image = cv2.imread(name)

    def get_name(self):
        """
        Get the name of the image.

        :return: The name of the image.
        :rtype: str
        """

        return self.name

    def get_bboxes(self):
        """
        Use an object detection model to get bounding boxes for titles, text, figures, lists, and tables in the image.

        :return: A list of bounding boxes of the image.
        :rtype: list
        """
        return detect_document(self.image)

    def draw_classifications(self, file):
        """
        Draw the bounding boxes on the image.

        :param file: The output file to save the image to.
        :type file: str

        :return: Boolean indicating if the image was saved.
        :rtype: bool
        """
        
        bboxes = detect_document(self.image)

        classes = ["text", "title", "list", "table", "figure"]
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 255, 255)]

        for bbox in bboxes:
            x1, y1, x2, y2, class_id = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), int(bbox[5])
            color = colors[class_id]
            cv2.rectangle(self.image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(self.image, classes[class_id], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

        cv2.imwrite(file, self.image)

        return True

    def get_text(self):
        """
        Get the text from the image.

        :return: The text from the image.
        :rtype: str
        """

        return pytesseract.image_to_string(self.image, lang='eng')

    def get_text_from_bbox(self, bbox):
        """
        Get the text from the bounding box.

        :param bbox: The bounding box to get the text from.
        :type bbox: list with 4 elements [x1, y1, x2, y2]

        :return: The text from the bounding box.
        :rtype: str
        """

        x1, y1, x2, y2 = utils.reformat_bbox(bbox)
        cropped = self.image[y1:y2, x1:x2]
        return pytesseract.image_to_string(cropped, lang='eng')