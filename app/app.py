import streamlit as st
import tensorflow as tf
import numpy as np
import joblib
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the model and tokenizer
@st.cache_resource
def load_model():
    model_path = os.path.join(os.getcwd(), "next_word_prediction_model.keras")
    return tf.keras.models.load_model(model_path)

@st.cache_resource
def load_tokenizer():
    tokenizer_path = os.path.join(os.getcwd(), "tokenizer.joblib")
    return joblib.load(tokenizer_path)

model = load_model()
tokenizer = load_tokenizer()

def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = []
    in_text = seed_text
    for _ in range(n_words):
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        predict_x = model.predict(encoded, verbose=0)
        yhat = np.argmax(predict_x, axis=1)
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)

st.title("Next Word Prediction App")

# Input text box for user to enter 50 words
user_input = st.text_area("Enter at least 50 words:", height=200)

if st.button("Predict Next 6 Words"):
    if user_input:
        words = user_input.split()
        if len(words) >= 50:
            seed_text = " ".join(words[:50])
            next_words = generate_seq(model, tokenizer, 50, seed_text, 6)
            
            st.subheader("Prediction:")
            st.write(f"Next 6 words:")
            st.success(f"{next_words}")
            
            full_text = seed_text + " " + next_words
            st.subheader("Full text with prediction:")
            st.write(full_text)
            
        else:
            st.error("Please enter at least 50 words.")
    else:
        st.error("Please enter some text.")