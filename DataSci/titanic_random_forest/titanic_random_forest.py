from sklearn.ensemble import RandomForestClassifier 
import csv as csv 
import numpy as np

train_data_columns = (0, 1, 3, 4, 5, 6, 8, 10)
test_data_columns = (0, 2, 3, 4, 5, 7, 9)

def main():
    train_data_raw = data_input('train.csv')
    train_data = data_process(train_data_raw, train_data_columns)
    test_data_raw = data_input('test.csv')
    test_data = data_process(test_data_raw, test_data_columns)
    model_output = random_forest_fit(train_data, test_data)
    create_file(model_output)

#convert data into numpy array stored in memory
def data_input(data_file):
    data_object = csv.reader(open(data_file, 'rb'))
    header = data_object.next()
    data = []
    for row in data_object:
        data.append(row)
    data = np.array(data)
    return data

#process data for compatibility with random forest algorithm
def data_process(data_array, included_columns):
    data = data_array[0::, included_columns]
    data[data=='male'] = '1'
    data[data=='female'] = '0'
    data[data=='C'] = '0'
    data[data=='S'] = '1'
    data[data=='Q'] = '2'
    data[data==''] = '0'
    data = data.astype(float)
    return data
  
#fit a random forest to the training data, apply to test data
def random_forest_fit(train, test):
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(train[0::,1::],train[0::,0])
    output = forest.predict(test)
    return output


#create the prediction file
def create_file(result):
    result = result.tolist()
    fname = "randomforestbasedmodelpy.csv"
    f = open(fname, "wb")
    open_file_object = csv.writer(f)
    for row in result:
        open_file_object.writerow([row])
        print row
    f.close()

if __name__ == "__main__":
    main()
