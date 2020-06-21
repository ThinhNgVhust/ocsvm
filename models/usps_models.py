import os

cwd = os.getcwd()
import sys

sys.path.append(cwd)
print cwd

from  sklearn_OCSVM_model import sklearn_OCSVM_linear, sklearn_OCSVM_rbf
from  OneClass_NN_model import One_Class_NN_explicit_linear, One_Class_NN_explicit_sigmoid
from  sklearn_OCSVM_explicit_model import sklearn_OCSVM_explicit_linear, sklearn_OCSVM_explicit_sigmoid
from tf_OneClass_NN_model import tf_OneClass_NN_linear, tf_OneClass_NN_sigmoid, tf_OneClass_NN_Relu
from  sklearn_OCSVM_rpca import sklearn__RPCA_OCSVM
from sklearn_isolation_forest import sklearn_IsolationForest

dataPath = "/Users/raghav/Documents/Uni/oc-nn/data/"
# Declare a dictionary to store the results

from itertools import izip_longest
decision_scorePath = "/Users/raghav/Documents/Uni/oc-nn/Decision_Scores/usps/"
def write_decisionScores2Csv(path, filename, positiveScores, negativeScores):

    newfilePath = path+filename
    print "Writing file to ", path+filename
    poslist = positiveScores.tolist()
    neglist = negativeScores.tolist()

    # rows = zip(poslist, neglist)
    d = [poslist, neglist]
    export_data = izip_longest(*d, fillvalue='')
    with open(newfilePath, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Normal", "Anomaly"))
        wr.writerows(export_data)
    myfile.close()

    return


df_usps_scores = {}
df_usps_time = {}
import numpy as np


def prepare_usps_mlfetch():
    import tempfile
    import pickle
    # print "importing usps from pickle file ....."

    with open(dataPath + 'usps_data.pkl', "rb") as fp:
        loaded_data1 = pickle.load(fp)

    # test_data_home = tempfile.mkdtemp()
    # from sklearn.datasets.mldata import fetch_mldata
    # usps = fetch_mldata('usps', data_home=test_data_home)
    # print usps.target.shape
    # print type(usps.target)
    labels = loaded_data1['target']
    data = loaded_data1['data']
    # print "******",labels

    k_ones = np.where(labels == 2)
    label_ones = labels[k_ones]
    data_ones = data[k_ones]

    k_sevens = np.where(labels == 8)
    label_sevens = labels[k_sevens]
    data_sevens = data[k_sevens]
    #
    # print "data_sevens:",data_sevens.shape
    # print "label_sevens:",label_sevens.shape
    # print "data_ones:",data_ones.shape
    # print "label_ones:",label_ones.shape
    #
    data_ones = data_ones[:220]
    label_ones = label_ones[:220]
    data_sevens = data_sevens[:11]
    label_sevens = label_sevens[:11]

    data = np.concatenate((data_ones, data_sevens), axis=0)
    label = np.concatenate((label_ones, label_sevens), axis=0)
    label[0:220] = 1
    label[220:231] = -1
    # print "1-s",data[0]
    # print label
    # print "7-s",data[230]
    # print label
    # print "data:",data.shape
    # print "label:",label.shape

    # import matplotlib.pyplot as plt
    # plt.hist(label,bins=5)
    # plt.title("Count of  USPS Normal(1's) and Anomalous datapoints(7's) in training set")
    # plt.show()

    return [data, label]


nu = 0.04


def func_getDecision_Scores_usps(dataset, data_train, data_test, data_train_ae2, data_test_ae2, data_train_cae,
                                 data_test_cae):
    # sklearn_OCSVM
    result = sklearn_OCSVM_linear(data_train, data_test, nu)
    df_usps_scores["sklearn-OCSVM-Linear-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-Linear-Test"] = result[1]

    df_usps_time["sklearn-OCSVM-Linear-Train"] = result[2]
    df_usps_time["sklearn-OCSVM-Linear-Test"] = result[3]

    result = sklearn_OCSVM_rbf(data_train, data_test, nu)
    df_usps_scores["sklearn-OCSVM-RBF-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-RBF-Test"] = result[1]

    df_usps_time["sklearn-OCSVM-RBF-Train"] = result[2]
    df_usps_time["sklearn-OCSVM-RBF-Test"] = result[3]
    print ("Finished sklearn_OCSVM_linear")

    result = tf_OneClass_NN_linear(data_train, data_test)
    df_usps_scores["tf_OneClass_NN-Linear-Train"] = result[0]
    df_usps_scores["tf_OneClass_NN-Linear-Test"] = result[1]

    df_usps_time["tf_OneClass_NN-Linear-Train"] = result[2]
    df_usps_time["tf_OneClass_NN-Linear-Test"] = result[3]

    print ("Finished tf_OneClass_NN_linear")

    result = tf_OneClass_NN_sigmoid(data_train, data_test)
    df_usps_scores["tf_OneClass_NN-Sigmoid-Train"] = result[0]
    df_usps_scores["tf_OneClass_NN-Sigmoid-Test"] = result[1]

    df_usps_time["tf_OneClass_NN-Sigmoid-Train"] = result[2]
    df_usps_time["tf_OneClass_NN-Sigmoid-Test"] = result[3]

    print ("Finished tf_OneClass_NN_sigmoid")

    result = tf_OneClass_NN_Relu(data_train, data_test)
    df_usps_scores["tf_OneClass_NN-Relu-Train"] = result[0]
    df_usps_scores["tf_OneClass_NN-Relu-Test"] = result[1]

    print ("Finished tf_OneClass_NN_sigmoid")

    result = sklearn__RPCA_OCSVM(data_train, data_test, nu)
    df_usps_scores["rpca_ocsvm-Train"] = result[0]
    df_usps_scores["rpca_ocsvm-Test"] = result[1]

    df_usps_time["rpca_ocsvm-Train"] = result[2]
    df_usps_time["rpca_ocsvm-Test"] = result[3]

    print ("Finished rpca_ocsvm")

    result = sklearn_IsolationForest(data_train, data_test)
    df_usps_scores["isolation-forest-Train"] = result[0]
    df_usps_scores["isolation-forest-Test"] = result[1]

    df_usps_time["isolation-forest-Train"] = result[2]
    df_usps_time["isolation-forest-Test"] = result[3]

    print ("Finished isolation-forest")

    result = AE2_SVDD_Linear(data_train_ae2, data_test_ae2, nu)
    df_usps_scores["ae_svdd-linear-Train"] = result[0]
    df_usps_scores["ae_svdd-linear-Test"] = result[1]

    df_usps_time["ae_svdd-linear-Train"] = result[2]
    df_usps_time["ae_svdd-linear-Test"] = result[3]
    print ("Finished ae_ocsvm-linear")

    result = AE2_SVDD_RBF(data_train_ae2, data_test_ae2, nu)
    df_usps_scores["ae_svdd-rbf-Train"] = result[0]
    df_usps_scores["ae_svdd-rbf-Test"] = result[1]

    df_usps_time["ae_svdd-rbf-Train"] = result[2]
    df_usps_time["ae_svdd-rbf-Test"] = result[3]

    print ("Finished ae_ocsvm-sigmoid")

    result = CAE_OCSVM_Linear(data_train_cae, data_test_cae, nu)
    df_usps_scores["cae_ocsvm-linear-Train"] = result[0]
    df_usps_scores["cae_ocsvm-linear-Test"] = result[1]

    df_usps_time["cae_ocsvm-linear-Train"] = result[2]
    df_usps_time["cae_ocsvm-linear-Test"] = result[3]

    print ("Finished cae_ocsvm-linear")

    result = CAE_OCSVM_RBF(data_train_cae, data_test_cae, nu)
    df_usps_scores["cae_ocsvm-rbf-Train"] = result[0]
    df_usps_scores["cae_ocsvm-rbf-Test"] = result[1]

    df_usps_time["cae_ocsvm-rbf-Train"] = result[2]
    df_usps_time["cae_ocsvm-rbf-Test"] = result[3]

    print ("Finished cae_ocsvm-rbf")

    # Write a CSV file for Cifar-10 data consisting of Methods, Train and test time
    # Method, Train, Test
    methods = ['OC-NN-Linear', 'OC-NN-Sigmoid', 'CAE-OCSVM-Linear', 'CAE-OCSVM-RBF', 'AE2-SVDD-Linear',
               'AE2-SVDD-RBF', 'OCSVM-Linear', 'OCSVM-RBF', 'RPCA_OCSVM', 'Isolation_Forest']
    write_training_test_results(df_usps_time, methods)

    return df_usps_scores


import csv

def write_training_test_results(df_time, methods):
    download_dir = "/Users/raghav/Documents/Uni/oc-nn/trainTest_Time/usps_trainTest.csv"  # where you want the file to be downloaded to
    print "Writing file to ", download_dir
    csv = open(download_dir, "a")
    for method in methods:
        if (method == "OC-NN-Linear"):
            row = method + "," + str(df_time["tf_OneClass_NN-Linear-Train"]) + "," + str(
                df_time["tf_OneClass_NN-Linear-Test"]) + "\n"
            csv.write(row)
        if (method == "OC-NN-Sigmoid"):
            row = method + "," + str(df_time["tf_OneClass_NN-Sigmoid-Train"]) + "," + str(
                df_time["tf_OneClass_NN-Sigmoid-Test"]) + "\n"
            csv.write(row)

        if (method == "CAE-OCSVM-Linear"):
            row = method + "," + str(df_time["cae_ocsvm-linear-Train"]) + "," + str(
                df_time["cae_ocsvm-linear-Test"]) + "\n"
            csv.write(row)

        if (method == "CAE-OCSVM-RBF"):
            row = method + "," + str(df_time["cae_ocsvm-rbf-Train"]) + "," + str(df_time["cae_ocsvm-rbf-Test"]) + "\n"
            csv.write(row)

        if (method == "AE2-SVDD-Linear"):
            row = method + "," + str(df_time["ae_svdd-linear-Train"]) + "," + str(df_time["ae_svdd-linear-Test"]) + "\n"
            csv.write(row)

        if (method == "AE2-SVDD-RBF"):
            row = method + "," + str(df_time["ae_svdd-rbf-Train"]) + "," + str(df_time["ae_svdd-rbf-Test"]) + "\n"
            csv.write(row)

        if (method == "OCSVM-Linear"):
            row = method + "," + str(df_time["sklearn-OCSVM-Linear-Train"]) + "," + str(
                df_time["sklearn-OCSVM-Linear-Test"]) + "\n"
            csv.write(row)

        if (method == "OCSVM-RBF"):
            row = method + "," + str(df_time["sklearn-OCSVM-RBF-Train"]) + "," + str(
                df_time["sklearn-OCSVM-RBF-Test"]) + "\n"
            csv.write(row)

        if (method == "RPCA_OCSVM"):
            row = method + "," + str(df_time["rpca_ocsvm-Train"]) + "," + str(df_time["rpca_ocsvm-Test"]) + "\n"
            csv.write(row)

        if (method == "Isolation_Forest"):
            row = method + "," + str(df_time["isolation-forest-Train"]) + "," + str(
                df_time["isolation-forest-Test"]) + "\n"
            csv.write(row)

    return

import time

def AE2_SVDD_RBF(data_train, data_test, nu):
    print("[INFO] preparing the network to extract flattened inputs(X,X_test) for scoring..... done!!!")
    import matplotlib.pyplot as plt
    from sklearn import svm
    ocSVM = svm.OneClassSVM(nu=nu, kernel='rbf')
    start_time = time.time()
    ocSVM.fit(data_train)
    trainTime = time.time() - start_time
    activations = ["linear", "rbf"]
    start_time = time.time()
    pos_decisionScore = ocSVM.decision_function(data_train)
    neg_decisionScore = ocSVM.decision_function(data_test)
    testTime = time.time() - start_time
    print pos_decisionScore
    print neg_decisionScore

    print "AE2_SVDD_rbf+", pos_decisionScore
    print "AE2_SVDD_rbf-", neg_decisionScore

    return [pos_decisionScore, neg_decisionScore,trainTime,testTime]


def AE2_SVDD_Linear(data_train, data_test, nu):
    print("[INFO] preparing the network to extract flattened inputs(X,X_test) for scoring..... done!!!")
    import matplotlib.pyplot as plt
    from sklearn import svm
    ocSVM = svm.OneClassSVM(nu=nu, kernel='linear')
    start_time = time.time()
    ocSVM.fit(data_train)
    trainTime = time.time() - start_time
    activations = ["linear", "rbf"]

    start_time = time.time()
    pos_decisionScore = ocSVM.decision_function(data_train)
    neg_decisionScore = ocSVM.decision_function(data_test)
    testTime = time.time() - start_time
    print pos_decisionScore
    print neg_decisionScore

    print "AE2_SVDD_rbf+", pos_decisionScore
    print "AE2_SVDD_rbf-", neg_decisionScore

    return [pos_decisionScore, neg_decisionScore,trainTime,testTime]


def CAE_OCSVM_RBF(data_train, data_test, nu):
    print("[INFO] preparing the network to extract flattened inputs(X,X_test) for scoring..... done!!!")
    import matplotlib.pyplot as plt
    from sklearn import svm
    ocSVM = svm.OneClassSVM(nu=nu, kernel='rbf')
    start_time = time.time()
    ocSVM.fit(data_train)

    trainTime = time.time() - start_time
    activations = ["linear", "rbf"]
    start_time = time.time()
    pos_decisionScore = ocSVM.decision_function(data_train)
    neg_decisionScore = ocSVM.decision_function(data_test)
    testTime = time.time() - start_time
    print pos_decisionScore
    print neg_decisionScore

    print "CAE_OCSVM_RBF+", pos_decisionScore
    print "CAE_OCSVM_RBF-", neg_decisionScore
    write_decisionScores2Csv(decision_scorePath, "CAE_OCSVM_RBF.csv", pos_decisionScore, neg_decisionScore)

    return [pos_decisionScore, neg_decisionScore,trainTime,testTime]


def CAE_OCSVM_Linear(data_train, data_test, nu):
    print("[INFO] preparing the network to extract flattened inputs(X,X_test) for scoring..... done!!!")
    import matplotlib.pyplot as plt
    from sklearn import svm
    ocSVM = svm.OneClassSVM(nu=nu, kernel='linear')
    start_time = time.time()
    ocSVM.fit(data_train)
    trainTime = time.time() - start_time
    activations = ["linear", "rbf"]
    start_time = time.time()
    pos_decisionScore = ocSVM.decision_function(data_train)
    neg_decisionScore = ocSVM.decision_function(data_test)
    testTime = time.time() - start_time
    print pos_decisionScore
    print neg_decisionScore

    print "CAE_OCSVM_Linear+", pos_decisionScore
    print "CAE_OCSVM_Linear-", neg_decisionScore
    write_decisionScores2Csv(decision_scorePath, "CAE_OCSVM_Linear.csv", pos_decisionScore, neg_decisionScore)

    return [pos_decisionScore, neg_decisionScore,trainTime,testTime]


def usps_autoencoder_representation(data_train, data_test):
    from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
    from keras.models import Model
    from keras import backend as K
    import matplotlib.pyplot as plt
    import numpy  as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as srn
    import sys
    import os
    cwd = "/Users/raghav/Documents/Uni/oc-nn/"
    import sys
    sys.path.append(cwd + "/data_load/")
    sys.path.append(cwd + "/models/")

    ## Import all the datasets and prepare the Training and test set for respective datasets


    ### Prepare training and test set for respective datasets


    input_img = Input(shape=(16, 16, 1))  # adapt this if using `channels_first` image data format

    x = Conv2D(8, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(4, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(2, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)
    encoder = Model(input_img, x)
    # at this point the representation is (4, 4, 8) i.e. 128-dimensional

    x = Conv2D(2, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(4, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    # x = Conv2D(16, (3, 3), activation='relu')(x)
    # x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')

    print autoencoder.summary()

    from keras.datasets import mnist
    import numpy as np

    # (x_train, x_trainLabels), (x_test, x_testLabels) = mnist.load_data()
    # x_train = data_train_usps
    # x_test = data_test_usps
    # print x_train.shape



    x_train = data_train
    x_test = data_test

    # print labels
    # print targets_test_usps
    # print x_train.shape
    # print x_test.shape

    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = np.reshape(x_train, (len(x_train), 16, 16, 1))  # adapt this if using `channels_first` image data format
    x_test = np.reshape(x_test, (len(x_test), 16, 16, 1))  # adapt this if using `channels_first` image data format

    from keras.callbacks import TensorBoard

    autoencoder.fit(x_train, x_train,
                    epochs=100,
                    batch_size=50,
                    shuffle=True,
                    validation_data=(x_test, x_test),
                    callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])

    decoded_imgs = autoencoder.predict(x_test)

    train_encoded_imgs = encoder.predict(x_train)
    test_encoded_imgs = encoder.predict(x_test)
    train_encoded_imgs = np.reshape(train_encoded_imgs, (len(train_encoded_imgs), 128))
    test_encoded_imgs = np.reshape(test_encoded_imgs, (len(test_encoded_imgs), 128))
    print "Training Encoded Representations....", train_encoded_imgs.shape
    print "Testing Encoded Representations....", test_encoded_imgs.shape

    return [train_encoded_imgs, test_encoded_imgs]


def func_getDecision_Scores_usps_old(dataset, data_train, data_test):
    # if(autoencoder == "yes"):
    # 	[data_train,data_test] = usps_autoencoder_representation(data_train, data_test)

    # sklearn_OCSVM
    result = sklearn_OCSVM_linear(data_train, data_test)
    df_usps_scores["sklearn-OCSVM-Linear-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-Linear-Test"] = result[1]

    result = sklearn_OCSVM_rbf(data_train, data_test)
    df_usps_scores["sklearn-OCSVM-RBF-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-RBF-Test"] = result[1]
    print ("Finished sklearn_OCSVM_linear")

    # sklearn _OCSVM_explicit
    result = sklearn_OCSVM_explicit_linear(data_train, data_test)
    df_usps_scores["sklearn-OCSVM-explicit-Linear-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-explicit-Linear-Test"] = result[1]

    result = sklearn_OCSVM_explicit_sigmoid(data_train, data_test)
    df_usps_scores["sklearn-OCSVM-explicit-Sigmoid-Train"] = result[0]
    df_usps_scores["sklearn-OCSVM-explicit-Sigmoid-Test"] = result[1]

    print ("Finished sklearn _OCSVM_explicit")

    # One Class NN Explicit
    result = One_Class_NN_explicit_linear(data_train, data_test)
    df_usps_scores["One_Class_NN_explicit-Linear-Train"] = result[0]
    df_usps_scores["One_Class_NN_explicit-Linear-Test"] = result[1]

    result = One_Class_NN_explicit_sigmoid(data_train, data_test)
    df_usps_scores["One_Class_NN_explicit-Sigmoid-Train"] = result[0]
    df_usps_scores["One_Class_NN_explicit-Sigmoid-Test"] = result[1]

    print ("Finished One Class NN Explicit")

    result = tf_OneClass_NN_linear(data_train, data_test)
    df_usps_scores["tf_OneClass_NN-Linear-Train"] = result[0]
    df_usps_scores["tf_OneClass_NN-Linear-Test"] = result[1]
    print ("Finished tf_OneClass_NN_linear")

    result = tf_OneClass_NN_sigmoid(data_train, data_test)
    df_usps_scores["tf_OneClass_NN-Sigmoid-Train"] = result[0]
    df_usps_scores["tf_OneClass_NN-Sigmoid-Test"] = result[1]

    print ("Finished tf_OneClass_NN_sigmoid")

    # Y = labels_train
    # Y = Y.tolist()
    # labels_train = [[i] for i in Y]
    # result = tflearn_OneClass_NN_linear(data_train,data_test,labels_train)
    # df_usps_scores["tflearn_OneClass_NN-Linear-Train"] = result[0]
    # df_usps_scores["tflearn_OneClass_NN-Linear-Test"] =  result[1]
    #
    # result = tflearn_OneClass_NN_Sigmoid(data_train,data_test,labels_train)
    # df_usps_scores["tflearn_OneClass_NN-Sigmoid-Train"] = result[0]
    # df_usps_scores["tflearn_OneClass_NN-Sigmoid-Test"] = result[1]
    # print ("Finished tflearn_OneClass")

    # print (type(df_usps_scores))
    # print ( (df_usps_scores.keys()))

    return df_usps_scores
