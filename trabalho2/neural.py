

import sys
import csv
import glob
import pprint
import random
import copy
import math
import numpy


class Input(object):
    def __init__(self,values):
        self.values = values

class Output(object):
    def __init__(self,output = 0):
        self.output = output

class Window(object):
    def __init__(self):
        self.inputs = []
        self.outputs = []
    
    def add_input(self, values):
        self.inputs.append(values)
    
    def add_output(self, value):
        self.outputs.append(value)

    def get_median_inputs(self):
        values = [ float(x) for x in self.inputs[0]]
        nwin = len(self.inputs)
        for i in range(1,nwin):
            for j in range(len(self.inputs[i])):
                values[j] = values[j] + float(self.inputs[i][j])

        for i in range(len(values)):
            values[i] = values[i]/nwin
        """ 
        return Input(values) """
        return values

    def get_median_output(self):
        value = float(self.outputs[0])
        nwin = len(self.outputs)
        for i in range(1,nwin):
            value = value + float(self.outputs[i])
        value = value/nwin

        """         return Output(value) """
        return value

        



    


class Neural_Network(object):
    def __init__(self):
        self.n_inputs = 8
        self.hidden_nodes = arguments['hnodes']
        
        self.weight_input = numpy.random.randn(self.n_inputs,self.hidden_nodes)
        """ self.weight_input =  []
        for _ in range(self.n_inputs):
            arr = [random.random() for j in range(self.hidden_nodes)]            
            self.weight_input.append(arr) """

        self.weight_hnodes = numpy.random.randn(self.hidden_nodes,1)
        """ self.weight_hnodes = [random.random() for j in range(self.hidden_nodes)] """

    def sigmoid(self,x):
        return 1/(1+numpy.exp(-x))

    def forward(self,inputs):

        z = numpy.dot(inputs, self.weight_input)
        
        z2 = self.sigmoid(z)

        z3 = numpy.dot(z2,self.weight_hnodes)

        return self.sigmoid(z3)

    def sigmoidPrime(self,x):
        return x*(1-x)

    

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
    window_list = []
    file_list = glob.glob(arguments['path'] + 'd?p[0-9]*[MF]')
    test_files = random.sample(file_list,k=int(len(file_list)*2/3))

    for file in test_files:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            time_slot = 0
            win = Window()
            for row in reader:
                inputs = row[1:-1] # copiar tudo menos o ultimo que e' o output e o tempo
                if len(row) == 9:
                    gender = file[-1:]
                    if gender == 'M':
                        inputs.append(1)
                    else:
                        inputs.append(2)

                    curr_slot = float(row[0])/arguments['window']
                    
                    if curr_slot > time_slot +1:
                        window_list.append(win)
                        win = Window()

                    win.add_input(inputs)
                    win.add_output(row[8])
                    time_slot = time_slot +1
                    
                    #print('time',row[0])
                    #print('GF',row[1])
                    #print('GV',row[2])
                    #print('GL',row[3])
                    #print('antenna',row[4])
                    #print('rssi',row[5])
                    #print('phase',row[6])
                    #print('freq',row[7])
                    #print('gender',file[-1:])
                    #print('expected_output',row[8])

            window_list.append(win)
                    
    return window_list

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(file_list)

file_list = []
test_files = []
training_inputs = None
training_outputs = None
arguments = {'window' : 5, 'hnodes' : 8, 'rate':0.03, 'sample':0.75}

neural_net = Neural_Network()

if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        if sys.argv[1].find('=') > 0:
            args = sys.argv[1].split('=')
            if args[0] != 'path':
                arguments[args[0]] = float(args[1])
            else:
                if args[1][len(args[1])-1] == '\\':
                    arguments[args[0]] = args[1]
                else:
                    arguments[args[0]] = args[1] + '\\'

    if 'path' not in  arguments:
        print('ERROR no path to dataset specified')
    else:
        #set defaults
        window_list = read_data_sets()
        training_inputs = numpy.array([window_list[i].get_median_inputs() for i in range(len(window_list))], dtype=float)
        training_outputs = numpy.array([window_list[i].get_median_output() for i in range(len(window_list))], dtype=float)
        """ for i in range(len(window_list)):
            training_inputs.append(window_list[i].get_median_inputs())
            training_outputs.append(window_list[i].get_median_output()) """

        #scale
        training_inputs = training_inputs /numpy.amax(training_inputs,axis=0)
        training_outputs = training_outputs/10

        print('neural_net: ', neural_net.forward(training_inputs)   )
        print('expected_output', training_outputs)




else:
    print('path=[path_to_dataset]')
    print('window=[sliding window size in seconds] -> default 5 seconds')
    print('hnodes=[number_of__hidden_nodes] -> default 8 = inputs-1')
    print('rate=[learning_rate] = default 0.03')
    print('sample=[sample_rate] -> default 0.75 = 75% training, 25% test')






