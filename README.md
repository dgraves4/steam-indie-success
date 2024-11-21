# Predicting Indie Game Success on Steam using Machine Learning

## Project Overview
This project aims to predict the success of indie games on Steam by analyzing game metadata, gameplay features, and community engagement data. By leveraging machine learning models such as Logistic Regression, Random Forest, and Support Vector Machine (SVM), we aim to identify key factors that contribute to a game's success. The project involves data collection via the Steam API, feature engineering, and extensive exploratory data analysis (EDA) to build predictive models. The insights gained can help indie developers optimize their games for better audience reception and provide consumers with more information about game quality.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Data Collection](#data-collection)
- [Data Cleaning and Feature Engineering](#data-cleaning-and-feature-engineering)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Results and Discussion](#results-and-discussion)
- [Limitations and Future Work](#limitations-and-future-work)
- [References](#references)
- [Links](#links)

## Project Structure
- `data/`: Contains raw and processed datasets (`steam_indie_games_all.csv`, `steam_indie_games_cleaned.csv`, `steam_indie_games_balanced.csv`).
- `notebooks/`: Jupyter notebooks used for data cleaning, exploration, feature engineering, model training, and evaluation. Notebooks include:
  - **Data Cleaning and EDA**: Cleaning the raw data, handling missing values, and initial exploration.
  - **Model Training and Evaluation**: Training models (Logistic Regression, Random Forest, SVM), hyperparameter tuning, and evaluating results.
- `src/`: Python scripts for:
  - **Data Collection** (`steam_data_collection.py`): Script used for initial data extraction from the Steam API, including handling rate limits.
- `results/`: Visualizations and performance metrics from the analysis, including correlation heatmaps, distribution plots, and model evaluation charts.
- `images/`: Contains diagrams and screenshots used in reporting (e.g., pipeline diagrams, flowcharts, code snippets, visuals).
- `README.md`: Overview and documentation of the project.
- `.env`: File to store environment variables (like Steam API keys).
- `.gitignore`: Specifies which files and directories should be ignored by Git (e.g., `.env`, virtual environment files, etc.).


## Installation and Setup
To set up this project locally, follow these steps:

1. **Clone the repository**:
```bash
   git clone https://github.com/dgraves4/steam-indie-success
   cd steam-indie-success
```

2. **Create and activate a virtual environment**

```bash
py -m venv .venv
source .venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure API access:

- Obtain an API key from the Steam API.
- Store the key in an environment variable or in a configuration file such as .env (ensure you include it in your .gitignore file to prevent it from being pushed to the repository).

5.  Jupyter Notebook Setup
- If using Jupyter notebooks for running analysis, ensure Jupyter is installed:

```bash
pip install jupyter
jupyter notebook
```

## Data Collection

Data was collected from the [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API), which provides extensive game metadata including game details, gameplay features, community engagement metrics, and user reviews. This project focuses on extracting key attributes like game price, release date, genre, developer information, and user recommendation counts to predict the success of indie games on the platform.

The data collection process involved:
- **API Requests**: A Python script (`steam_data_collection.py`) was used to collect data via API calls, including error handling for API rate limits (using retry logic and exponential backoff).
- **Balanced Dataset**: Data was curated to ensure a balanced representation of both popular and lesser-known indie games. The balancing aimed to avoid bias and ensure a fair distribution of recommendations.

For sample data and data processing scripts, refer to the `data/` folder and the `src/` directory.


### Data Attributes

| Column Name        | Description                                          | Data Type | Example Value        |
|--------------------|------------------------------------------------------|-----------|----------------------|
| AppID              | Unique identifier for each game                      | Integer   | 440                  |
| Game Name          | Title of the game                                    | String    | Team Fortress 2      |
| Release Date       | Date when the game was released                      | DateTime  | 2007-10-10           |
| Developer          | Developer(s) of the game                             | String    | Valve                |
| Genres             | Genres associated with the game                      | String    | Action, Free-to-Play |
| Price ($)          | Price of the game in USD                             | Float     | 19.99                |
| Recommendations    | Number of recommendations received (log transformed) | Float     | 10.82                |
| Years Since Release| Years since the game was released                    | Integer   | 17                   |

### Notes on Dataset

- **Data Source**: The dataset consists of indie games from the Steam platform, collected using the Steam Web API. This provides game-specific information, including release dates, developers, genres, and community reception metrics.
- **Feature Engineering**:
  - The "Release Date" column was converted to a `DateTime` data type for easier manipulation during analysis.
  - The "Recommendations" feature underwent a logarithmic transformation to address skewness and reduce the influence of outliers.
  - A new feature, "Years Since Release," was engineered to provide temporal context, aiding in the analysis of how game release longevity impacts success.
- **Data Formats**: The data was saved in two formats:
  - `steam_indie_games_all.csv` (full dataset with multiple cleaning versions)
  - `steam_indie_games_balanced.csv` (initial, uncleaned, balanced dataset for machine learning models)
- **Balanced Dataset**: The balanced dataset aimed to include a mix of both highly popular and lesser-known games to ensure a more representative analysis for machine learning models.

## Model Training and Evaluation

The models were trained on the processed dataset and evaluated using various metrics, including accuracy, precision, recall, and F1-score. The process involved an 80/20 stratified train-test split in an attempt to ensure class balance was maintained across both training and testing sets.

### Models Implemented
- **Logistic Regression**: Chosen as the baseline model for its simplicity and interpretability, allowing us to understand basic relationships between features and game success.
- **Random Forest**: Selected to capture more complex, non-linear relationships between features, given the mix of numerical and categorical data.
- **Support Vector Machine (SVM)**: Added to explore more complex decision boundaries, focusing on maximizing the margin between classes.

### Model Training Approach
- **Feature Engineering**: Initial training was conducted with basic features like "Recommendations." Additional features like "Price," "Years Since Release," and "Genres" were gradually added to enhance model accuracy.
- **Hyperparameter Tuning**: Hyperparameter tuning was conducted through `GridSearchCV` to optimize model performance for Random Forest and SVM, experimenting with different parameter combinations to improve accuracy and generalizability.

### Evaluation Metrics
Models were evaluated using:
- **Accuracy**: To measure the overall correctness of predictions.
- **Precision**: To understand how many of the predicted successes were actually successful.
- **Recall**: To determine the model's ability to identify all successful games.
- **F1-score**: To balance precision and recall, particularly useful given the potential class imbalance issues.

Currently, the Random Forest model with tuned hyperparameters provided the best performance in terms of accuracy. However, due to the inherent class imbalance in the dataset, further adjustments like class weighting or resampling are being considered to improve model reliability.


## Results and Discussion

### Model Performance Summary

The following table presents the evaluation metrics for the different machine learning models trained on the dataset. The metrics include Accuracy, Precision, and Recall for both classes (Class 0: Not Successful, Class 1: Successful).

| Model                           | Accuracy | Precision (Class 0) | Recall (Class 0) | Precision (Class 1) | Recall (Class 1) |
|---------------------------------|----------|---------------------|------------------|---------------------|------------------|
| Logistic Regression (Combined Features) | 56.90%   | 0.65                | 0.63             | 0.46                | 0.48             |
| Random Forest (Combined Features)       | 60.34%   | 0.66                | 0.71             | 0.50                | 0.43             |
| Tuned Random Forest                     | **66.00%**   | 0.67                | 0.86             | 0.62                | 0.35             |
| SVM (Combined Features)                 | 50.00%   | 0.58                | 0.60             | 0.36                | 0.35             |
| Tuned SVM                               | 55.17%   | 0.62                | 0.69             | 0.42                | 0.35             |

**Key Observations**:
- The **Tuned Random Forest** model achieved the highest accuracy of **66%**, demonstrating its ability to capture complex, non-linear relationships better than Logistic Regression and SVM.
- The **Recall (Class 0)** for the Tuned Random Forest model was notably high at **0.86**, indicating the model's strength in correctly identifying non-successful games.
- On the other hand, the **Recall (Class 1)** values were relatively low across all models, which suggests that predicting "Successful" games remains challenging, likely due to class imbalance in the dataset.

The insights gained from these results will help refine feature selection and further improve model performance, particularly focusing on boosting **Recall for Class 1** (Successful games) in future iterations.

## Limitations and Future Work

### Limitations
Some limitations encountered in this project include:

- **Potential biases in user reviews**: Reviews may not accurately represent the entire player base, as they could be biased by extreme experiences—either highly positive or highly negative. This may impact the reliability of "Recommendations" as a predictor of game success.
- **Class Imbalance**: The dataset had significantly more non-successful games compared to successful ones, which impacted model performance, particularly in accurately identifying successful games. This imbalance was partially addressed through stratified sampling and careful data selection, but it remains a challenge in improving predictive performance for lesser-known, successful indie games.
- **Data constraints for niche games**: Data availability for niche games was limited, which can impact the model's ability to generalize across the entire spectrum of indie games on Steam.
- **Modeling complex user behavior**: Predicting user behavior based on review sentiment and game metadata is inherently complex due to individual player motivations and preferences. The models used in this project may struggle to capture these nuances fully.

### Future Work
Future improvements and extensions for this project could include:

- **Addressing Class Imbalance**: Implementing techniques like Synthetic Minority Over-sampling Technique (SMOTE) or experimenting with different class weights to address class imbalance and improve recall for the "successful" class.
- **Exploring Additional Platforms**: Collecting data from other gaming platforms beyond Steam, such as the Epic Games Store or Microsoft Store, to enhance the generalizability of the model.
- **Advanced Modeling Techniques**: Implementing more sophisticated models, such as deep learning, to capture more nuanced sentiment and complex patterns in user behavior, potentially improving prediction accuracy.
- **Sentiment Analysis of Reviews**: Adding sentiment analysis of user reviews to quantify the qualitative aspects of player feedback. This could be used as an additional feature to help predict game success more accurately.
- **Hyperparameter Tuning Automation**: Exploring automated hyperparameter tuning approaches, such as Bayesian optimization, to reduce the manual effort required for model improvement.
- **Real-time Data Integration**: Integrating real-time data using the Steam API to track ongoing changes in player sentiment and game engagement, which could make the prediction dynamic and timely.

## References

- Bellavista, P., Corradi, A., & Stefanelli, C. (2001). [Mobile agent middleware for mobile computing](https://doi.org/10.1109/2.910896). *Computer, 34*(3), 73-81.
- Kirasich, K., Smith, T., & Sadler, B. (2018). [Random Forest vs Logistic Regression: Binary Classification for Heterogeneous Datasets](https://scholar.smu.edu/datasciencereview/vol1/iss3/9). *SMU Data Science Review, 1*(3), Article 9. Creative Commons License.
- Lounela, K. (2024). [On Identifying Relevant Features for a Successful Indie Video Game Release on Steam](https://aaltodoc.aalto.fi/items/d578980e-71fa-4618-b500-dff30bbac490). *Master’s Programme in Department of Information and Service Management*.

## Links
- [Overleaf Project Report](https://www.overleaf.com/read/nkwywqzxpcwr#cf3410)
- [GitHub Repository](https://github.com/dgraves4/steam-indie-success)
