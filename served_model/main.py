import gc
import torch

from flask import Flask, request, jsonify
from flask_cors import CORS

from transformers import BertTokenizer, BertForSequenceClassification

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('huawei-noah/TinyBERT_General_4L_312D')

# Load fine-tuned model (@localhost) './' (@deployment)
model = BertForSequenceClassification.from_pretrained(
    # '/home/senimtra/Desktop/SENIMTRA/ROBO-reviews/served_model', 
    './', output_attentions = True  # Enable attention outputs
)

device = torch.device('cpu')
model.to(device)
model.eval()

# Dropout layers for Monte Carlo sampling
def enable_dropout(model):
    for module in model.modules():
        # Activate all dropout layers
        if module.__class__.__name__.startswith('Dropout'):
            module.train()

@app.route('/predict', methods = ['POST'])
def predict():
    """
    Handle POST requests to perform sentiment regression prediction.
    The input should include a 'review' key with the text to analyze.
    """
    data = request.get_json()
    review_text = data.get('review', '')

    # Tokenize input text and prepare tensors
    inputs = tokenizer(
        review_text, 
        return_tensors = 'pt',
        truncation = True,
        padding = True,
        max_length = 512
    )
    # Move input tensors to device
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():  # Disable gradient computation
        enable_dropout(model)

        # Perform Monte Carlo sampling
        n_samples = 10
        predictions = []
        for _ in range(n_samples):
            outputs = model(**inputs)  # Forward pass
            logits = outputs.logits  # Extract logits (regression output)
            predictions.append(logits.item())  # Add scalar prediction to list

        # Calculate mean prediction (final regression value)
        regression_value = sum(predictions) / n_samples
        
        # Determine sentiment (range not 0-100)
        sentiment = 'Neutral'
        if regression_value < 0.3:
            sentiment = 'Negative'
        elif regression_value > 0.8:
            sentiment = 'Positive'

        # Calculate std of predictions (uncertainty measure)
        std = torch.std(torch.tensor(predictions)).item()

        # Normalize confidence as a percentage (higher is better)
        max_std = 1.0  # Define maximum expected standard deviation
        confidence_percentage = max(0, min(100, 100 * (1 - (std / max_std))))

        # Retrieve attention scores from last layer
        attentions = outputs.attentions
        # Aggregate attention scores: average across heads and tokens
        attention_scores = attentions[-1].mean(dim = 1).squeeze(0).mean(dim = 0)
        # Map token IDs to actual token strings
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        # Pair tokens with their corresponding attention scores
        token_scores = [{'token': token, 'attention': score.item() * 100} for token, score in zip(tokens, attention_scores)]

    gc.collect()

    return jsonify({
        'sentiment': sentiment,
        'confidence': confidence_percentage,
        'token_scores': token_scores
    })

# @deployment (remove)
# if __name__ == '__main__':
#     app.run(host = '127.0.0.1', port = 5000, debug = True)
