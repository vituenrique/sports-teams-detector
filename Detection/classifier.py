import mahotas as mh
import numpy as np
import os
from glob import glob

from features import features, histogram
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Extract features  
def extractFeatures(hists, haralicks, labels, images):
    for fname in sorted(images):
        imc = mh.imread(fname)
        haralicks.append(features(mh.colors.rgb2grey(imc)))
        hists.append(histogram(imc))
        # Extract file path and its extention leaving only the filename
        labels.append(os.path.splitext(os.path.basename(fname[:-len('xxx.jpg')]))[0])

# Save model 
def saveModel(fileName, model):
    from sklearn.externals import joblib
    joblib.dump(model, fileName)

basePath = './dataset/allFiles/'

haralicks = []
classes = []
hists = []

print('Computing features...')

# Get all the images
images = glob('{}/*.png'.format(basePath))

# Extract Features(haralicks), Histograms(hists) and classes(labels) 
extractFeatures(hists, haralicks, classes, images)    

print('Finished computing features.')

haralicks = np.array(haralicks)
classes = np.array(classes)
hists = np.array(hists)
haralick_plus_hists = np.hstack([hists, haralicks])

from sklearn.model_selection import cross_val_score, ShuffleSplit, train_test_split
# Split dataset for train and test
x_train, x_test, y_train, y_test = train_test_split(haralicks, classes, test_size=0.5, random_state=0)


standardScaler = StandardScaler()
logisticRegression = LogisticRegression(C = 100)
clf = Pipeline([('preproc', standardScaler),('classifier', logisticRegression)])

cv = ShuffleSplit(n_splits=7, test_size=0.5, random_state=0)

from sklearn.metrics import classification_report
# Train classifier
logisticRegression = logisticRegression.fit(x_train, y_train)
# Predict classifications for test set
y_pred = logisticRegression.predict(x_test)
print(y_pred)
# Output results
print("Logistic regression: \n%s\n" % (classification_report(y_test, y_pred, target_names=['teamA','teamB'])))

# Cross-validation scores using Logistic Regression Classifier
scores = cross_val_score(logisticRegression, hists, classes, cv=cv)
print('Accuracy with Logistic Regression [color histograms]: {:.1%}'.format(scores.mean()))

# Save trained model
savingPath = '../Detection/Models/'
if not os.path.exists(savingPath):
    os.mkdir(savingPath)
saveModel(savingPath + 'model.sav', logisticRegression)


