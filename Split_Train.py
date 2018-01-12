import sys
import numpy as np
import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adadelta, adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, Callback

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import average_precision_score

top_M = 500

class History(Callback):
    def on_train_begin(self,logs={}):
        self.tr_losses=[]
        self.val_losses=[]
        self.tr_accs=[]
        self.val_accs=[]
    def on_epoch_end(self,epoch,logs={}):
        self.tr_losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.tr_accs.append(logs.get('acc'))
        self.val_accs.append(logs.get('val_acc'))

def dump_history(store_path,logs):
    with open(os.path.join(store_path,'train_loss'),'a')as f:
        for loss in logs.tr_losses: f.write('{}\n'.format(loss))
    with open(os.path.join(store_path,'train_accuracy'),'a')as f:
        for acc in logs.tr_accs: f.write('{}\n'.format(acc))
    with open(os.path.join(store_path,'valid_loss'),'a')as f:
        for loss in logs.val_losses: f.write('{}\n'.format(loss))
    with open(os.path.join(store_path,'valid_accuracy'),'a')as f:
        for acc in logs.val_accs: f.write('{}\n'.format(acc));


def read_train(fileName):

    X_train = np.delete(np.genfromtxt(fileName, delimiter=','), [0], 0)
    Y_train = np.transpose([X_train[:,24]]);
    X_train = X_train[:,0:24];
    return X_train, Y_train

def read_test(fileName):

    X_test = np.delete(np.genfromtxt(fileName, delimiter=','), [0], 0)
    X_test = X_test[:,0:24];
    return X_test

def sigmoid(z):
      return 1/(1+np.exp(-z));

def preprocessing(fileName, oneHot, ifTrain):

    if(ifTrain): X_raw, Y = read_train(fileName)
    else: X_raw = read_test(fileName)

    if oneHot == 1:
        sex = np_utils.to_categorical(X_raw[:,2],3); sex = sex[:,1:]
        edu = np_utils.to_categorical(X_raw[:,3],7); edu[:,4] = edu[:,0]+edu[:,4]+edu[:,5]+edu[:,6]; edu = edu[:,1:5] 
        martial = np_utils.to_categorical(X_raw[:,4],4); temp = np.copy(martial[:,0]); martial[:,0:3] = martial[:,1:]; martial[:,3] = temp
        prev_1 = np_utils.to_categorical(X_raw[:,6],12);
        prev_2 = np_utils.to_categorical(X_raw[:,7],12);
        prev_3 = np_utils.to_categorical(X_raw[:,8],12);
        prev_4 = np_utils.to_categorical(X_raw[:,9],12);
        prev_5 = np_utils.to_categorical(X_raw[:,10],12);
        prev_6 = np_utils.to_categorical(X_raw[:,11],12);

        XDD = X_raw[:,12:]/np.transpose([X_raw[:,1]])
        X = np.concatenate((np.transpose([X_raw[:,1]]), sex, edu, martial, np.transpose([X_raw[:,5]]), 
            prev_1, prev_2, prev_3, prev_4, prev_5, prev_6, XDD), axis=1)
            #X_raw[:,12:]),axis=1)
        #X = np.concatenate((np.transpose([X_raw[:,1]]), sex, edu, martial, np.transpose([X_raw[:,5]]), 
        #    prev_1, prev_2, prev_3, prev_4, np.transpose([X_raw[:,12]/X_raw[:,1]]), np.transpose([(X_raw[:,13]-X_raw[:,18])/X_raw[:,1]]),
        #    np.transpose([(X_raw[:,14]-X_raw[:,19])/X_raw[:,1]]), np.transpose([(X_raw[:,15]-X_raw[:,20])/X_raw[:,1]]), 
        #    np.transpose([(X_raw[:,16]-X_raw[:,21])/X_raw[:,1]]), np.transpose([(X_raw[:,17]-X_raw[:,22])/X_raw[:,1]])),axis=1)
        #X = np.concatenate((sex, edu, martial, prev_1, prev_2, prev_3, prev_4, prev_5, prev_6), axis=1)

    else:
        X = X_raw

    if(ifTrain): 
        val_split = 20000
        X_val = X[val_split:,:]; X_train = X[:val_split,:]
        Y_val = Y[val_split:,:]; Y_train = Y[:val_split,:]
        return X_train, X_val, Y_train, Y_val

    else:
        return X

