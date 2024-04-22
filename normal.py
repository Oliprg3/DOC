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

        if predicted_class == 0:
            st.wrtie("This X-ray image shows characteristic features consistent with tuberculosis (TB) infection:\n"
            "- Areas of increased opacity and consolidation are observed, indicating inflammation and fluid accumulation in the lung tissue.\n"
            "- Cavitations, represented by dark areas surrounded by dense tissue, are visible, suggesting advanced TB disease.\n"
            "- The distribution of abnormalities appears bilateral and asymmetrical, typical of TB infection.\n"
            "- Associated findings such as pleural effusions and mediastinal lymphadenopathy may also be present.\n\n"
            "Based on these findings and considering the patient's clinical history and symptoms, it is likely that the patient is infected with tuberculosis."

            "ይህ የኤክስሬይ ምስል ከሳንባ ነቀርሳ (ቲቢ) ኢንፌክሽን ጋር የሚጣጣሙ ባህሪያትን ያሳያል
            "- በሳንባ ቲሹ ውስጥ እብጠት እና ፈሳሽ መከማቸትን የሚያመለክቱ ግልጽነት እና ማጠናከሪያ ቦታዎች ይታያሉ.
            "- ጥቅጥቅ ባለ ቲሹ በተከበቡ ጨለማ ቦታዎች የተወከሉት ካቪቴቶች የሚታዩ ሲሆን ይህም የተራቀቀ የቲቢ በሽታ ይጠቁማል.
            "- የተዛባዎች ስርጭት በሁለትዮሽ እና ያልተመጣጠነ ይመስላል, የቲቢ ኢንፌክሽን የተለመደ ነው.
            "- እንደ pleural effusions እና mediastinal lymphadenopathy የመሳሰሉ ተያያዥ ግኝቶችም ሊኖሩ ይችላሉ።
            "በእነዚህ ግኝቶች ላይ በመመርኮዝ እና የታካሚውን ክሊኒካዊ ታሪክ እና ምልክቶች ከግምት ውስጥ በማስገባት በሽተኛው በሳንባ ነቀርሳ ሊጠቃ ይችላል."
        )
        else:
            st.write( "This X-ray image does not show significant abnormalities indicative of tuberculosis (TB) infection.\n"
            "There are no areas of increased opacity, consolidation, or cavitations observed in the lung tissue.\n\n"
            "Considering the absence of characteristic TB findings and in conjunction with the patient's clinical history and symptoms, it is unlikely that the patient is infected with tuberculosis."
        )   "ይህ የኤክስሬይ ምስል የሳንባ ነቀርሳ (ቲቢ) ኢንፌክሽንን የሚያመለክቱ ጉልህ የሆኑ ያልተለመዱ ነገሮችን አያሳይም።\n"
            "በሳንባ ቲሹ ውስጥ የጨመሩ ግልጽነት፣ ማጠናከሪያ ወይም ክፍተቶች የታዩባቸው ቦታዎች የሉም።\n\n"
            "ባህሪያዊ የቲቢ ግኝቶች አለመኖራቸውን እና ከታካሚው ክሊኒካዊ ታሪክ እና ምልክቶች ጋር በመተባበር በሽተኛው በሳንባ ነቀርሳ መያዙ አይቀርም."
if __name__ == "__main__":
    main()
