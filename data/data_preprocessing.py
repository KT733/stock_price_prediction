import pandas as pd
import numpy as np

def shift_data(X, y, time_step):
    """
    Shifts the input features (X) and target variable (y) based on the specified time step.

    Parameters:
    - X (pd.DataFrame): Input features DataFrame.
    - y (pd.Series): Target variable Series.
    - time_step (int): Number of time steps to shift the data.

    Returns:
    - pd.DataFrame, pd.Series: Shifted input features (X) and target variable (y).
    """
    X = X.iloc[:-time_step]
    y = y.iloc[time_step:]
    return X, y

def data_preprocessing1(df):
    """
    Perform data preprocessing on the given DataFrame.

    This function keeps only the necessary columns ('Open', 'High', 'Low', 'Close'),
    shifts the data by one time step, and performs a train-validation-test split.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing financial data.

    Returns:
    - X_train, X_val, X_test: Input features for training, validation, and testing sets.
    - y_train, y_val, y_test: Target variable for training, validation, and testing sets.
    """
    # keep necessary columns
    col_list = ["Open", "High", "Low", "Close"]
    df = df[col_list]

    X = df.drop(['Close'],axis = 1)
    y = df['Close']

    X, y = shift_data(X, y, 1)

    # train validation test split
    X_train, X_val, y_train, y_val = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=42,
                                                        shuffle=False)
    X_val, X_test, y_val, y_test = train_test_split(X_val, y_val,
                                                        test_size=0.2,
                                                        random_state=42,
                                                        shuffle=False)

    return X_train, X_val, X_test, y_train, y_val, y_test

def reshape_X(X_train, X_test, X_val):
    """
    Reshape input feature sets for compatibility with LSTM.

    This function converts input DataFrames to NumPy arrays and reshapes them to have an
    additional dimension, usually required for input to neural networks with sequential data.

    Parameters:
    - X_train (pd.DataFrame): Input features for training set.
    - X_test (pd.DataFrame): Input features for testing set.
    - X_val (pd.DataFrame): Input features for validation set.

    Returns:
    X_train, X_test, X_val: Reshaped input feature arrays.
    """
    X_train = X_train.to_numpy().reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.to_numpy().reshape(X_test.shape[0], X_test.shape[1], 1)
    X_val = X_val.to_numpy().reshape(X_val.shape[0], X_val.shape[1], 1)

    return X_train, X_test, X_val
