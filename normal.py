import streamlit as st
import onnxruntime
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import time

def load_onnx_model(model_path):
    session = onnxruntime.InferenceSession(model_path)
    return session

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485], std=[0.229])
    ])
    image = transform(image)
    return image

def classify_image_onnx(image, session):
    processed_image = preprocess_image(image)
    
    processed_image = processed_image.unsqueeze(0)

    input_data = processed_image.numpy()

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_data})[0]

    predicted_class = "Normal" if result[0][0] > result[0][1] else "Tuberculosis"
    return predicted_class

def main():
    st.title('Upload Lung X-ray image')

    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    time.sleep(2)
    if uploaded_file is not None:
        onnx_model_path = "resnet.onnx"
        session = load_onnx_model(onnx_model_path)

        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        predicted_class = classify_image_onnx(image, session)

        st.write(f"This X-ray image shows : {predicted_class} radiographic image")
        
if __name__ == "__main__":
    main()
