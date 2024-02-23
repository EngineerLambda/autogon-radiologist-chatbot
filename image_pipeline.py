import requests
import streamlit as st

st.set_page_config(page_title="Hemorrhage Detection Demo", page_icon="🧠")



endpoint_url = "https://api.autogon.ai/api/v1/label/model/predict/"
api_key = st.secrets["api-key"]

st.title("Hemorrhage Detection Demo 🧠")

def get_img_prediction(image_url :str) -> str:
    # local variables
    app_id = "041f6943-4c29-4f36-b5d1-bc851fc70f16"
    img_url = [image_url]
    model_name = "herm_model_2"
    confidence_thresh = 0.3
    overlap_tresh = 0.5
    
    # body
    body = {
        "app_id" : app_id,
        "image_urls" : img_url,
        "model_name" : model_name,
        "confidence_tresh" : confidence_thresh,
        "overlap_tresh" : overlap_tresh
    }
    
    # auth params
    header = {"X-Aug-Key": api_key}
    
    # request part
    try:
        # request to get the model's prediction for the image
        model_response = requests.post(
            url=endpoint_url, json=body, headers=header
        ).json()
        
        if model_response["status"]:
            # Extract all the labels only either "yes" or "no"
            labels = [(label["lbl"], label["conf"]) for labels in model_response["annotations"].values() for label in labels]
            
            # filter the result, if there is any yes with confidence level greater than
            # or equal to set threshold,
            filtered = list(filter(lambda x: x[0] == "yes" and x[1] >= confidence_thresh, labels))
            
            if bool(filtered):
                st.error("Hemorrhage Detected")
                
            else:
                st.success("Hemorrhage Not Detected")
        
            
    
    # handling exceptions if any 
    except Exception as e:
        st.error(f"Error encountered: {e}")

pred_link = st.text_input("Enter the Autogon AI supported Image url")


if st.button("DETECT"):
    with st.spinner("Detecting ..."):
        get_img_prediction(pred_link)
