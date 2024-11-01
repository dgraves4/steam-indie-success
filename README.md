# Predicting Indie Game Success on Steam using Sentiment Analysis and Machine Learning

## Project Overview
This project analyzes user reviews and metadata of indie games on Steam to predict their success. By leveraging sentiment analysis and machine learning models (such as Random Forest and Logistic Regression), this project aims to identify key factors that contribute to a game's popularity. The insights gained from this analysis could help indie developers optimize their games for better audience reception and could also be useful to consumers.

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
- `data/`: Contains raw and processed datasets.
- `notebooks/`: Jupyter notebooks used for data exploration, feature engineering, and model training.
- `src/`: Python scripts for data collection and model training.
- `results/`: Visualizations and results from the analysis.
- `README.md`: Overview and documentation of the project.
- `.env`: File to store environment variables (like Steam API keys).

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
source .venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```
4. Configure API access (if applicable):

Obtain an API key from the Steam API.
Store the key in an environment variable or in a configuration file such as needed (ensure you include it in your .gitignore file).

## Data Collection

Data is sourced from the [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API), which provides access to user reviews and game metadata. This project focuses on extracting sentiment data, gameplay features, and game popularity indicators. For sample data (if available) and data processing scripts, refer to the `data/` folder and the `src/` directory.

### Data Attributes

| Column Name        | Description                                          | Data Type | Example Value        |
|--------------------|------------------------------------------------------|-----------|----------------------|
| AppID              | Unique identifier for each game                      | Integer   | 440                  |
| Game Name          | Title of the game                                    | String    | Team Fortress 2      |
| Release Date       | Date when the game was released                      | String    | October 10, 2007     |
| Developer          | Developer(s) of the game                             | String    | Valve                |
| Genres             | Genres associated with the game                      | String    | Action, Free-to-Play |
| Price ($)          | Price of the game in USD                             | Float     | 19.99                |
| Recommendations    | Number of recommendations received                   | Integer   | 50000                |

### Additional Notes

- The dataset consists of indie games from the Steam platform.
- Each game is represented with its `AppID`, name, and other relevant metadata.
- The dataset was collected using the Steam Web API, which allows us to gather game-specific information, including release dates, developers, genres, and community reception.

## Model Training and Evaluation

The models are trained on the processed dataset and evaluated using various metrics, including accuracy, precision, recall, and F1-score. Initial models implemented include:
- **Random Forest**
- **Logistic Regression**

Hyperparameter tuning is conducted through grid search to optimize model performance. 

## Results and Discussion

This section will present the outcomes of the model evaluations and key insights gained from the analysis. Specific findings and visualizations will be provided once model training is complete, offering actionable insights for indie game developers.

## Limitations and Future Work

Some limitations encountered in this project include:

- **Potential biases in user reviews**: Reviews may not accurately represent the entire player base, as they could be biased by extreme experiences (either highly positive or highly negative).
- **Constraints in the data for niche games**: Data availability for niche games may be limited, impacting the model's ability to generalize across all indie games.
- **Modeling complex user behavior**: Understanding and predicting user behavior based on review sentiment and metadata remains challenging due to the complexity of individual player motivations and preferences.

### Future Work
Future improvements and extensions for this project could include:

- **Exploring additional platforms**: Collecting data from other gaming platforms beyond Steam to enhance the generalizability of the model, such as the Epic Games Store or Microsoft Store for PC.
- **Advanced deep learning techniques**: Implementing more sophisticated models, such as neural networks or deep learning models, to capture more nuanced sentiment and complex patterns in user behavior for improved prediction accuracy.

## References

- Guzsvinecz, T., & Szűcs, J. (2022). [Length and Sentiment Analysis of Reviews about Top-Level Video Game Genres on the Steam Platform](https://www.sciencedirect.com/science/article/pii/S0747563223003060). *Computers in Human Behavior*.
- Lounela, K. (2024). [On Identifying Relevant Features for a Successful Indie Video Game Release on Steam](https://aaltodoc.aalto.fi/items/d578980e-71fa-4618-b500-dff30bbac490). *Master’s Programme in Department of Information and Service Management*.
- Kirasich, K., Smith, T., & Sadler, B. (2018). [Random Forest vs Logistic Regression: Binary Classification for Heterogeneous Datasets](https://scholar.smu.edu/datasciencereview/vol1/iss3/9). *SMU Data Science Review, 1*(3), Article 9. Creative Commons License.


## Links
- [Overleaf Project Report](https://www.overleaf.com/read/nkwywqzxpcwr#cf3410)
- [GitHub Repository](https://github.com/dgraves4/steam-indie-success)
