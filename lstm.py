import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM

# TODO: Define class LSTM with functions for training, testing and saving the model and trained weights

class LSTM_Models:
    def single_feature_vanilla_lstm(neurons, n_steps, self):
        model = Sequential()
        model.add(LSTM(neurons, activation='relu', input_shape=(n_steps, 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    def multiple_feature_vanilla_lstm(neurons, n_steps, n_features, self):
        model = Sequential()
        model.add(LSTM(neurons, activation='relu', input_shape=(n_steps, n_features)))
        model.add(Dense(30))
        model.compile(optimizer='adam', loss='mse')
        return model


if __name__ == "__main__":
    file_path = "./data/F.txt"
    signal_df = pd.read_csv(file_path, delimiter="\t", names=['Inst1', 'Inst2', 'Inst3', 'Inst4'])
    print(signal_df.head())
    print("Read input file into dataframe")