def computeMean_Var(X):
    length = (np.shape(X)[1]);
    table = np.zeros((2,length));
    for i in range(length):
        if(i==0 or i==11 or i>=84):
            table[0][i] = np.mean(X[:,i]); table[1][i] = np.std(X[:,i]);
    return table;

def normalize(lX,table):
    length = np.shape(table)[1];
    for i in range(length):
        if(table[1,i] > 0): lX[:,i] = (lX[:,i]-table[0,i])/table[1,i];

def shuffle(X, Y):
    randomize = np.arange(len(X))
    np.random.shuffle(randomize)
    return (X[randomize], Y[randomize])

def logistic(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):

    W = np.zeros((96+1, 1))
    #table = computeMean_Var(np.concatenate((X_train, X_test), axis=0))
    table = computeMean_Var(X_train) 

    normalize(X_train, table); normalize(X_test_public, table)
    X_train = np.insert(X_train, 0, 1, axis=1)
    X_test = np.insert(X_test, 0, 1, axis=1)

    eta = 0.05; epoch = 0;
    totalgra = 0; conti = 0; prevcost = 9999;
    batch_size = 4000;
    batch_num = int(np.floor(X_train.shape[0]/batch_size));

    while(epoch<2000):
        X_train, Y_train = shuffle(X_train, Y_train)
        for idx in range(batch_num): 
            gradient = -np.transpose([np.mean((Y_train[idx*batch_size:(idx+1)*batch_size,:]-sigmoid(np.dot(X_train[idx*batch_size:(idx+1)*batch_size,:],W)))*X_train[idx*batch_size:(idx+1)*batch_size,:],axis=0)]);

            #gradient = -np.transpose([np.mean((Y_train-sigmoid(np.dot(X_train,W)))*X_train,axis=0)])

            if(epoch!=0): W = W - eta*gradient/np.sqrt(totalgra)
            else: W = W - eta*gradient
            totalgra += np.power(gradient + 0.0001*np.ones((97, 1)),2)

        y = (sigmoid(np.dot(X_train,W)) > 0.5); y = y.astype(int)
        cost = np.mean(np.abs(Y_train-y)); print(cost)

        if(cost >= prevcost): conti += 1;
        else: conti = 0;
        prevcost = cost;
        epoch += 1;
        if (conti > 10): break;

    #output = (sigmoid(np.dot(X_test_public,W)) > 0.5); output = output.astype(int)
    #print (output)
    #check_answer(output, 'Test_2_ans.csv')

def check_answer(output, fileName):
    data = np.delete(np.genfromtxt(fileName, delimiter=','), [0], 0)
    Y_test = np.transpose([data[:,1]])
    print(np.mean(output == Y_test))

    #print(np.mean((output != Y_test) * (output == 1)), np.mean((output != Y_test) * (output == 0)))
   
def MAP_eval(output, fileName, M):
    data = np.delete(np.genfromtxt(fileName, delimiter=','), [0], 0)
    Y_yes = np.transpose([data])
    #Y_yes = (np.where(Y_test == 1))
    #Y_yes = np.transpose([Y_yes[0]+1])

    correct_ans = 0.0; answer = 0.0
    for i in range(M):
        if output[i, 0] in Y_yes: 
            correct_ans += 1.0
        answer += (correct_ans/(i+1))
    print ("Average Precision: " + str(answer/M))
    #print ("Average Precision: " + str(average_precision_score(Y_test[:M,:], output[:M,1])))

def predict(output, name):
    print ("Output predict.csv!")
    np.savetxt(name, output[:, 0], fmt=['%d'], delimiter=",")

