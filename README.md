
# RoboReviews

## Overview

This repository contains the source code, documentation, and deliverables for the **Video Game Review Aggregator** project. The goal of this project is to build an NLP-powered website that processes and analyzes video game reviews. The system performs sentiment classification, clusters reviews into categories, and generates summaries to recommend top products.

## Features

1. **Sentiment Analysis**:
   - Classifies reviews as **Positive**, **Neutral**, or **Negative**.
   - Fine-tuned model ensures high accuracy tailored to the dataset.

2. **Category Clustering**:
   - Groups reviews into broader product categories, e.g., **Action Games**, **RPGs**, etc.
   - Enables better data organization and visualization.

3. **Review Summarization**:
   - Generates blog-like articles summarizing key points of each category.
   - Highlights:
     - Top 3 products and their unique features.
     - Top complaints and feedback.
     - Worst product in the category with reasons.

4. **Interactive Website**:
   - Presents all analyses in an intuitive, user-friendly interface.
   - Allows users to upload reviews for live processing.

## Datasets

- **Primary Dataset**: Custom video game review dataset.
  - [UCSD Amazon Reviews](https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews)

## Project Structure

```
root/
├── data/               # Raw and processed datasets
├── models/             # Saved and fine-tuned models
├── notebooks/          # Jupyter notebooks for model development
├── app/                # Code for the website and deployment
│   ├── static/         # Static files (CSS, JS, images)
│   └── templates/      # HTML templates
├── results/            # Evaluation metrics, visualizations, and summaries
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## How It Works

1. **Preprocessing**:
   - Text cleaning: Removing unnecessary characters, standardizing text.
   - Tokenization and vectorization: Using pretrained models.

2. **Model Pipeline**:
   - **Classifier**: Fine-tuned DistilBERT for sentiment classification.
   - **Clusterer**: Custom clustering algorithm using product metadata and review content.
   - **Summarizer**: Generative model (e.g., Llama or Mistral) for creating human-like summaries.

3. **Evaluation**:
   - Metrics: Accuracy, Precision, Recall, F1-Score.
   - Extensive testing and failure case analysis for model improvements.

4. **Deployment**:
   - Hosted website built with Django.
   - Hosted (Frontend/Backend) on (Netlify/Heroku).

## Deliverables

1. **Source Code**:
   - Organized Python scripts and Jupyter notebooks.
   - Code adheres to linting standards (e.g., `pylint`).

2. **Website**:
   - Live demo hosted (TBA URL).

3. **Presentation**:
   - Summarizes project goals, challenges, results, and outcomes.

4. **Evaluation Metrics**:
   - Comprehensive table of model performance.

## Usage

- **Upload Reviews**: Users can upload review files (e.g., CSV) via the website.
- **Analyze Reviews**: View categorized, summarized, and sentiment-analyzed results on the platform.

## Future Enhancements

- Extend datasets for broader coverage.
- Add multilingual review support.
- Integrate a dashboard for real-time insights.

## Acknowledgments

- Datasets from UCSD.
- Pretrained models from Hugging Face.
