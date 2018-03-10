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
        moving_average = np.full((len(data), 3), 0)
        max_value = 0
        for ma_a in range(5,6):
            for ma_b in range(10, 11):
                for i in range(4,len(data)):
                    if i >= ma_b - 1:
                        moving_average[i][1] = self.count_MA(data, i, ma_b)
                    if i >= ma_c - 1:
                        moving_average[i][2] = self.count_MA(data, i, ma_c)
                    moving_average[i][0] = self.count_MA(data, i, ma_a)
        return moving_average

    def predict_action(self, index, training_data, moving_average,  hold):
        action = 0

        weight_a = 1
        weight_b = 1

        #price cross MA
        if (training_data[index-1][3] < moving_average[index-1][1]) and (training_data[index][3] > moving_average[index][1]):
            action = action + weight_a
        if (training_data[index-1][3] > moving_average[index-1][1]) and (training_data[index][3] < moving_average[index][1]):
            action = action - weight_a
        if (training_data[index-1][3] < moving_average[index-1][2]) and (training_data[index][3] > moving_average[index][2]):
            action = action + weight_a
        if (training_data[index-1][3] > moving_average[index-1][2]) and (training_data[index][3] < moving_average[index][2]):
            action = action - weight_a

        #short cross long
        if (moving_average[index-1][0] < moving_average[index-1][1]) and (moving_average[index][0] > moving_average[index][1]):
            action = action + weight_b
        if (moving_average[index-1][0] > moving_average[index-1][1]) and (moving_average[index][0] < moving_average[index][1]):
            action = action - weight_b
        if (moving_average[index-1][1] < moving_average[index-1][2]) and (moving_average[index][1] > moving_average[index][2]):
            action = action + weight_b
        if (moving_average[index-1][1] > moving_average[index-1][2]) and (moving_average[index][1] < moving_average[index][2]):
            action = action - weight_b

        if (hold < 1) and (action > 0):
            return '1'
        if (hold > -1) and (action < 0):
            return '-1'
        return '0'

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
    ma_a = 5 
    ma_b = 15
    ma_c = 120
    moving_average = trader.train(training_data)
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
            moving_average = np.vstack((moving_average, [trader.count_MA(training_data, index, ma_a), trader.count_MA(training_data, index, ma_b), trader.count_MA(training_data, index, ma_c)]))
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
