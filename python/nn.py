import time
import tqdm
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Conv2D, Flatten
from sklearn.model_selection import KFold


def main():
    path = input("Input path to dataset:\n> ")
    dataset = np.loadtxt(path)
    (x_train, y_train), (x_test, y_test) = get_images()

    n = 0
    for i,row in enumerate(dataset):
        dataset[i] = row.append(n)
        if (i > 0 and i % 100 == 0):
            n += 1
    # Label1 = syphilis
    # Label2 = herpes
    # Label3 = oral cancer
    # Label4 = healthy

    # Running analysis with keras over each possibility, using 10-fold CV.
    analysis = evaluate_architecture_keras(dataset)

    # Collecting result and determining best set of parameters.
    print("\n\nBest mean accuracy over 10-fold cross validation with accuracy: %.2f%%" % (analysis))

    # Predict the output of the given dataset.
    #print("Predictions are:\n ", predict_hidden(dataset,model))

def evaluate_architecture_keras(dataset):

    # Dataset style
    X = dataset[:,:-1]
    Y = dataset[:,-1]

    # Define 10-fold cross validation test harness.
    kfold = KFold(n_splits=10, shuffle=True)
    cvscores = []

    for j,(train,test) in enumerate(kfold.split(X, Y)):
        # Create model.
        model = Sequential()

        model.add(Conv2D(64, kernel_size=3, activation=’relu’, input_shape=(28,28,1)))
        model.add(Conv2D(32, kernel_size=3, activation=’relu’))
        model.add(Flatten())
        model.add(Dense(4, activation=’softmax’))

        # Compile model.
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model.
        model.fit(X[train], Y[train], epochs=3)

        # Evaluate the model.
        scores = model.evaluate(X[test], Y[test], verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        cvscores.append(scores[1] * 100)

    mean = np.mean(cvscores)
    std = np.std(cvscores)
    print("%.2f%% (+/- %.2f%%)" % (mean, std))
    return mean

def confusion_matrix(pred, Y):
    c_m = np.zeros((4,4))
    for i in range(len(Y)):
        true = list(Y[i][-4:]).index(1.0)
        p = list(pred[i][-4:]).index(1)
        c_m[true, p] += 1
    return c_m

def predict_hidden(dataset, model):
    X = dataset[:,:-2]
    Y = dataset[:,-1]

    # Evaluate loaded model on test data
    model.compile(loss='categorical_crossentropy', optimizer='nadam', metrics=['accuracy'])
    predictions = model.predict(X)
    # pred = [list(map(lambda x: 1 if x > 0.2 else 0, predictions[i])) for i in range(len(predictions))]
    # c_m = confusion_matrix(pred, Y)
    # print(c_m)
    return predictions

if __name__ == "__main__":
    main()
