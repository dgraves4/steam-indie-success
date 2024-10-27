# Predicting Indie Game Success on Steam using Sentiment Analysis and Machine Learning

## Project Overview
This project analyzes user reviews and metadata of indie games on Steam to predict their success. By leveraging sentiment analysis and machine learning models (such as Random Forest and Logistic Regression), this project aims to identify key factors that contribute to a game's popularity. The insights gained from this analysis could help indie developers optimize their games for better audience reception, and could also be useful to the consumer.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Data Collection](#data-collection)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Results and Discussion](#results-and-discussion)
- [Limitations and Future Work](#limitations-and-future-work)
- [References](#references)
- [Links](#links)

## Project Structure
├── data/ # Folder containing raw and processed data ├── notebooks/ # Jupyter notebooks for data analysis and model training ├── src/ # Python scripts for data processing, model training, and evaluation ├── models/ # Saved models and serialized files ├── README.md # Project overview and instructions └── requirements.txt # Python dependencies for the project

bash
Copy code

## Installation and Setup
To set up this project locally, follow these steps:

1. **Clone the repository**:
```bash
   git clone https://github.com/dgraves4/steam-indie-success.git
   cd steam-indie-success
```

2. **Create and activate a virtual environment**

```bash
py -m venv .venv
source env/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```
4. Configure API access (if applicable):

Obtain an API key from the Steam API.
Store the key in an environment variable or in a configuration file as needed.

## Data Collection

Data is sourced from the [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API), which provides access to user reviews and game metadata. This project focuses on extracting sentiment data, gameplay features, and game popularity indicators. For sample data (if available) and data processing scripts, refer to the `data/` folder and the `src/` directory.

## Model Training and Evaluation

The models are trained on the processed dataset and evaluated using various metrics, including accuracy, precision, recall, and F1-score. Initial models implemented include:
- **Random Forest**
- **Logistic Regression**

Hyperparameter tuning is conducted through grid search to optimize model performance. For detailed steps in the model training process, refer to the Jupyter notebooks available in the `notebooks/` directory.

## Results and Discussion

This section will present the outcomes of the model evaluations and key insights gained from the analysis. Specific findings and visualizations will be provided once model training is complete, offering actionable insights for indie game developers.


## Limitations and Future Work

Some limitations encountered in this project include:

- **Potential biases in user reviews**: Reviews may not accurately represent the entire player base, as they could be biased by extreme experiences (either highly positive or highly negative).
- **Constraints in the data for niche games**: Data availability for niche games may be limited, impacting the model's ability to generalize across all indie games.
- **Modeling complex user behavior**: Understanding and predicting user behavior based on review sentiment and metadata remains challenging due to the complexity of individual player motivations and preferences.

### Future Work
Future improvements and extensions for this project could include:

- **Exploring additional platforms**: Collecting data from other gaming platforms beyond Steam to enhance the generalizability of the model.
- **Advanced deep learning techniques**: Implementing more sophisticated models, such as neural networks or deep learning models, to capture more nuanced sentiment and complex patterns in user behavior for improved prediction accuracy.

## References
- Guzsvinecz, T., & Szűcs, J. (2022). [Length and Sentiment Analysis of Reviews about Top-Level Video Game Genres on the Steam Platform](https://www.sciencedirect.com/science/article/pii/S0747563223003060). *Computers in Human Behavior*.
- Lounela, K. (2024). [On Identifying Relevant Features for a Successful Indie Video Game Release on Steam](https://aaltodoc.aalto.fi/items/d578980e-71fa-4618-b500-dff30bbac490). *Master’s Programme in Department of Information and Service Management*.

## Links
- [Overleaf Project Report](https://www.overleaf.com/read/nkwywqzxpcwr#cf3410)
- [GitHub Repository](https://github.com/dgraves4/steam-indie-success)
