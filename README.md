# 🤖 **RoboReviews**

## Overview

This repository contains the source code, documentation, and deliverables for a **Video Game & Reviews ML/AI** project. The goal is to process and analyze video game data and reviews. It performs sentiment classification, clusters game genres, and generates summaries to recommend top games.

## 🎮 **Features**

1. **🔍 Sentiment Analysis**:
   - Classifies reviews as **Positive**, **Neutral**, or **Negative**.
   - Fine-tuned DistilBERT ensures high accuracy tailored to the dataset.

2. **🗂️ Category Clustering**:
   - Groups games into broader genre categories, such as **Combat-Focused Gameplay**, etc..
   - Enables better data organization and visualization.

3. **📝 Review Summarization**:
   - Generates blog-like articles summarizing game features.
   - Highlights the top three games per cluster and reasons why people like/dislike them.

4. **🌐 Interactive Website**:
   - Presents all analyses in an intuitive, user-friendly interface.
   - Allows live sentiment processing of user review texts.

## 📊 **Datasets**

- **Primary Dataset**: Custom video game review dataset.
  - [UCSD Amazon Reviews](https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews)

## 🏗️ **Project Structure**

```
root/
├── core/               # Core Django app
│   └── templates/      # HTML index view
├── data/               # Raw and processed datasets
├── models/             # Saved and fine-tuned models
│   ├── clustering/     # pyLDAvis visualization
│   └── sentiment/      # DistilBERT files
├── notebooks/          # Jupyter notebooks for model development
├── scripts/            # Python scripts for feeding the database
├── served_model/       # Flask app serving TinyBERT
├── static/             # Static files (CSS, JS, images)
├── db.sqlite3          # Django SQLite database
├── manage.py           # Django CLI utility script
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## ⚙️ **How It Works**

1. **🧹 Preprocessing**:
   - **Text Cleaning**: Removes special characters and standardizes text.  
   - **Data Cleaning**: Drops unnecessary columns and handles missing values.  
   - **Enrichment**: Adds genres via the OpenAI API.  
   - **Balancing**: Applies upsampling and downsampling.  
   - **Normalization**: Performs lemmatization and stopword removal.  
   - **Tokenization & Vectorization**: Prepares text for modeling.  

2. **📈 Model Pipeline**:
   - **Sentiment Classification**: Uses fine-tuned DistilBERT for sentiment analysis.  
   - **Topic Modeling**: Employs LDA to uncover hidden topics and group similar game genres.  
   - **Summarization**: Utilizes the OpenAI API for concise summaries of game pros and cons.  

3. **📊 Evaluation**:
   - **Metrics**: Evaluates model performance using accuracy, precision, recall, and F1-score.  
   - **Visualization**: Includes confusion matrix, word clouds, and t-SNE plot.  
   - **Analysis**: Displays example predictions and enables interactive topic exploration with pyLDAvis.  

4. **🚀 Deployment**:
   - **Web Interface**: Built with Django.  
   - **Model Serving**: Sentiment model served via Flask.  
   - **Hosting**: Entire application hosted on Heroku.  

## 📦 **Deliverables**

1. **📜 Source Code**:
   - Organized Python scripts and Jupyter notebooks.

2. **🌐 Website**:
   - Live demo hosted ([RoboReviews](https://robo-reviews-c8f7c8e0c66c.herokuapp.com/)).

3. **📊 Evaluation Metrics**:
   - Visualizations: Plots (images/notebooks) and LDA visualization rendered as HTML.

## 💡 **Usage**

- **💬 Sentiment Predictions**: Users can test written texts for sentiment.
- **📊 Review Analysis**: View categorized and summarized results.

## 🚧 **Future Enhancements**

- Extend datasets for broader coverage.
- Fine-tune and host LLM for game summarization.

## 🙌 **Acknowledgments**

- 📚 Datasets from UCSD.
- 🛠️ Pretrained models from Hugging Face.
