from os import getcwd

TEST_CODE = True  # True if testing code, False if running neural network fully
if TEST_CODE:
    print(f'You are in CODE TESTING mode. To switch to regular program mode,\n'
          f'change `TEST_CODE = True` in config.py')

    # Training/Testing Specs
    EPOCHS = 2
    SPLIT = 59900  # validation data size
else:
    # Training/Testing Specs
    EPOCHS = 300
    SPLIT = 10000  # validation data size

# Network Layer Sizes
OUTPUT_SIZE = 13
DROPOUT = False
DROP_VAL = 0.3

# Hyperparameters
ETA = 0.001
BETA1 = 0.9
BETA2 = 0.999

# Training/Testing Specs
AUGMENT_IMAGES = False   # If True, augments images, if False, uses original images
VALIDATE = False  # If True, create validation data, if False, no validation data is used
BATCH_SIZE = 32
ACTIVATE_FN = ["relu", "relu", "relu", "relu", "softmax"]

# Image Specs
ROW = 32
COL = 32
DEPTH = 1
TOTAL_LABELS = 13

# Graph Specs
ANNOTATE = False  # if True, annotate accuracies, if False, don't annotate
ANNOTATE_LEVEL = 95  # percentage above which annotations occur
COLOR_ACCURACY = ['#f15d29', '#37744a']  # green and blue line
COLOR_COST = ['#f15d29', '#37744a']  # red and green lines
PLOT_COST = True  # if True, plots cost values, if False, does not plot cost values

# Directories and Files
GRAPHS_DIR = getcwd() + '/accuracy_graphs/'  # directory for storing accuracy graphs
