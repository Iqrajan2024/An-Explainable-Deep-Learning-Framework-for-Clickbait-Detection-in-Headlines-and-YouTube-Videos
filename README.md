# An Explainable Deep Learning Framework for Clickbait Detection in Headlines and YouTube Videos

## Overview

This repository contains the implementation of our Final Year Project (FYP), **"An Explainable Deep Learning Framework for Clickbait Detection in Headlines and YouTube Videos."**

The project proposes **ClickDetect AI**, an AI-powered browser extension that detects clickbait in online news headlines and YouTube videos in real time. The system combines deep learning models with Explainable Artificial Intelligence (XAI) techniques to not only classify content as clickbait or non-clickbait, but also explain the factors that influenced each prediction.

The system consists of:

- A Chrome browser extension
- A FastAPI backend server
- Deep learning models for headline and multimodal clickbait detection
- SHAP-based explainability modules
- GRAD-CAM based visualizations
- Interactive user interface for prediction results

---

# Repository Structure

```
.
├── Data Preprocessing.ipynb
├── Exploratory Data Analysis.ipynb
├── Models.ipynb
├── XAI.ipynb
├── clickbait-detector-extension/
├── screenshots/
├── Datasets/
├── Video Data Collection Scripts/
├── requirements.txt
└── README.md
```

---
## Datasets

This project uses two datasets:

### Headline Dataset
- Contains clickbait and non-clickbait news headlines.
- Used to train the BiLSTM headline classification model.

### YouTube Dataset
- A novel annotated custom multimodal dataset collected using the YouTube Data API.
- Contains:
  - Video title
  - Video description
  - Thumbnail
  - Video metadata
  - Channel information
- Labels were generated using a rule-based labeling strategy based on the video title and were subsequently used to train the multimodal deep learning model.

> **Note:** The datasets are not fully included in this repository due to their size. Only sample datasets are included. Users wishing to reproduce the experiments should prepare equivalent datasets and place them in the appropriate directories.

# Jupyter Notebooks

## 1. Data Preprocessing.ipynb

Performs all data preparation tasks required before model training.

Includes:

- Dataset loading
- Data cleaning
- Missing value handling
- Text preprocessing
- Feature engineering
- Metadata preprocessing
- Image path preparation
- Dataset splitting
- Tokenization
- Sequence padding
- Feature scaling

Outputs the processed datasets used for model training.

---

## 2. Exploratory Data Analysis.ipynb

Performs exploratory analysis of both headline and YouTube datasets.

Includes:

- Dataset statistics
- Class distribution
- Feature distributions
- Correlation analysis
- Missing value analysis
- Visualization of important dataset characteristics

---

## 3. Models.ipynb

Implements and trains all deep learning models used in the project.

Includes:

### Headline Model

- BiLSTM architecture
- Training
- Validation
- Evaluation

### Multimodal Model

Combines:

- Text (BiLSTM)
- Thumbnail images (CNN)
- Video metadata (Dense Network)

Includes:

- Model construction
- Training pipeline
- Performance evaluation
- Model saving

---

## 4. XAI.ipynb

Implements Explainable Artificial Intelligence techniques.

Includes:

- SHAP explainability
- Local explanations
- Global explanations
- Surrogate model training
- Feature importance visualization
- Waterfall plots
- Bar plots
- GRAD-CAM local and global explanations
- GRAD-CAM visualizations

---

# Browser Extension Structure

```
clickbait-detector-extension/

├── backend/
│   ├── api/
│   ├── explainability/
│   ├── models/
│   ├── preprocessing/
│   ├── resources/
│   └── services/
│
├── extension/
│   ├── background/
│   ├── content/
│   ├── popup/
│   ├── assets/
│   ├── manifest.json
│   └── styles/
│
└── requirements.txt
```

## Backend

The backend is implemented using **FastAPI**.

Responsibilities include:

- Receiving requests from the browser extension
- Text preprocessing
- Metadata preprocessing
- Image preprocessing
- Loading trained models
- Performing clickbait prediction
- Generating SHAP explanations
- Returning prediction results via REST APIs

---

## Browser Extension

The Chrome extension performs:

- Hover detection
- Content extraction
- API communication
- Displaying prediction popup
- Displaying explanation popup

---

# Screenshots

The `screenshots` directory contains screenshots demonstrating:

- Browser extension interface
- Clickbait predictions
- Explainability results
- User interface workflow
- Unit testing results
- Integration testing results
- Performance testing
- Functional testing

---

# Technologies Used

- Python
- TensorFlow / Keras
- FastAPI
- SHAP
- GRAD-CAM
- NumPy
- Pandas
- Scikit-learn
- OpenCV
- JavaScript
- HTML
- CSS
- Chrome Extension APIs

---

# Running the Project Locally

## 1. Clone the Repository

```bash
git clone https://github.com/Iqrajan2024/An-Explainable-Deep-Learning-Framework-for-Clickbait-Detection-in-Headlines-and-YouTube-Videos.git

cd An-Explainable-Deep-Learning-Framework-for-Clickbait-Detection-in-Headlines-and-YouTube-Videos
```

---

## 2. Create a Virtual Environment

Windows

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add the Trained Models

Due to GitHub's file size limitations, the trained model files are **not included** in this repository.

Place the trained model files inside:

```
clickbait-detector-extension/backend/models/
```

Similarly, place any required background `.npy` resources inside:

```
clickbait-detector-extension/backend/resources/
```

---

## 5. Start the FastAPI Backend

Navigate to the backend directory and run:

```bash
uvicorn backend.api.app:app --reload
```

The backend will start at:

```
http://127.0.0.1:8000
```

---

# Loading the Chrome Extension

1. Open Google Chrome.
2. Navigate to:

```
chrome://extensions/
```

3. Enable **Developer Mode**.
4. Click **Load unpacked**.
5. Select the `clickbait-detector-extension/extension` folder.
6. Ensure the FastAPI backend is running.
7. Open any supported news website or YouTube.
8. Hover over a news headline or YouTube video to view clickbait predictions and explanations.

---

# Notes

- The trained deep learning models are excluded from this repository because they exceed GitHub's maximum file size limit.
- The notebooks are provided for reproducibility of the preprocessing, model training, and explainability workflow.

---

# Author

**Iqra Jan**
**Jawairia**

Bachelor of Science in Computer Science

University of Peshawar

Final Year Project

2026
