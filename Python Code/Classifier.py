import inspect
import sys
import numpy as np
import math

'''
Raise a "not defined" exception as a reminder 
'''
def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)


'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit) 
'''
def extract_basic_features(digit_data, width, height):
    features=[[0] * height for i in range(width)]
    for m in range(height):
        for n in range(width):
            if digit_data[m][n] == 0 or digit_data[m][n] == ' ':
                features[m][n] = False
            else:
                features[m][n] = True
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here
    return features
''' 
Extract advanced features that you will come up with 
'''
def extract_advanced_features(digit_data, width, height):
    features = []
    features1 = [[0] * height for i in range(width)]
    features2 = [[0] * height for h in range(width)]
    features3 = 0
    for m in range(height):
        for n in range(width):
            if digit_data[m][n] == 0 or digit_data[m][n] == ' ':
                features1[m][n] = False
                features2[m][n] = False
            elif digit_data[m][n] == 1 or digit_data[m][n] == '#':
                features1[m][n] = True
                features2[m][n] = False
            else:
                features1[m][n] = False
                features2[m][n] = True
                features3 += 1

    features.append(features1)
    features.append(features2)
    features.append(features3)
    return features
def extract_advanced_features2(digit_data, width, height):
    features = []
    features1 = [[0] * height for i in range(width)]
    features2 = [[0] * height for h in range(width)]
    features3 = 0
    features4 = [[0] * height for j in range(width)]
    for m in range(height):
        for n in range(width):
            if digit_data[m][n] == 0 or digit_data[m][n] == ' ':
                features1[m][n] = False
                features2[m][n] = False
                features4[m][n] = False
            elif digit_data[m][n] == 1 or digit_data[m][n] == '#':
                features1[m][n] = True
                features2[m][n] = False
                features4[m][n] = True
            else:
                features1[m][n] = False
                features2[m][n] = True
                features4[m][n] = False
                features3 += 1

    features.append(features1)
    features.append(features2)
    features.append(features3)
    features.append(features4)
    return features

'''
Extract the final features that you would like to use
'''
def extract_final_features(digit_data, width, height):
    features = [[0] * height for i in range(width)]
    for m in range(height):
        for n in range(width):
            if digit_data[m][n] == 1 or digit_data[m][n] == ' ':
                features[m][n] = True
            else:
                features[m][n] = False
    return features
'''
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training. 
'''
statsF = [0.0]*10 #cond. prob. for features
stats = [0.0]* 10 #
prior = [0.0]*10 # prior for classes 0-9
mean =0
variance =0
def compute_statistics(data, label, width, height, feature_extractor, percentage=100.0):
    global stats, statsF, mean, variance
    getPrior(label)
    k = 1
    length = len(data)
    perLen = length*percentage/100
    testData = []
    testLabels = []
    for i in range(len(data)):
        if i < perLen:
            testData.append(data[i])
            testLabels.append(label[i])
        else:
            break
    # data set seperated into testData and testLabels
    features = []
    for d in testData:
        features.append(feature_extractor(d, width, height))
    # created features for all of the testData set to variable features
    if len(features[0][0]) == 5 and features[0][0][2] == 2:
        #print("final features SUPREME")
        for stat in range(10): #loops through the stats for every class 0-9
            statFeature=[[0,0],[0,0]]
            instance0 = []
            instance1 = []
            total = 0.0
            for h in range(len(testLabels)):#loops through all the data
                if testLabels[h] == stat: # if this is data is classified as i it is data we are looking for
                    total+=1.0
                    statFeature[0][0] += features[h][0][0]
                    statFeature[1][0] += features[h][0][1]
                    instance0.append(features[h][0][0])
                    instance1.append(features[h][0][1])
            statFeature[0][0] = statFeature[0][0]/total
            statFeature[1][0] = statFeature[1][0] / total
            for i in range(len(instance0)):
                statFeature[0][1] += math.pow((instance0[i] - statFeature[0][0]),2)
                statFeature[1][1] += math.pow((instance1[i] - statFeature[1][0]),2)

            statFeature[0][1] = math.sqrt(statFeature[0][1] / (total - 1))
            statFeature[1][1] = math.sqrt(statFeature[0][1] / (total - 1))

            if statFeature[0][0] == 0:
                statFeature[0][0]= k / (total + (total * k))
            if statFeature[1][0] == 0:
                statFeature[1][0] = k / (total + (total * k))

            #print("Mean1: " + str(statFeature[0][0]) + " variance1: " + str(statFeature[0][1])+" Mean2: " + str(statFeature[1][0]) + " variance2: " + str(statFeature[1][1]))
            statsF[stat] = statFeature
    elif len(features[0]) == 2:
        #print("final features bois")
        for stat in range(10): #loops through the stats for every class 0-9
            statFeature=[]
            list =[[0] * height for i in range(width)]
            statFeature.append(list)
            statFeature.append(list)
            total = 0.0
            for h in range(len(testLabels)):#loops through all the data
                if testLabels[h] == stat: # if this is data is classified as i it is data we are looking for
                    total+=1.0
                    for row in range(len(features[h][0])):# loop through all features of this data h
                        for col in range(len(features[h][0][0])):
                            if features[h][0][row][col] == True:
                                statFeature[0][row][col] += 1.0
                            if features[h][1][row][col] == True:
                                statFeature[1][row][col] += 1.0

            #the statFeature has the amount of times the feature pixel is equal to 1
            #print("Stats: "+str(stat)+" total: "+ str(total))
            for row in range(len(statFeature[0])):
                for col in range(len(statFeature[0][0])):
                    if statFeature[0][row][col] == 0:
                        statFeature[0][row][col] = k / (total+(total*k))
                    else:
                        statFeature[0][row][col] = statFeature[0][row][col]/total
                    if statFeature[1][row][col] == 0:
                        statFeature[1][row][col] = k / (total+(total*k))
                    else:
                        statFeature[1][row][col] = statFeature[1][row][col]/total

            statsF[stat] = statFeature
    elif len(features[0]) == 3:
        #print("advanced feature 1")
        for stat in range(10): #loops through the stats for every class 0-9
            statFeature=[]
            list =[[0] * height for i in range(width)]
            instance = []
            statFeature.append(list)
            statFeature.append(list)
            statFeature.append([0, 0])
            total = 0.0
            for h in range(len(testLabels)):#loops through all the data
                if testLabels[h] == stat: # if this is data is classified as i it is data we are looking for
                    total+=1.0
                    count = 0.0
                    for row in range(len(features[h][0])):# loop through all features of this data h
                        for col in range(len(features[h][0][0])):
                            if features[h][0][row][col] == True:
                                statFeature[0][row][col] += 1.0
                            if features[h][1][row][col] == True:
                                statFeature[1][row][col] += 1.0
                                count+=1.0
                    statFeature[2][0]+=count
                    instance.append(count)

            #the statFeature has the amount of times the feature pixel is equal to 1
            #print("Stats: "+str(stat)+" total: "+ str(total))
            for row in range(len(statFeature[0])):
                for col in range(len(statFeature[0][0])):
                    if statFeature[0][row][col] == 0:
                        statFeature[0][row][col] = k / (total+(total*k))
                    else:
                        statFeature[0][row][col] = statFeature[0][row][col]/total
                    if statFeature[1][row][col] == 0:
                        statFeature[1][row][col] = k / (total+(total*k))
                    else:
                        statFeature[1][row][col] = statFeature[1][row][col]/total

            statFeature[2][0] = statFeature[2][0]/(total) #mean
            for inst in instance:
                statFeature[2][1] += math.pow((inst - statFeature[2][0]), 2)
            statFeature[2][1]= math.sqrt(statFeature[2][1]/((total)-1)) #variance
            #print("Mean: "+ str(statFeature[2][0])+" variance: "+str(statFeature[2][1]))
            statsF[stat] = statFeature
    elif len(features[0]) == 4:
        #print("advanced feature 2")
        for stat in range(10): #loops through the stats for every class 0-9
            statFeature=[]
            list =[[0] * height for i in range(width)]
            instance = []
            statFeature.append(list)
            statFeature.append(list)
            statFeature.append([0, 0])
            statFeature.append(list)
            total = 0.0
            for h in range(len(testLabels)):#loops through all the data
                if testLabels[h] == stat: # if this is data is classified as i it is data we are looking for
                    total+=1.0
                    count = 0.0
                    for row in range(len(features[h][0])):# loop through all features of this data h
                        for col in range(len(features[h][0][0])):
                            if features[h][0][row][col] == True:
                                statFeature[0][row][col] += 1.0
                            if features[h][1][row][col] == True:
                                statFeature[1][row][col] += 1.0
                            if features[h][3][row][col] == True:
                                statFeature[3][row][col] += 1.0
                                count+=1.0
                    statFeature[2][0]+=count
                    instance.append(count)

            #the statFeature has the amount of times the feature pixel is equal to 1
            #print("Stats: "+str(stat)+" total: "+ str(total))
            for row in range(len(statFeature[0])):
                for col in range(len(statFeature[0][0])):
                    if statFeature[0][row][col] == 0:
                        statFeature[0][row][col] = k / (total+(total*k))
                    else:
                        statFeature[0][row][col] = statFeature[0][row][col]/total
                    if statFeature[1][row][col] == 0:
                        statFeature[1][row][col] = k / (total+(total*k))
                    else:
                        statFeature[1][row][col] = statFeature[1][row][col]/total
                    if statFeature[3][row][col] == 0:
                        statFeature[3][row][col] = k / (total+(total*k))
                    else:
                        statFeature[3][row][col] = statFeature[3][row][col]/total

            statFeature[2][0] = statFeature[2][0]/(total) #mean
            for inst in instance:
                statFeature[2][1] += math.pow((inst - statFeature[2][0]), 2)
            statFeature[2][1]= math.sqrt(statFeature[2][1]/((total)-1)) #variance
           #print("Mean: "+ str(statFeature[2][0])+" variance: "+str(statFeature[2][1]))
            statsF[stat] = statFeature
    else:
        #print("its just basic me yo")
        for stat in range(10): #loops through the stats for every class 0-9
            statFeature=[[0] * height for i in range(width)]
            statFeature = setZero(statFeature)
            total = 0.0
            for h in range(len(testLabels)):#loops through all the data
                if testLabels[h] == stat: # if this is data is classified as i it is data we are looking for
                    total+=1.0
                    for row in range(len(features[h])):# loop through all features of this data
                        for col in range(len(features[h][0])):
                            if features[h][row][col] == True:
                                statFeature[row][col] +=1.0

            #the statFeature has the amount of times the feature pixel is equal to 1
            #print("Stats: "+str(stat)+" total: "+ str(total))
            for row in range(len(statFeature)):
                for col in range(len(statFeature[0])):
                    if statFeature[row][col] == 0:
                        statFeature[row][col] = k / (total+(total*k))
                    else:
                        statFeature[row][col] = statFeature[row][col]/total
            #printList(statFeature)
            statsF[stat] = statFeature
    '''
    for num in range(10):
        for rows in range(len(statsF[num])):  # loop through all features of this data
            for cols in range(len(statsF[num][0])):
                stats[num] += np.log(statsF[num][rows][cols])
    print(stats)
    '''

def setZero(array):
    for row in array:
        for col in row:
            col = 0.0
    return array
def printList(array):
    print("ARRAY")
    for row in array:
        for col in row:
            print(str(col)+" "),
        print("\n")
def getPrior(labels):
    global prior
    length = len(labels)
    for i in range(10):
        for h in labels:
            if h == i:
                prior[i] +=1
    for j in range(10):
        prior[j] = prior[j]/length

'''
For the given features for a single digit image, compute the class 
'''
def compute_class(features):
    predicted = -1
    prob = None
    #print("feature length: "+str(len(features[0])))
    if len(features[0]) == 5 and features[0][2] == 2:
        #print("blah")
        for i in range(10):
            newProb = 0.0
            next = ((-.5) * np.log(2 * math.pi)) - (np.log(statsF[i][0][1])) - (
                        (-.5) * math.pow(((features[0][0] - statsF[i][0][0]) / statsF[i][0][1]), 2))
            next1 = ((-.5) * np.log(2 * math.pi)) - (np.log(statsF[i][1][1])) - (
                    (-.5) * math.pow(((features[0][1] - statsF[i][1][0]) / statsF[i][1][1]), 2))
            newProb += np.log(prior[i]) + next +next1
            if newProb > prob or prob == None:
                prob = newProb
                predicted = i
    elif len(features) == 3:
        #print("advanced fool 1")
        for i in range(10):
            newProb = 0.0
            for rows in range(len(features[0])):  # loop through all features of this data
                for cols in range(len(features[0][0])):
                    if features[0][rows][cols] == True:
                        newProb += np.log(statsF[i][1][rows][cols])
                    if features[1][rows][cols] == True:
                        newProb += np.log(statsF[i][1][rows][cols])
            # print("feature 3 "+str(((-.5)*np.log(2*math.pi)))+" - "+str((np.log(statsF[i][2][1])))+" - "+ str(((-.5)*math.pow(((features[2]-statsF[i][2][0])/statsF[i][2][1]),2))))
            # print("feat - mean= "+str((features[2]-statsF[i][2][0]))+" deviation: "+str(statsF[i][2][1])+" mean: "+str(statsF[i][2][0]))
            next = ((-.5) * np.log(2 * math.pi)) - (np.log(statsF[i][2][1])) - ((-.5) * math.pow(((features[2] - statsF[i][2][0]) / statsF[i][2][1]), 2))
            newProb += np.log(prior[i]) + next
            if newProb > prob or prob == None:
                prob = newProb
                predicted = i
    elif len(features) == 2:
        #print("final fool")
        for i in range(10):
            newProb = 0.0
            for rows in range(len(features[0])):  # loop through all features of this data
                for cols in range(len(features[0][0])):
                    if features[0][rows][cols] == True:
                        newProb += np.log(statsF[i][0][rows][cols])
                    if features[1][rows][cols] == True:
                        newProb += np.log(statsF[i][1][rows][cols])
            newProb += np.log(prior[i])
            if newProb > prob or prob == None:
                prob = newProb
                predicted = i
    elif len(features) == 4:
        #print("advanced fool 2")
        for i in range(10):
            newProb = 0.0
            for rows in range(len(features[0])):  # loop through all features of this data
                for cols in range(len(features[0][0])):
                    if features[0][rows][cols] == True:
                        newProb += np.log(statsF[i][0][rows][cols])
                    if features[1][rows][cols] == True:
                        newProb += np.log(statsF[i][1][rows][cols])
                    if features[3][rows][cols] == True:
                        newProb += np.log(statsF[i][3][rows][cols])
            #print("feature 3 "+str(((-.5)*np.log(2*math.pi)))+" - "+str((np.log(statsF[i][2][1])))+" - "+ str(((-.5)*math.pow(((features[2]-statsF[i][2][0])/statsF[i][2][1]),2))))
            #print("feat - mean= "+str((features[2]-statsF[i][2][0]))+" deviation: "+str(statsF[i][2][1])+" mean: "+str(statsF[i][2][0]))
            next = ((-.5)*np.log(2*math.pi))- (np.log(statsF[i][2][1])) - ((-.5)*math.pow(((features[2]-statsF[i][2][0])/statsF[i][2][1]),2))
            newProb+= np.log(prior[i]) + next
            if newProb > prob or prob == None:
                prob = newProb
                predicted = i
    else:
        #print("IM BASIC YO")
        for i in range(10):
            newProb = 0.0
            for rows in range(len(features)):  # loop through all features of this data
                for cols in range(len(features[0])):
                    if features[rows][cols] == True:
                        newProb += np.log(statsF[i][rows][cols])
            newProb+= np.log(prior[i])
            if newProb > prob or prob == None:
                prob = newProb
                predicted = i

    return predicted

'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''
def classify(data, width, height, feature_extractor):
    predicted=[]
    features = []
    for set in data:
        features.append(feature_extractor(set, width, height))
    for feat in features:
        predicted.append(compute_class(feat))

    #print(predicted)
    return predicted







        
    
