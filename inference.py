import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

class DHMLM:
    def __init__(self):
        self.l1 = keras.models.load_model('models/layer1.h5')
        self.l2 = keras.models.load_model('models/layer2.h5')
        self.l3 = keras.models.load_model('models/layer3.h5')
        self.n1 = []
        self.n2 = []
        self.n3 = []
        self.final_n = []

    def first_layer_inference(self, data,flag=0):
        pred1 = self.l1.predict(data)
        for i in range(len(pred1)):
            if pred1[i] >= 0.5:
                self.n1.append(1)
            else:
                self.n1.append(0)
        attack_indices = tf.where(tf.equal(tf.convert_to_tensor(self.n1), 1))
        rows = tf.gather(data, attack_indices[:, 0])

        if flag==1:
            return self.n1
        else:
            return rows

    def second_layer_inference(self, data,flag=0):
        pred2 = self.l2.predict(data)
        for i in pred2:
            i=list(i)
            maxvalue=max(i)
            self.n2.append(i.index(maxvalue))
        attack_indices = tf.where(tf.equal(tf.convert_to_tensor(self.n2), 0))
        rows = tf.gather(data, attack_indices[:, 0])

        if flag==1:
            return self.n2
        else:
            return rows

    def third_layer_inference(self, data,flag=0):
        pred3 = self.l3.predict(data)
        for i in pred3:
            i=list(i)
            maxvalue=max(i)
            self.n3.append(i.index(maxvalue))
        
        if flag==1:
           return self.n3
      

    def full_model_inference(self, data):
        rows = self.first_layer_inference(data)
        rows = self.second_layer_inference(rows)
        self.third_layer_inference(rows)

        for i in range(len(self.n1)):
            if self.n1[i] == 0:
                self.final_n.append(self.n1[i])

        for i in range(len(self.n2)):
            if self.n2[i] == 1:
                self.final_n.append(10)
            if self.n2[i] == 2:
                self.final_n.append(11)
            if self.n2[i] == 3:
                self.final_n.append(12)

        for i in range(len(self.n3)):
            self.final_n.append(self.n3[i]+1)

        return self.final_n

def main():

    model = DHMLM()
    choice = sys.argv[1]
    data_path = sys.argv[2]
    output_path = sys.argv[3]


    df = pd.read_csv(data_path)
    df = df[[' Source Port', ' Destination Port', ' Protocol', ' Flow Duration',
       ' Total Fwd Packets', ' Total Backward Packets',
       'Total Length of Fwd Packets', ' Fwd Packet Length Min',
       'Bwd Packet Length Max', ' Flow IAT Mean', ' Flow IAT Std',
       ' Flow IAT Min', 'Fwd IAT Total', ' Fwd IAT Mean', ' Fwd IAT Min',
       ' Fwd Header Length', ' Bwd Header Length', ' Bwd Packets/s',
       ' Init_Win_bytes_backward', ' NFlow Packets/s']]

    df = tf.convert_to_tensor(df)

    if choice == '-l1':
        output = model.first_layer_inference(df,flag=1)
    elif choice == '-l2':
        output = model.second_layer_inference(df,flag=1)
    elif choice == '-l3':
        output = model.third_layer_inference(df,flag=1)
    elif choice == '-fm':
        output = model.full_model_inference(df)

    output = np.array(output)

    np.savetxt(output_path,output)

if __name__ == '__main__':
    main()