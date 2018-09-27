# Sharma, Roopam
# 1001-559-960
# 2018-09-24
# Assignment-02-02
import numpy as np

# This module calculates the activation function for meshgrid
def calculate_activation_function(weights,bias,input_data,type='SymmetricHardLimit'):
    net_value = weights[0] * input_data[0]+weights[1]*input_data[1]+ bias
    activation = []
    if type == 'SymmetricHardLimit':
        net_value[net_value>0] = 1
        net_value[net_value<0] = -1
        activation = net_value
    elif type == "Linear":
        activation = net_value
    elif type == "tanh":
        activation = (np.exp(net_value)-np.exp(-net_value))/(np.exp(net_value)+np.exp(-net_value))
    return activation

# This module calculates the error on each data point and updates wrights and bias
def calculate_error(weights,bias,input_data,type='SymmetricHardLimit'):
    for i in range(len(input_data)):
        a = calculate_activation1(weights,bias,input_data.iloc[i,0:2],type)
        e = input_data.iloc[i,2]-a
        print("Error :",e)
        weights = weights + e*input_data.iloc[i,0:2].values
        bias = bias + e
    return  weights,bias

# helper function for calculating activation for updating weights and bais
def calculate_activation1(weights,bias,input_data,type='SymmetricHardLimit'):
    net_value = weights[0] * input_data[0]+weights[1]*input_data[1]+ bias
    activation = []
    if type == 'SymmetricHardLimit':
        if net_value>0:
            activation = 1
        else:
            activation = -1
    elif type == "Linear":
        activation = net_value
    elif type == "tanh":
        activation = (np.exp(net_value)-np.exp(-net_value))/(np.exp(net_value)+np.exp(-net_value))
    return activation