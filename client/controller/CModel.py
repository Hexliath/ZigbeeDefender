import pandas as pd
from controller.CDatabase import *
from datetime import datetime
from model.MModel import *
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
from model.MEnum import *
from keras.models import model_from_json
from keras.utils.vis_utils import plot_model
import matplotlib.pyplot as plt


class CModel:
    m = MModel()

    def __init__(self,mode=1,name=None):
        if(mode==1):
            if not name:
                self.m.name = str(datetime.timestamp(datetime.now())).split(".")[0]
            self.feed()
            self.create()
            self.train()
            self.save()
        elif(mode==2):
            self.feed()
            self.load()
        elif(mode==3):
            self.predict_one()
     #   self.test()

    def feed(self):
        db = CDatabase()

        #recover data from database
        train_df  = db.pd_select("(select * from inputs where result=1) union (select * from inputs where result=0)")

        #split the dataset
        self.m.train_df, self.m.test_df = train_test_split(train_df, test_size=0.2)  
        self.m.train_X = self.m.train_df.drop(columns=['result','original'])
        
        self.m.test_X = self.m.test_df.drop(columns=['result','original'])
        self.m.train_Y = self.m.train_df[['result']]

        #transform to categorical (10, 01)
        self.m.train_Y = to_categorical(self.m.train_df.result)
        print(self.m.train_Y)
        print(self.m.train_X)
    
    def predict_one(self):
        db = CDatabase()
        number = input("how many samples to test ? : ")
        train_df  = db.pd_select("(select * from inputs where result=0 ORDER BY ID DESC LIMIT {}) union (select * from inputs where result=1 ORDER BY ID DESC LIMIT {})".format(number,number))
        from sklearn.utils import shuffle
        train_df = shuffle(train_df)
        train_X =  train_df.drop(columns=['result','original'])

        model_name = input("model name : ")
       
        

        # load json and create model
        json_file = open('{}.json'.format(model_name), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("{}.h5".format(model_name))

        test_y_predictions = loaded_model.predict(train_X)
        count = 0
        total = 0
        #print(test_y_predictions.astype('int') )
        for i in range(0,len(test_y_predictions)):
            print("Result : " , train_df['result'].values[i], " -> ", train_df['original'].values[i])
            result_expected = train_df['result'].values[i]
            if test_y_predictions[i].astype('int')[0]:
                result=0
                print("NORMAL")
            else:
                result=1
                print("SUSPICIOUS")

            if result_expected == result:
                count = count +1
            total = total +1
        
        result = count/total
        f=open("results.txt", "a+")
        f.write("{};{}\n".format(number,result))



    def create(self):
        #create model
        model = Sequential()

        #get number of columns in training data
        n_cols = self.m.train_X.shape[1]
        print(n_cols)
                
        #add layers to model
        model.add(Dense(250, activation='relu', input_shape=(n_cols,)))
        model.add(Dense(250, activation='relu'))
        model.add(Dense(250, activation='relu'))
        model.add(Dense(2, activation='softmax'))

        # categoricad_crossentropy:  For a multi-class classification problem
        model.compile( loss = "categorical_crossentropy", 
                    optimizer = "adam", 
                    metrics=['accuracy']
                    )
        self.m.model = model

    def train(self):
        #Stop training when no improvments since 10 epochs
        #early_stopping_monitor = EarlyStopping(patience=10)
        history = self.m.model.fit( self.m.train_X,
                                    self.m.train_Y,
                                    validation_split=0.50,
                                    epochs=30,
                                    batch_size=100,
                                    verbose=1
                                    )
        scores = self.m.model.evaluate(self.m.train_X, self.m.train_Y, verbose=0)
        print("%s: %.2f%%" % (self.m.model.metrics_names[1], scores[1]*100))

        # Plot training & validation accuracy values
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()

        self.test(self.m.model)
                

    def save(self):
        save = False
        ans = input("Do you want to save it ? (y/n)\n ~> ")
        if( ans == "n"):
            return 0
        ans = input("Name of the model ?\n\n ~> ")
        # serialize model to JSON
        model_json = self.m.model.to_json()
        with open("{}.json".format(ans), "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.m.model.save_weights("{}.h5".format(ans))
        print("Saved model to disk")


    def load(self):
        json = input("json filename : ")
        h5 = input("h5 filename : ")

        # load json and create model
        json_file = open('{}.json'.format(json), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights("{}.h5".format(h5))
        print("Loaded model from disk")
      
        # evaluate loaded model on test data
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        score = loaded_model.evaluate(self.m.train_X, self.m.train_Y, verbose=0)
        print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
        self.test(loaded_model)
        print(loaded_model.summary())
        plot_model(loaded_model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
        

    def test(self,model):
        # Test the model against the test sample
        test_y_predictions = model.predict(self.m.test_X)
        #print(test_y_predictions.astype('int') )
        #print(self.m.test_df['result'])
        
        for i in range(0,len(test_y_predictions)):
                    print("Result : " , self.m.train_df['result'].values[i], " -> ", self.m.train_df['original'].values[i])

                    if test_y_predictions[i].astype('int')[0]:
                        print("NORMAL")
                    else:
                        print("SUSPICIOUS")










    




