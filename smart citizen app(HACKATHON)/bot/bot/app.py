import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch
# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Streamlit UI
st.title("Sentiment Analysis")

# Input text area
text = st.text_area("Enter text:", "")

# Predict button
if st.button("Predict"):
    if text:
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt")
        
        # Pass the tokenized inputs through the model
        outputs = model(**inputs)
        
        # Get the predicted class probabilities
        probabilities = F.softmax(outputs.logits, dim=-1)
        
        # Get the predicted class
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        
        # Display prediction
        st.write("Predicted Sentiment:")
        if predicted_class == 0:
            st.write("Negative")
        else:
            st.write("Positive")
    else:
        st.write("Please enter some text.")
