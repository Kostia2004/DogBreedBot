import tensorflow as tf
import cv2
import numpy as np

ModelPath = "./models/model.tflite"

def resolve(filename):
    interpreter = tf.lite.Interpreter(model_path=ModelPath)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = tf.keras.preprocessing.image.load_img(filename); #получение изображения
    img_1 = tf.keras.preprocessing.image.img_to_array(img) #конвертация изображения
    img_1 = cv2.resize(img_1, (224, 224),
                       interpolation=cv2.INTER_AREA) #изменение размера
    img_2 = np.expand_dims(img_1, axis=0) / 255. #перевод в матрицу

    interpreter.set_tensor(input_details[0]['index'], img_2)
    interpreter.invoke() #получение значений на нейронах выходного слоя
    output_data = interpreter.get_tensor(output_details[0]['index'])# получение результата
    return output_data[0]
