import fitness_core as fc
from fitness_core import cv2, Image, common, make_interpreter

class Inference:
    @staticmethod
    def preprocess_image(frame, target_size=(256, 256)):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_image = cv2.resize(image_rgb, target_size)
        return resized_image

    @staticmethod
    def doInferenceTPU(frame, interpreter):
        image_rgb = Inference.preprocess_image(frame)
        resized_img = Image.fromarray(image_rgb)
        common.set_input(interpreter, resized_img)
        interpreter.invoke()
        return common.output_tensor(interpreter, 0).copy().reshape(fc._NUM_KEYPOINTS, 3)

    @staticmethod
    def doInferenceCPU(frame, interpreter):
        image_rgb = Inference.preprocess_image(frame)
        input_image = tf.expand_dims(image_rgb, axis=0)
        input_image = tf.cast(input_image, dtype=tf.uint8)
        interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_image.numpy())
        interpreter.invoke()
        return interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0].reshape(_NUM_KEYPOINTS, 3)
