import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    file_path = "./data/F.txt"
    signal_df = pd.read_csv(file_path, delimiter="\t", names=['Inst1', 'Inst2', 'Inst3', 'Inst4'])
    print(signal_df.head())
    print("Read input file into dataframe")
    print("Plotting the patterns for the 4 different instruments.")
    plt.plot(signal_df['Inst1'], color='red', label='Inst1')
    plt.plot(signal_df['Inst2'], color='blue', label='Inst2')
    plt.plot(signal_df['Inst3'], color='green', label='Inst3')
    plt.plot(signal_df['Inst4'], color='yellow', label='Inst4')
    plt.legend(title='Instrument')
    plt.xlabel('Time Step')
    plt.ylabel('Key Number')
    plt.title('Key Number by Time Step')
    plt.savefig('./data/key_time_plt.png')
    print("\nMin-Max and Unique Keys for each instrument:\n")
    for col in signal_df.columns:
        print('{}: Max: {}, Min: {}, Unique Keys: {}'.format(col, max(signal_df[col]), min(signal_df[col]), len(signal_df[col].unique())-1))
    pass
