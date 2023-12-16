# Most Active Stocks Price Predictions and Visualizations

## Overview
This project aims to predict tomorrow's stock price (close price) for a specified ticker using Long Short-Term Memory (LSTM). The prediction is based on today's relevant stock information, including open, high, and low prices for the baseline model.

## Data Collection
We gathered stock data from Yahoo Finance using web scraping techniques. The acquired data underwent thorough cleaning and preprocessing. Additionally, we incorporated macroeconomic information such as interest rates and calculated technical data like moving averages.

## Model Training
The LSTM model was designed and trained using Tensorflow and Keras. Google Colab served as our platform for training, utilizing a dataset comprising the most active 250 stocks based on Yahoo Finance.

## Deployment
To make our predictions accessible and interactive, we deployed the model using Plotly Dash. This allows users to input a desired stock and receive a detailed financial graph. The graph includes technical indicators, aiding users in understanding the stock's past price movement and facilitating predictions of future trends.

## How to Use
Clone the repository to your local machine.
Ensure you have the required dependencies installed (Tensorflow, Keras, Plotly Dash).
Run the Plotly Dash application script.
Input the desired stock ticker.
Explore the detailed financial graph and technical indicators for insightful stock analysis.
Feel free to contribute, provide feedback, or customize the project for your specific needs!
