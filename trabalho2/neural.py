

import sys
import csv
import glob
import pprint
import random
import copy
import math
import numpy
import os


class Input(object):
    def __init__(self,values):
        self.values = values

class Output(object):
    def __init__(self,output = 0):
        self.output = output

class Window(object):
    def __init__(self):
        self.lines = []
        self.inputs = []
        self.outputs = []

    def add_lines(self, line):
        self.lines.append(line)

    def filter_lines(self):
        #filter diferent outputs
        n_ouputs = {}
        for l in self.lines:
            if l["output"] in n_ouputs:
                n_ouputs[l["output"]] = n_ouputs[l["output"]] +1
            else:
                n_ouputs[l["output"]] = 1
        output_king = max(n_ouputs,key=n_ouputs.get)

        for l in self.lines:
            if l["output"] != output_king:
                self.lines.remove(l)

        #add filtered lines
        for l in self.lines:
            ip = list(l.values())
            self.inputs.append(ip[:-1]) #add all except output
            self.outputs.append(ip[-1:])

    
    def get_median_inputs(self):
        values = [ float(x) for x in self.inputs[0]]
        nwin = len(self.inputs)
        for i in range(1,nwin):
            for j in range(len(self.inputs[i])):
                values[j] = values[j] + float(self.inputs[i][j])

        for i in range(len(values)):
            values[i] = values[i]/nwin

        return values

    def get_median_output(self):
        value = [float(self.outputs[0][0])]
        return value


class Neural_Network(object):
    def __init__(self):
        self.n_inputs = 8
        self.hidden_nodes = arguments['hnodes']
        
        self.weight_input = numpy.random.randn(self.n_inputs,self.hidden_nodes)

        self.weight_hnodes = numpy.random.randn(self.hidden_nodes,1)

    def sigmoid(self,x):
        return 1/(1+numpy.exp(-x))

    def forward(self,inputs):

        z = numpy.dot(inputs, self.weight_input)
        
        self.act_function = self.sigmoid(z)

        z3 = numpy.dot(self.act_function,self.weight_hnodes)

        return self.sigmoid(z3)

    def sigmoidPrime(self,x):
        return x*(1-x)

    def backward(self, input, act_output, predicted):
        self.p_error = act_output - predicted
        self.p_delta = self.p_error*self.sigmoidPrime(predicted)

        self.h_error = self.p_delta.dot(self.weight_hnodes.T)
        self.h_delta = self.h_error*self.sigmoidPrime(self.act_function)

        self.weight_input += input.T.dot(self.h_delta)
        self.weight_hnodes += self.act_function.T.dot(self.p_delta)

    def train(self, input, act_output):
        o = self.forward(input)
        self.backward(input,act_output,o)

    
window_list = []
file_list = []
test_files = []
training_window = []
training_inputs = None
training_outputs = None
test_window = []
arguments = {'window' : 5, 'hnodes' : 8, 'rate':0.03, 'sample':0.75, 'iterations':1000}


'''
Column 1: Time in seconds 
Column 2: Acceleration reading in G for frontal axis 
Column 3: Acceleration reading in G for vertical axis 
Column 4: Acceleration reading in G for lateral axis 
Column 5: Id of antenna reading sensor 
Column 6: Received signal strength indicator (RSSI) 
Column 7: Phase 
Column 8: Frequency 
Column 9: Label of activity, 1: sit on bed, 2: sit on chair, 3: lying, 4: ambulating 
In addition, gender of participant is included in the last character of file name eg: d1p33F (F:female).
'''
def read_data_sets():
    file_list = glob.glob(arguments['path'] + 'd?p[0-9]*[MF]')

    for file in file_list:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            time_slot = 0
            win = Window()
            for row in reader:
                if len(row) == 9:
                    
                    gender = file[-1:]
                    g = 1
                    if gender != 'M':
                        g = 2
                    inputs = { 
                        'GF' : row[1],
                        'GV':row[2],
                        'GL':row[3],
                        'antenna':row[4],
                        'rssi':row[5],
                        'phase':row[6],
                        'freq':row[7],
                        'gender' : g,
                        'output':row[8]
                        }

                    curr_slot = float(row[0])/arguments['window']
                    
                    if curr_slot > time_slot +1:
                        window_list.append(win)
                        win = Window()

                    win.add_lines(inputs)
                    
                    time_slot = time_slot +1

            window_list.append(win)
    
    random.shuffle(window_list)


neural_net = Neural_Network()

if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        if sys.argv[i].find('=') > 0:
            args = sys.argv[i].split('=')
            if args[0] != 'path':
                arguments[args[0]] = float(args[1])
            else:
                arguments[args[0]] = os.path.join(args[1], '') #add trailing slash, os independent

    if 'path' not in  arguments:
        print('ERROR no path to dataset specified')
    else:
        #set defaults
        read_data_sets()
        sample = int(len(window_list)*arguments["sample"])
        training_window.extend( window_list[:sample])
        test_window.extend( window_list[sample:])

        arr_i = []
        arr_o = []
        for w in training_window:
            w.filter_lines()
            arr_i.append(w.get_median_inputs())
            arr_o.append(w.get_median_output())

        training_inputs = numpy.array(arr_i, dtype=float)
        training_outputs = numpy.array(arr_o, dtype=float)
 
        #scale
        training_inputs = training_inputs /numpy.amax(training_inputs,axis=0)
        training_outputs = training_outputs/4 #4 # val max de output


else:
    print('path=[path_to_dataset]')
    print('window=[sliding window size in seconds] -> default 5 seconds')
    print('hnodes=[number_of__hidden_nodes] -> default 8 = inputs-1')
    print('iterations=[iterations] = default 1000')
    print('sample=[sample_rate] -> default 0.75 = 75% training, 25% test')


for i in range(int(arguments['iterations'])):
    neural_net.train(training_inputs,training_outputs)

arr_i = []
arr_o = []
for w in test_window:
    w.filter_lines()
    arr_i.append(w.get_median_inputs())
    arr_o.append(w.get_median_output())

test_input =  numpy.array(arr_i, dtype=float)
test_output = numpy.array(arr_o, dtype=float)

 #scale
test_input = test_input /numpy.amax(test_input,axis=0)
test_output = test_output/4 #4 # val max de output


predicted_out = neural_net.forward(test_input)

for i in range(len(test_output)):
    print("actual = ", 4*test_output[i]," predicted = ",4*predicted_out[i])

print("Training Loss: ", str(numpy.mean(numpy.square(training_outputs - neural_net.forward(training_inputs)))))
print("Testing Loss: ", str(numpy.mean(numpy.square(test_output - predicted_out))))