def random_forest(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):

    table = computeMean_Var(X_train) 
    normalize(X_train, table); normalize(X_test_public, table); normalize(X_test_private, table)

    print (np.shape(X_train))
    parameter_gridsearch = {
        'max_depth' : [5, 10, 15],  #depth of each decision tree
        'n_estimators': [250, 300, 400, 500],  #count of decision tree
        #'max_features': ['sqrt', 'log2'], 
        'min_samples_split': [2],
        #'min_samples_leaf': [1, 3, 4],
        #'bootstrap': [True, False],
    }

    randomforest = RandomForestClassifier()
    crossvalidation = StratifiedKFold(n_splits=5)

    gridsearch = GridSearchCV(randomforest,             #grid search for algorithm optimization
                             scoring='average_precision',#'accuracy',
                             param_grid=parameter_gridsearch,
                              cv=crossvalidation)

    gridsearch.fit(X_train, Y_train[:,0]) 
    model = gridsearch
    parameters = gridsearch.best_params_
    print(parameters)

    print(1-np.mean(Y_train[:,0]),'Best Score: {}'.format(gridsearch.best_score_))
    #output = gridsearch.predict(X_test_public); output = np.transpose([output])
    #check_answer(output, 'Test_2_ans.csv')

    prob_output = gridsearch.predict_proba(X_test_public)
    prob_output[:, 0] = np.arange(1,5001)
    prob_output = prob_output[(-prob_output[:, 1]).argsort()]
    MAP_eval(prob_output, 'Test_Ans_Public.csv', top_M)
    predict(prob_output, 'public.csv') # Output the public.csv

    prob_output = gridsearch.predict_proba(X_test_private)
    prob_output[:, 0] = np.arange(5001,10001)
    prob_output = prob_output[(-prob_output[:, 1]).argsort()]
    MAP_eval(prob_output, 'Test_Ans_Private.csv', top_M)
    predict(prob_output, 'private.csv') # Output the private.csv

    output = gridsearch.predict(X_train)
    print (1-np.mean(Y_train[:,0]),np.mean(output==Y_train[:,0]))
    
    #print(np.mean((output != Y_train[:,0]) * (output == 1)), np.mean((output != Y_train[:,0]) * (output == 0) * (X_train[:,12] == 1)))

def adaptive_boosting(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):

    table = computeMean_Var(X_train) 
    normalize(X_train, table); normalize(X_test_public, table)

    parameter_gridsearch = {
        'n_estimators': [300],  #count of decision tree
        #'base_estimator': [], #[DecisionTreeClassifier(max_depth=1,min_samples_leaf=1)],
        #'algorithm': ['SAMME'],
    }

    adaboost = AdaBoostClassifier()
    crossvalidation = StratifiedKFold(n_splits=5)

    gridsearch = GridSearchCV(adaboost,             #grid search for algorithm optimization
                              scoring='accuracy',
                              param_grid=parameter_gridsearch,
                              cv=crossvalidation)

    gridsearch.fit(X_train, Y_train[:,0]) 
    model = gridsearch
    parameters = gridsearch.best_params_
    print(parameters)

    print(1-np.mean(Y_train[:,0]),'Best Score: {}'.format(gridsearch.best_score_))
    
    output = gridsearch.predict(X_test_public); output = np.transpose([output]);
    #check_answer(output, 'Test_2_ans.csv')

    output = gridsearch.predict(X_train)
    print (1-np.mean(Y_train[:,0]),np.mean(output==Y_train[:,0]))

    #print(np.mean((output != Y_train[:,0]) * (output == 1)), np.mean((output != Y_train[:,0]) * (output == 0) * (X_train[:,12] == 1)))

def KNN(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):

    table = computeMean_Var(X_train) 
    normalize(X_train, table); normalize(X_test_public, table)
    
    parameter_gridsearch = {
        'n_neighbors':[12, 25, 37],
    }

    neigh = KNeighborsClassifier()
    crossvalidation = StratifiedKFold(n_splits=5)

    gridsearch = GridSearchCV(neigh,
                              scoring='accuracy',
                              param_grid=parameter_gridsearch,
                              cv=crossvalidation)
    gridsearch.fit(X_train, Y_train[:,0])
    parameters = gridsearch.best_params_
    print(parameters)
 
    print(1-np.mean(Y_train[:,0]),'Best Score: {}'.format(gridsearch.best_score_))
    
    output = gridsearch.predict(X_test_public);  output = np.transpose([output]);
    #check_answer(output, 'Test_2_ans.csv')

    output = gridsearch.predict(X_train)
    print (1-np.mean(Y_train[:,0]), np.mean(output==Y_train[:,0]))

    print(np.mean((output != Y_train[:,0]) * (output == 1)), np.mean((output != Y_train[:,0]) * (output == 0) * (X_train[:,12] == 1)))

