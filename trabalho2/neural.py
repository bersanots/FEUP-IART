#!/usr/bin/python3

import sys
import csv
import glob
import pprint
import random


class Input_node(object):
    def __init__(self, name, val):
        self.name = name
        self.value = val
        self.wheights = []

class Input_weight(object):
    def __init__(self, weight, node):
        self.weight = weight
        self.node = node

class Node(object):
    def __init__(self):
        self.input_w = []
        self.node_w = []


class Node_weight(object):
    def __init__(self, weight, node):
        self.weight = weight
        self.node = node

class Output(object):
    def __init__(self,output = 0):
        self.node_w = []
        self.output = output

class Window(object):
    def __init__(self,inputs,output = None):
        self.inputs = inputs
        self.expected_output = output

    


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
def read_data_sets(set):
    window_list = []
    file_list = glob.glob(set + 'd?p[0-9]*[MF]')
    test_files = random.sample(file_list,k=int(len(file_list)*2/3))

    for file in test_files:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            for row in reader:
                inputs = []
                if len(row) == 9:
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
                    inputs.append(Input_node('time',row[0]))
                    inputs.append(Input_node('GF',row[1]))
                    inputs.append(Input_node('GV',row[2]))
                    inputs.append(Input_node('GL',row[3]))
                    inputs.append(Input_node('antenna',row[4]))
                    inputs.append(Input_node('rssi',row[5]))
                    inputs.append(Input_node('phase',row[6]))
                    inputs.append(Input_node('freq',row[7]))
                    gender = file[-1:]
                    if gender == 'M':
                        inputs.append(Input_node('gender',0))
                    else:
                        inputs.append(Input_node('gender',1))
                    window_list.append(Window(inputs,Output(row[8])))
    return window_list

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(file_list)

if len(sys.argv) > 1:
    window_list = read_data_sets(sys.argv[1])
else:
    print('first argument should be path to dataset folder')






