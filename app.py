from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, request, jsonify
import numpy as np
import pickle
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

# Load the tokenizer and models
def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as file:
        tokenizer = pickle.load(file)
    return tokenizer

maxlen_questions = 13
tokenizer_path = 'tokenizer.pickle'
model_path = 'chatbot_model.h5'
decoder_model_path = 'decoder_model.h5'
encoder_model_path = 'encoder_model.h5'

tokenizer = load_tokenizer(tokenizer_path)
model = load_model(model_path)
decoder_model = load_model(decoder_model_path)
encoder_model = load_model(encoder_model_path)

def decode_sequence(input_seq):
    enc_out, enc_h, enc_c = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = tokenizer.word_index['end']
    
    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + [enc_out, enc_h, enc_c])

        sampled_token_index = np.argmax(output_tokens[0, -1, :])

        if sampled_token_index in reverse_word_index:
            sampled_char = reverse_word_index.get(sampled_token_index, '')

            if sampled_char == 'start':
                stop_condition = True
            else:
                decoded_sentence += ' {}'.format(sampled_char)

            target_seq = np.zeros((1, 1))
            target_seq[0, 0] = sampled_token_index
            enc_h, enc_c = h, c
        else:
            break

    return decoded_sentence.strip()

def string_to_integer(user_input, tokenizer, max_len):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded = pad_sequences(sequence, maxlen=max_len, padding='post')
    return padded

def load_tokenizer(tokenizer_path):
    with open('tokenizer.pickle', 'rb') as file:
        tokenizer = pickle.load(file)
    return tokenizer
    
tokenizer = load_tokenizer('tokenizer.pickle')
reverse_word_index = {i: word for word, i in tokenizer.word_index.items()}

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json['question']
    input_sequence = string_to_integer(user_input, tokenizer, maxlen_questions)
    output_result = decode_sequence(input_sequence)
    return jsonify({'response': output_result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