def sklearn_logistic(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):

    table = computeMean_Var(X_train) 
    normalize(X_train, table); normalize(X_test_public, table)

    parameter_gridsearch = {
        'C':[1.5, 2.0, 2.5],
        'max_iter':[100, 200, 300],
        #'class_weight':['balanced'],
    }

    logic = LogisticRegression()
    crossvalidation = StratifiedKFold(n_splits=5)

    gridsearch = GridSearchCV(logic,
                              scoring='average_precision',#'accuracy',
                              param_grid=parameter_gridsearch,
                              cv=crossvalidation)
    gridsearch.fit(X_train, Y_train[:,0])
    parameters = gridsearch.best_params_
    print(parameters)

    print(gridsearch.best_estimator_.coef_)

    #print(1-np.mean(Y_train[:,0]),'Best Score: {}'.format(gridsearch.best_score_))
    
    output = gridsearch.predict(X_test_public); output = np.transpose([output]);
    #check_answer(output, 'Test_2_ans.csv')

    prob_output = gridsearch.predict_proba(X_test_public)
    #MAP_eval(prob_output, 'Test_2_ans.csv', top_M)

    output = gridsearch.predict(X_train)
    print (1-np.mean(Y_train[:,0]), np.mean(output==Y_train[:,0]))

    #print(np.mean((output != Y_train[:,0]) * (output == 1)), np.mean((output != Y_train[:,0]) * (output == 0) * (X_train[:,12] == 1)))

def ANN(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val):
    
    '''
    base_dir = (os.path.dirname(os.path.realpath(__file__)))
    exp_dir = os.path.join(base_dir, 'exp')
    dir_cnt = 1; epoch = 400
    log_path = "epoch{}".format(str(epoch)); log_path += "_"
    store_path = os.path.join(exp_dir,log_path + str(dir_cnt))

    while(dir_cnt<30):
        if not os.path.isdir(store_path):
            os.mkdir(store_path)
            break
        else:
            dir_cnt += 1
            store_path = os.path.join(exp_dir,log_path+str(dir_cnt))
    '''
    table = computeMean_Var(X_train) 
    normalize(X_train, table); normalize(X_val, table); normalize(X_test_public, table)

    Y_train = np_utils.to_categorical(Y_train, 2)
    Y_val = np_utils.to_categorical(Y_val, 2)

    model = Sequential()

    model.add(Dense(input_dim=72, units=512));
    model.add(keras.layers.advanced_activations.PReLU(alpha_initializer='zero', weights=None));
    model.add(Dense(units=256));
    model.add(keras.layers.advanced_activations.PReLU(alpha_initializer='zero', weights=None));
    model.add(Dropout(0.4))
    model.add(Dense(units=256));
    model.add(keras.layers.advanced_activations.PReLU(alpha_initializer='zero', weights=None));
    model.add(Dropout(0.4))
    model.add(Dense(units=128));
    model.add(keras.layers.advanced_activations.PReLU(alpha_initializer='zero', weights=None));
    model.add(Dropout(0.3))
    model.add(Dense(units=128));
    model.add(keras.layers.advanced_activations.PReLU(alpha_initializer='zero', weights=None));
    model.add(Dropout(0.3))

    model.add(Dense(units=2, activation="softmax"));
    model.summary();

    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy']);
    #model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy']);

    earlystopping = EarlyStopping(monitor='val_acc', patience = 20, verbose=1, mode='max')
    checkpoint = ModelCheckpoint(filepath='best2.hdf5', verbose=1, save_best_only=True, save_weights_only=False, monitor='val_acc', mode='max')

    nb_epoch = 100; b_size = 64
    hist = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=nb_epoch, batch_size=b_size, callbacks=[earlystopping, checkpoint])

    prob_output = model.predict(X_test_public)
    output = prob_output.argmax(axis=1); output = np.transpose([output]);
    #check_answer(output, 'Test_2_ans.csv')

    #MAP_eval(prob_output, 'Test_2_ans.csv', top_M)

    #history = History();
    #filepath = os.path.join(store_path,'model.{epoch:03d}-{val_acc:.4f}.h5');
    #model.fit(X_train, Y_train, batch_size=64, epochs=epoch, validation_data=(X_val, Y_val), callbacks=[history]);
    #dump_history(store_path,history);
    #model.save(os.path.join(store_path,'model.h5'));


if __name__ == '__main__':

    oneHot = 1
    X_train, X_val, Y_train, Y_val = preprocessing(sys.argv[1], oneHot, True)
    X_test_public = preprocessing(sys.argv[2], oneHot, False)
    X_test_private = preprocessing(sys.argv[3], oneHot, False)

    random_forest(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
    #logistic(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
    #adaptive_boosting(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
    #KNN(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
    #sklearn_logistic(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
    #ANN(X_train, X_val, X_test_public, X_test_private, Y_train, Y_val)
   


