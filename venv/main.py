"""
modified keras code from the following sources:
https://medium.com/nybles/create-your-first-image-recognition-classifier-using-cnn-keras-and-tensorflow-backend-6eaab98d14dd
"""
from keras.models import Sequential
from keras.layers import Convolution2D, Flatten, Dense, Dropout
from keras.layers import MaxPooling2D, AveragePooling2D
from keras.utils import to_categorical
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import adam

import cv2
from graph import Graph
import config as CFG
import numpy as np
from contextlib import redirect_stdout
import matplotlib.pyplot as plt


def keras_network(train_data, train_labels, test_data, test_labels, batch):
    """
    Creates a neural network using the Keras library with Tensorflow backend
    :param train_data: sliced training data
    :param train_labels: actual labels for training data
    :param test_data: sliced testing data
    :param test_labels: actual labels for test data
    :param batch: batch size for gradient descent
    """
    training_accuracy = []
    training_loss = []
    testing_accuracy = []
    testing_loss = []

    # preprocess images: augment data
    if CFG.AUGMENT_IMAGES:
        datagen = ImageDataGenerator(
            # Randomly apply the following parameters to the images
            width_shift_range=0.1,    # shift images horizontally
            height_shift_range=0.1,   # shift images vertically
            shear_range=0.1,          # shear images
            fill_mode='nearest',      # set mode for filling points outside the input boundaries
            zoom_range=[0.95, 1.05],  # set a zoom range randomly applied to images
            horizontal_flip=True)     # flip images horizontally

        datagen.fit(train_data)
        steps_per_epoch = len(train_data) // batch
        print(f'steps_per_epoch = {steps_per_epoch}')

    classifier = Sequential()

    # build model
    print(f'build model')
    # input layer
    classifier.add(Convolution2D(32, (3, 3), input_shape=train_data.shape[1:], activation=CFG.ACTIVATE_FN[0]))
    classifier.add(AveragePooling2D(pool_size=(2, 2)))

    if CFG.DROPOUT:
        classifier.add(Dropout(0.2))

    # added layer
    classifier.add(Convolution2D(64, (3, 3), activation=CFG.ACTIVATE_FN[1]))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # added layer
    classifier.add(Convolution2D(128, (3, 3), activation=CFG.ACTIVATE_FN[2]))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # layer
    classifier.add(Flatten())
    classifier.add(Dense(output_dim=128, activation=CFG.ACTIVATE_FN[3]))

    # output layer
    classifier.add(Dense(output_dim=CFG.OUTPUT_SIZE, activation=CFG.ACTIVATE_FN[4]))

    # compile model
    print(f'compile model')
    optimizer = adam(lr=CFG.ETA, beta_1=CFG.BETA1, beta_2=CFG.BETA2)
    classifier.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['categorical_accuracy'])

    # train the model
    print(f'train model')
    for e in range(CFG.EPOCHS):
        print(f'===================== EPOCH {e} =====================')

        if CFG.AUGMENT_IMAGES:
            tr_results = classifier.fit_generator(datagen.flow(train_data, train_labels, batch_size=batch),
                                                               epochs=1, steps_per_epoch=steps_per_epoch)
        else:
            tr_results = classifier.fit(train_data, train_labels, batch_size=batch, epochs=1)

        classifier.summary()

        # run the classifier on the test data
        epoch_accuracy = classifier.evaluate(test_data, test_labels, batch_size=batch)
        print(f'=============== TEST RESULTS ===============')
        print(f'evaulation classifier score: {epoch_accuracy}')
        print("%s: %.2f%%" % (classifier.metrics_names[1], epoch_accuracy[1] * 100))
        print(f'============================================')
        testing_accuracy.append(epoch_accuracy[1])
        testing_loss.append(epoch_accuracy[0])
        training_accuracy.append(tr_results.history['categorical_accuracy'])
        training_loss.append(tr_results.history['loss'])
    print(f'=====================================================')

    path = CFG.GRAPHS_DIR + 'summary.txt'
    with open(path, 'w') as file:
        with redirect_stdout(file):
            classifier.summary()

    return testing_accuracy, testing_loss, parse_functions(CFG.ACTIVATE_FN), training_accuracy, training_loss


