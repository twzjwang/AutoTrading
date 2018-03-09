import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data(path):
    data = np.genfromtxt(path, delimiter=',')
    return data

class Trader():
    # i : current index, n : n days MA
    def count_MA(self, data, i, n):
        sum = 0
        for i in range(i-n+1, i+1):
            sum = sum + data[i][3]
        return sum / n

    def train(self, data):
        moving_average = np.full((len(data), 2), 0)
        max_value = 0
        max_ma_a = 5
        max_ma_b = 20
        for ma_a in range(5,6):
            for ma_b in range(10, 11):
                for i in range(4,len(data)):
                    if i >= ma_b - 1:
                        moving_average[i][1] = self.count_MA(data, i, ma_b)
                    moving_average[i][0] = self.count_MA(data, i, ma_a)
        return moving_average

    def predict_action(self, index, training_data, moving_average,  hold):
 
        action = '0'
        if (moving_average[index-2][0] < moving_average[index-2][1]) and (moving_average[index-1][0] > moving_average[index-1][1]) and (hold < 1):
            action = '1'
        if (moving_average[index-2][0] > moving_average[index-2][1]) and (moving_average[index-1][0] < moving_average[index-1][1]) and (hold > -1):
            action = '-1'
        if (moving_average[index-1][0] < moving_average[index-1][1]) and (moving_average[index][0] > moving_average[index][1]) and (hold < 1):
            action = '1'
        if (moving_average[index-1][0] > moving_average[index-1][1]) and (moving_average[index][0] < moving_average[index][1]) and (hold > -1):
            action = '-1'
        return action

    def re_training(self, data):
        print('re_training')
    

# You can write code above the if-main block.

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')

    args = parser.parse_args()
    
    # The following part is an example.
    # You can modify it at will.
    training_data = load_data(args.training)
    trader = Trader()
    moving_average = trader.train(training_data)
    ma_a = 5
    ma_b = 20
    training_data_len = len(training_data)    

    testing_data = load_data(args.testing)
    hold = 0    
    with open(args.output, 'w') as output_file:
        for row in testing_data:
            # skip the last day 
            if((row == testing_data[len(testing_data)-1]).all()):
                break
            # We will perform your action as the open price in the next day.
            index = len(training_data)
            training_data = np.vstack((training_data, row))
            moving_average = np.vstack((moving_average, [trader.count_MA(training_data, index, ma_a), trader.count_MA(training_data, index, ma_b)]))
            action = trader.predict_action(index, training_data, moving_average, hold)
            if action == '1':
                hold = hold + 1
            if action == '-1':
                hold = hold - 1
            if hold > 1 or hold < -1:
                input('error')
            output_file.write(action+'\n')

            # this is your option, you can leave it empty.
            #trader.re_training(i)