def parse_functions(activation_fns: [str]):
    """
    Parses all of the activation functions so that they can be used as descriptors
    :param activation_fns: all activation functions that were used
    :return: a string of activation functions
    """
    total = len(activation_fns)
    if total < 2:
        if total < 1:
            return str(activation_fns)
        return activation_fns[1]

    fn_strings = ""
    for fn in range(total):
        fn_strings += activation_fns[fn]
        if fn != total - 1:
            fn_strings += "-"

    return fn_strings


def visualization(count, training_size, training_accuracy, training_cost, test_size, test_accuracy, test_cost,
                  function_name, batch):

    # create graph objects
    graph = Graph(count, training_size, training_accuracy, test_size, test_accuracy, function_name,
                           batch, "Accuracy Plot")

    # plot accuracy
    if CFG.ANNOTATE:
        graph.plot_accuracy(annotate=True)
    else:
        graph.plot_accuracy()

    # generate tabular data
    graph.tabular_data()

    # generate training cost plot
    if CFG.PLOT_COST:
        graph.plot_cost(training_cost.ravel(), test_cost.ravel())


def load_data() -> ((), ()):
    """
    Loads images of from defined dataset
    :return: lists of training data and testing data
    """
    (train_data, train_labels), (test_data, test_labels) = mnist.load_data()



    # visualize sample of data
    # src: http://home.mit.bme.hu/~hadhazi/Oktatas/NN18/dem3/html_demo/CIFAR-10Demo.html
    if CFG.SHOW_SAMPLE_IMAGES:

        f, axarr = plt.subplots(1, 5)
        f.set_size_inches(16, 6)

        for i in range(5):
            img = train_data[i]
            axarr[i].imshow(img)
        plt.show()


    train_data = train_data.astype('float32') / 255
    test_data = test_data.astype('float32') / 255

    # resize to work with tensorflow
    training_data = train_data.reshape(train_data.shape[0], CFG.ROW, CFG.COL, CFG.DEPTH)
    testing_data = test_data.reshape(test_data.shape[0], CFG.ROW, CFG.COL, CFG.DEPTH)

    total_classes = CFG.TOTAL_LABELS
    training_labels = to_categorical(train_labels, total_classes)
    test_labels = to_categorical(test_labels, total_classes)

    return (training_data, training_labels), (testing_data, test_labels)


def main():

    experiment_count = 1

    # grab specified data set and preprocess it for network training
    (train_data, train_labels), (test_data, test_labels) = load_data()
    training_size, _, _, _ = train_data.shape
    test_size, _, _, _ = test_data.shape

    # use Keras to create Neural Network
    test_accuracy, test_loss, function_names, \
        training_accuracy, training_loss = keras_network(train_data, train_labels, test_data, test_labels,
                                                         CFG.BATCH_SIZE)

    # Test print of results
    print(f'====================== RESULTS ======================')
    print(f'\n\ntraining_accuracy: {training_accuracy}\n')
    print(f'\ntraining_loss: {training_loss}\n')
    print(f'\n\ntest_accuracy: {test_accuracy}\n')
    print(f'\ntest_loss: {test_loss}\n')
    print(f'=====================================================')
    print(f'=====================================================')

    training_accuracy = np.asarray(training_accuracy)
    training_loss = np.asarray(training_loss)

    test_accuracy = np.asarray(test_accuracy)
    test_loss = np.asarray(test_loss)

    training_accuracy = np.nan_to_num(training_accuracy)
    training_loss = np.nan_to_num(training_loss)

    test_accuracy = np.nan_to_num(test_accuracy)
    test_loss = np.nan_to_num(test_loss)

    training_accuracy *= 100
    test_accuracy *= 100

    # visualize various results in plots
    visualization(experiment_count, training_size, training_accuracy, training_loss, test_size, test_accuracy,
                  test_loss, function_names, CFG.BATCH_SIZE)

    experiment_count += 1


if __name__ == '__main__':
    main()