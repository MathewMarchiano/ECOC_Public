import numpy as np
import seaborn as sn
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import Counter

# Contains methods for making graphs for anomaly detection (general).
class Visuals():

    def graphThresholdTestHistogram(self, knownHDs, unknownHDs, threshold,
                                    codebookNum, split, knownAcc,
                                    unknownAcc, seed, holdout, allData,
                                    unknownData, knownTrain, codeBook,
                                    knownSingleDataPoints, saveFolderPath, selectedClassifier, isBuilding):
        '''
        Graphs the number of instances of a particular hamming distance. Distinguishes between
        hamming distances that are supposed to be known or unknown.
        The last parameter "isBuilding" is used to differentiate this function when being used to visualize
        building the threshold (True) or visualize testing the threshold (False). This ensures that calling this
        function won't overwrite itself when trying to show 2 different histograms.

        :param knownHDs: List of Hamming distances generated using known data.
        :param unknownHDs: List of Hamming distances generated using unknown data.
        :param threshold: Threshold determined to be most optimal.
        :param codebookNum: Number of codebook you're currently on during Anomaly Detection tests.
        :param split: Unknown split of data you're currently on.
        :param knownAcc: Accuracy of known predictions.
        :param unknownAcc: Accuracy of unknown predictions.
        :param seed: Seed used for classifier.
        :param holdout: Holdout index you're on.
        :param allData: All original data samples.
        :param unknownData: All unknown data samples.
        :param knownTrain: All data used for training.
        :param codeBook: Codebook you're currently using.
        :param knownSingleDataPoints: List of all the single samples of data used to test the threshold.
        :param saveFolderPath: Path of the folder you want the figure to save to.
        :param selectedClassifier: Classifier used for the particular run.
        :param isBuilding: Whether or not this method is being used to show histograms of the Hamming distances
                           generated for building the threshold or testing the threshold (necessary for naming folder).
        :return: A histogram of the known and unknown Hamming distances along with the threshold being shown visually.
        '''
        bins = np.arange(20)
        ax = plt.subplot(111)
        thresholdText = "Optimal Threshold: " + str(threshold)
        title = "Codebook: " + str(codebookNum) + " Split: " + str(split) + " new" + "\n Seed: " + str(
            seed) + "\n Holdout: " + str(holdout)
        oldAccruacyText = "Known Classes: (" + str(round(knownAcc, 2)) + ")"
        newAccuracyText = "Unknown Classes: (" + str(round(unknownAcc, 2)) + ")"

        ax.hist([knownHDs], bins=bins - .5, alpha=1, label=oldAccruacyText, ec='black')
        ax.hist([unknownHDs], bins=bins - .5, alpha=0.60, label=newAccuracyText, ec='black', color='green')
        ax.axvline(x=threshold, color='r', linestyle='dashed', linewidth=3, label=thresholdText)
        ax.set_xlabel("Minimum Hamming Distance")
        ax.set_ylabel("Frequency")
        ax.set_title(title)

        # Setting up the legend
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        handles, labels = ax.get_legend_handles_labels()
        # For the line below, bbox_to_anchor manages where the legend will be located
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

        knownData = len(allData) - len(unknownData)
        percentTraining = round((len(knownTrain) / knownData), 2)
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"]
        if isBuilding:
            saveInfo = saveFolderPath + "\\" + "_BuildingThreshold_" + models[selectedClassifier - 1] +"_CB"+ str(codebookNum) + "_CWLength(" + str(len(codeBook[0])) \
                       + ")_Holdout" + str(holdout) + "_Split" + str(split) + "_Threshold" \
                       + str(threshold) +"_UnknownHoldoutClasses1_KnownHoldoutSamples" \
                       + str(len(knownSingleDataPoints)) + "_PercentTrainingData" \
                       + str(percentTraining) + ".png"
        else:
            saveInfo = saveFolderPath + "\\" + "_TestingThreshold_" + models[selectedClassifier - 1] + "_CB" + str(
                codebookNum) + "_CWLength(" + str(len(codeBook[0])) \
                       + ")_Holdout" + str(holdout) + "_Split" + str(split) + "_Threshold" \
                       + str(threshold) + "_UnknownHoldoutClasses1_KnownHoldoutSamples" \
                       + str(len(knownSingleDataPoints)) + "_PercentTrainingData" \
                       + str(percentTraining) + ".png"
        plt.savefig(saveInfo, dpi = 300,
                    bbox_extra_artists = (lgd,), bbox_inches = 'tight')
        # plt.show()
        plt.clf()


    def graphHoldoutHDs(self, threshold, holdoutHammingDistances,
                        accuracy, codebookNum, split,
                        seed, holdout, saveFolderPath, selectedClassifier):
        '''
        Graphs the holdout class's HDs against the threshold.

        :param threshold: Threshold determined to be most optimal.
        :param holdoutHammingDistances: List of Hamming distances generated using the holdout class's data.
        :param accuracy: Accuracy of the predictions.
        :param codebookNum: Number of the codebook you are on.
        :param split: Split you are currently on.
        :param seed: Seed used for classifier.
        :param holdout: Index of the holdout you're currently on.
        :param saveFolderPath: Path the folder that will be used to save the figure.
        :param selectedClassifier: Classifier used for making predictions.
        :return: A figure of the holdout Hamming distances graphed.
        '''
        bins = np.arange(20)

        thresholdText = "Optimal Threshold: " + str(threshold)
        title = "Codebook: " + str(codebookNum) + " Split: " + str(split) + " new" + "\n Seed: " + str(
            seed) + "\n Holdout: " + str(holdout)
        accruacyText = "Accuracy: (" + str(round(accuracy, 2)) + ")"

        plt.hist([holdoutHammingDistances], bins=bins - .5, alpha=1, label=accruacyText, ec='black', color='green')
        plt.axvline(x=threshold, color='r', linestyle='dashed', linewidth=3, label=thresholdText)
        plt.xlabel("Minimum Hamming Distance")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.legend(loc='upper right')
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"]
        plt.savefig(saveFolderPath + "\\" + str(holdout) + "_" + str(split)
                    + "_" + str(threshold) + "_" + str(codebookNum) + "_" + models[selectedClassifier - 1] + ".png")
        # plt.show()
        plt.clf()

    def singleDataHoldoutHistogram(self, threshold, holdoutHammingDistances,
                                   accuracy, codebookNum, split,
                                   seed, holdout, saveFolderPath, selectedClassifier):
        '''
        Graphs the single data samples' hamming distances against the threshold.

        :param threshold: Threshold determined to be most optimal.
        :param holdoutHammingDistances: Hamming distances generated by using the single data samples.
        :param accuracy: Accuracy of the predictions.
        :param codebookNum: Codebook number you are currently on.
        :param split: Split you're currently.
        :param seed: Seed you're using
        :param holdout: Index of holdout you're currently using.
        :param saveFolderPath: Path of the folder you're going to save the figure to.
        :param selectedClassifier: Classifier used for making predictions.
        :return: Figure of the single data samples prediction's HD's graphed.
        '''
        bins = np.arange(20)

        thresholdText = "Optimal Threshold: " + str(threshold)
        title = "Codebook: " + str(codebookNum) + " Split: " + str(split) + " new" + "\n Seed: " + str(
            seed) + "\n Holdout: " + str(holdout)
        accruacyText = "Accuracy: (" + str(round(accuracy, 2)) + ")"

        plt.hist([holdoutHammingDistances], bins=bins - .5, alpha=1, label=accruacyText, ec='black', color='green')
        plt.axvline(x=threshold, color='r', linestyle='dashed', linewidth=3, label=thresholdText)
        plt.xlabel("Minimum Hamming Distance")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.legend(loc='upper right')
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"]
        plt.savefig(saveFolderPath + "\\" + str(holdout) + "_" + str(split)
                    + "_" + str(threshold) + "_" + str(codebookNum) + "_" + models[selectedClassifier - 1] +".png")
        plt.show()
        plt.clf()

    def accuraciesPlot_MinMaxValues(self, knownAccMinDict, knownAccMaxDict,
                                    unknownAccMinDict, unknownAccMaxDict, knownMean,
                                    unknownMean, codeBook, knownTrain, allData,
                                    unknownData, knownSingleDataPoints, saveFolderPath, selectedModel,
                                    listOfSplits, codebookNum, percentKnownClasses):
        '''
        Graphs the accuracies (for known/unknown predictions) for each split.

        :param knownAccMinDict: Dictionary with key = split and value = split's known accuracy (min across all holdouts)
        :param knownAccMaxDict: Dictionary with key = split and value = split's known accuracy (max across all holdouts)
        :param unknownAccMinDict: Dictionary with key = split and value = split's unknown accuracy (min across all holdouts)
        :param unknownAccMaxDict: Dictionary with key = split and value = split's unknown accuracy (max across all holdouts)
        :param knownMean: Mean (across all holdouts) of the known prediction accuracies.
        :param unknownMean: Mean (across all holdouts) of the unknown predictions accuracies.
        :param codeBook: Codebook being used.
        :param knownTrain: Data that was used for training the classifiers.
        :param allData: All of the data (regardless of the split it belongs to).
        :param unknownData: All data belonging to the unknown split.
        :param knownSingleDataPoints: The single samples of known data used to test the threshold.
        :param saveFolderPath: Path of the folder that will be used to save the figure.
        :param selectedModel: Model used to make the predictions.
        :param listOfSplits: All the splits used for testing.
        :param codebookNum: The number of the codebook you're currently on.
        :return: A figure showing the accuracies of known/unknown predictions across all desired splits.
        '''
        ax = plt.subplot(111)

        # Representation of min and max values.
        ax.plot(list(knownAccMaxDict.keys()), list(knownAccMaxDict.values()), marker='o', color='blue', label='Known Max')
        ax.plot(list(knownAccMinDict.keys()), list(knownAccMinDict.values()), marker='o', color='red', label='Known Min')
        ax.plot(list(unknownAccMinDict.keys()), list(unknownAccMinDict.values()), marker='o', color='green',
                 label='Unknown Min')
        ax.plot(list(unknownAccMaxDict.keys()), list(unknownAccMaxDict.values()), marker='o', color='black',
                 label='Unknown Max')


        # Representation of the means.
        ax.plot(list(knownMean.keys()), list(knownMean.values()), marker='o', color='magenta',
                 label='Known Mean', linestyle = '--')

        ax.plot(list(unknownMean.keys()), list(unknownMean.values()), marker='o', color='cyan',
                 label='Unknown Mean', linestyle = '--')

        plt.xticks(listOfSplits)
        plt.yticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1])


        ax.set_title("Detection Rate per Split")
        ax.set_xlabel("Percent Unknown")
        ax.set_ylabel("Accuracy")

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

        knownData = len(allData) - len(unknownData)
        percentTraining = round((len(knownTrain)/knownData), 2)
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"] # Corresponds to the number assigned for each classifier in Trainer.py
        # selectedModel has 1 subtracted from it because the models in the Trainer class are assigned with numbers
        # 1 - 4.
        saveInfo = saveFolderPath + "\\" + models[selectedModel - 1] +"_CB" + str(codebookNum) +"_CWLength(" + str(
            len(codeBook[0])) + ")" + "_UnknownHoldoutClasses1_KnownHoldoutSamples" \
            + str(len(knownSingleDataPoints))+ "_PercentTrainingData"+ str(percentTraining)+ \
            "_PercentKnownClasses" + str (percentKnownClasses) + ".png"

        plt.savefig(saveInfo, dpi = 300, bbox_extra_artists = (lgd,), bbox_inches = 'tight')
        plt.show()
        plt.clf()

    def accuraciesPlot_MeansOnly(self, knownMean,
                                 unknownMean, codeBook, knownTrain, allData,
                                 unknownData, knownSingleDataPoints, saveFolderPath, selectedModel,
                                 listOfSplits, codebookNum, percentKnownClasses):
        '''
        Graphs the accuracies (for known/unknown predictions) for each split.

        :param knownAccMinDict: Dictionary with key = split and value = split's known accuracy (min across all holdouts)
        :param knownAccMaxDict: Dictionary with key = split and value = split's known accuracy (max across all holdouts)
        :param unknownAccMinDict: Dictionary with key = split and value = split's unknown accuracy (min across all holdouts)
        :param unknownAccMaxDict: Dictionary with key = split and value = split's unknown accuracy (max across all holdouts)
        :param knownMean: Mean (across all holdouts) of the known prediction accuracies.
        :param unknownMean: Mean (across all holdouts) of the unknown predictions accuracies.
        :param codeBook: Codebook being used.
        :param knownTrain: Data that was used for training the classifiers.
        :param allData: All of the data (regardless of the split it belongs to).
        :param unknownData: All data belonging to the unknown split.
        :param knownSingleDataPoints: The single samples of known data used to test the threshold.
        :param saveFolderPath: Path of the folder that will be used to save the figure.
        :param selectedModel: Model used to make the predictions.
        :param listOfSplits: All the splits used for testing.
        :param codebookNum: The number of the codebook you're currently on.
        :return: A figure showing the accuracies of known/unknown predictions across all desired splits.
        '''
        ax = plt.subplot(111)

        # Representation of the means.
        ax.plot(list(knownMean.keys()), list(knownMean.values()), marker='o', color='magenta',
                label='Known Mean')

        ax.plot(list(unknownMean.keys()), list(unknownMean.values()), marker='o', color='cyan',
                label='Unknown Mean')

        plt.xticks(listOfSplits)
        plt.yticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1])

        ax.set_title("Detection Rate per Split")
        ax.set_xlabel("Percent Unknown")
        ax.set_ylabel("Accuracy")

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

        knownData = len(allData) - len(unknownData)
        percentTraining = round((len(knownTrain) / knownData), 2)
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes",
                  "Random Forest"]  # Corresponds to the number assigned for each classifier in Trainer.py
        # selectedModel has 1 subtracted from it because the models in the Trainer class are assigned with numbers
        # 1 - 4.
        saveInfo = saveFolderPath + "\\" + models[selectedModel - 1] + "_CB" + str(
            codebookNum) + "_CWLength(" + str(
            len(codeBook[0])) + ")" + "_UnknownHoldoutClasses1_KnownHoldoutSamples" \
                   + str(len(knownSingleDataPoints)) + "_PercentTrainingData" + str(percentTraining) + \
                   "_PercentKnownClasses" + str(percentKnownClasses) + ".png"

        plt.savefig(saveInfo, dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.show()
        plt.clf()

    # USED FOR graphROC. Utilizes the trapezoid rule to approximate AUC.
    def auc_from_fpr_tpr(self, fpr, tpr, trapezoid=False):
        fpr.sort()
        tpr.sort()
        area = 0
        ft = list(zip(fpr, tpr))
        for p0, p1 in zip(ft[: -1], ft[1:]):
            area += (p1[0] - p0[0]) * ((p1[1] + p0[1]) / 2 if trapezoid else p0[1])
        return area

    def graphROC(self, unknownAccs, knownAccs, split, codeBook, saveFolderPath, selectedModel, bestKnownAcc,
                 bestUnknownAcc, averagedOptimalThreshold, codebookNum):
        '''
        Creates an ROC graph. unknownAccs used for true positive rate. knownAccs used for false positive rate.
        besteknownAccs is used to graph the point on the ROC that corresponds to the accuracy of the threshold
        that was determined to be most optimal.

        :param unknownAccs: List of unknown accuracies.
        :param knownAccs: List of known accuracies.
        :param split: Split that's currently being used.
        :param codeBook: Codebook that's currently being used.
        :param saveFolderPath: Path of the folder that will be used to save the figure.
        :param selectedModel: Model being used to make the predictions.
        :param bestKnownAcc: Highest known accuracy (across all the holdouts).
        :param bestUnknownAcc: Highest unknown accuracy (across all the holdouts).
        :param averagedOptimalThreshold: Optimal threshold averaged across all holdouts.
        :param codebookNum: Number of the codebook you're currently on.
        :return: A ROC graph that also shows the optimal threshold that corresponds to the highest known/unknown accuracy.
        '''
        fprList = []
        bestFPR = 1 - bestKnownAcc
        # False Positive Rate is = 1 - specificity
        for acc in knownAccs:
            fprList.append(1 - acc)
        AUC = self.auc_from_fpr_tpr(fprList, unknownAccs)
        titleString = "ROC\nAUC="+ str(round(AUC, 2))
        ax = plt.subplot(111)
        ax.set_title(titleString)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.plot([0,1],[0,1], 'k--')
        ax.axis([0, 1, 0, 1,])
        ax.plot(fprList, unknownAccs, linewidth=2, label=None)
        roundedAvgOptimalThreshold = round(averagedOptimalThreshold, 1)
        roundedBestAcc = round(bestUnknownAcc, 2)

        ax.scatter(bestFPR, bestUnknownAcc, color='red', label="Avg. Optimal Threshold=" + str(roundedAvgOptimalThreshold) + "\nAccuracy=" + str(roundedBestAcc))
        ax.legend(loc='lower right')
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest",
                  "KMeansClustering", "OneClassSVM"]
        saveInfo = saveFolderPath + "\\" + models[selectedModel - 1] + "_CB"+ str(codebookNum) + "_CWLength(" + str(
            len(codeBook[0])) + ")" + "_Split(" + str(split) + ")" + ".png"
        plt.savefig(saveInfo)
        plt.show()
        plt.clf()

    def graphROC_VaryingCodelengthTest(self, unknownAccs, knownAccs,
                                       bestKnownAcc,
                                       bestUnknownAcc, averagedOptimalThreshold):
        '''
        Creates an ROC graph. unknownAccs used for true positive rate. knownAccs used for false positive rate.
        besteknownAccs is used to graph the point on the ROC that corresponds to the accuracy of the threshold
        that was determined to be most optimal.

        :param unknownAccs: List of unknown accuracies.
        :param knownAccs: List of known accuracies.
        :param split: Split that's currently being used.
        :param codeBook: Codebook that's currently being used.
        :param saveFolderPath: Path of the folder that will be used to save the figure.
        :param selectedModel: Model being used to make the predictions.
        :param bestKnownAcc: Highest known accuracy (across all the holdouts).
        :param bestUnknownAcc: Highest unknown accuracy (across all the holdouts).
        :param averagedOptimalThreshold: Optimal threshold averaged across all holdouts.
        :param codebookNum: Number of the codebook you're currently on.
        :return: A ROC graph that also shows the optimal threshold that corresponds to the highest known/unknown accuracy.
        '''
        # CB1
        fprList = []
        bestFPR = 1 - bestKnownAcc[0]
        # False Positive Rate is = 1 - specificity
        for acc in knownAccs[0]:
            fprList.append(1 - acc)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1, ])

        plt.plot(fprList, unknownAccs[0], linewidth=2, label="1.0c Codeword Length", color='green', zorder=1)

        plt.scatter(bestFPR, bestUnknownAcc[0], color='red',
                   label="Avg. Optimal Threshold", zorder=2)

        # # CB2
        fprList = []
        bestFPR = 1 - bestKnownAcc[1]
        # False Positive Rate is = 1 - specificity
        for acc in knownAccs[1]:
            fprList.append(1 - acc)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1, ])
        plt.plot(fprList, unknownAccs[1], linewidth=2, label="1.5c Codeword Length", color='blue', zorder=1)

        plt.scatter(bestFPR, bestUnknownAcc[1], color='red', zorder=2)

        # # CB3
        fprList = []
        bestFPR = 1 - bestKnownAcc[2]
        # False Positive Rate is = 1 - specificity
        for acc in knownAccs[2]:
            fprList.append(1 - acc)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1, ])
        plt.plot(fprList, unknownAccs[2], linewidth=2, label="2.0c Codeword Length", color='black', zorder=1)

        plt.scatter(bestFPR, bestUnknownAcc[2], color='red', zorder=2)

        plt.legend()
        plt.show()
        plt.clf()

    def generateConfusionMatrix(self, predictedValues, actualValues, codebook, saveFolderPath, selectedModel,
                                        codebookNum, split):
        '''
        Generates a confusion matrix using all the predictions made across all the holdouts.

        :param predictedValues: List of lists containing all the predictions for a particular holdout.
        :param actualValues: The label/class that would be the "correct answer"
        :param codebook: Codebook you're currently using.
        :param saveFolderPath: Path of the folder you want the figure to save to.
        :param selectedModel: Model being used to make the predictions.
        :param codebookNum: Number of the codebook being used.
        :param split: Percentage of unknown classes being used.
        :return: A confusion matrix generated from the predictions made across all holdouts for a particular split and CB.
        '''
        # numUniqueLabels has 1 added to it in order to account for the unknown label
        numUniqueLabels = len(codebook) + 1
        confusionMatrix = []
        # Create an (numUniqueLabels)x(numUniqueLabels) confusion matrix
        for row in range(numUniqueLabels):
            confusionMatrix.append([])
        for row in confusionMatrix:
            for column in range(numUniqueLabels):
                row.append(0)

        for predictions, actuals in zip(predictedValues, actualValues):
            for prediction, actual in zip(predictions, actuals):
                # If prediction is labeled as known, find row and column that it should
                # be graphed at
                if prediction in codebook:
                    rowNumber = codebook.index(actual)
                    columnNumber = codebook.index(prediction)
                    confusionMatrix[rowNumber][columnNumber] += 1
                # Otherwise, the prediction is unknown
                else:
                    rowNumber = codebook.index(actual)
                    confusionMatrix[rowNumber][numUniqueLabels - 1] += 1

        # Show confusion matrix before the averaging
        plt.figure(figsize=(20, 15))
        ax = plt.subplot()
        sn.heatmap(confusionMatrix, annot=True, ax=ax)
        ax.set_xlabel('Predictions')
        ax.set_ylabel('True Values')
        ax.set_title('Confusion Matrix')
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"]
        saveInfo = saveFolderPath + "\\" + "_Original_" + models[selectedModel - 1] + "_CB" + str(codebookNum) + "_CWLength(" + str(
            len(codebook[0])) + ")" + "_Split(" + str(split) + ")" + ".png"
        plt.savefig(saveInfo, dpi=100)
        plt.show()
        plt.clf()

        # Average confusion matrix across row-wise:
        cmDimension = len(confusionMatrix)
        for row in range(cmDimension):
            rowSum = 0
            for column in range(cmDimension):
                rowSum += confusionMatrix[row][column]
            if rowSum > 0:
                for column in range(cmDimension):
                    confusionMatrix[row][column] = round(confusionMatrix[row][column]/rowSum, 2)

        # Show confusion matrix after averaging row-wise
        plt.figure(figsize=(20, 15))
        ax = plt.subplot()
        sn.heatmap(confusionMatrix, annot=True, ax=ax)
        ax.set_xlabel('Predictions')
        ax.set_ylabel('True Values')
        ax.set_title('Confusion Matrix')
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"]
        saveInfo = saveFolderPath + "\\" + "_Averaged_" + models[selectedModel - 1] + "_CB" + str(
            codebookNum) + "_CWLength(" + str(
            len(codebook[0])) + ")" + "_Split(" + str(split) + ")" + ".png"
        plt.savefig(saveInfo, dpi=100)
        plt.show()
        plt.clf()

    def graphErrorOverTime(self, time, unknownDetectionError, knownDetectionError, knownClassificationError):
        '''
        Will graph the errors made over time for unknown detections, known detections, and known classifications.

        :param time: The number of data samples used in the experiment (each prediction represents a unit of time).
        :param unknownDetectionError: Cumulative errors for unknown detection.
        :param knownDetectionError: Cumulative errors for known detection
        :param knownClassificationError: Cumulative errors for known classification
        :return:
        '''
        fig, ax = plt.subplots()
        plt.xlabel("Time")
        plt.ylabel("Mean Error")

        # New Class Detection Error
        ax.plot(time, unknownDetectionError, color='red', linewidth=2, label="Unknown Detection Error")

        # Known Class Detection Error
        ax.plot(time, knownDetectionError, color='blue', linewidth=2, label="Known Class Detection Error")

        # Known Class Classification Error

        ax.plot(time, knownClassificationError, color='green', linewidth=2, label="Known Class Classification Error")

        plt.legend()
        plt.show()
        plt.clf()

# Contains methods that will probably only be used when working with incremental
# learning
class IncrementalLearningVisuals():

    def __init__(self):
        pass

    def graphCodewordFrequency(self, listOfCodewords, chosenCodeword, accuracy):
        '''
        Graphs the frequency of each codeword given in the list of codewords provided.

        This method is used for visualizing the number and frequency of codewords generated for
        data that the list of trained classifiers have never seen before.

        :param listOfCodewords: List of codewords generated using unknown/holdout data.
        :return: A histogram displaying the frequency of each codeword.
        '''
        #Convert list of lists (codewords) to list of strings
        stringCodewords = []
        for word in listOfCodewords:
            word = [str(bit) for bit in word]
            stringWord = ''.join(word)
            stringCodewords.append(stringWord)

        c = Counter(stringCodewords) # Used for making bar graph
        ax = plt.subplot(111)
        ax.bar(c.keys(), c.values(), ec='black')
        plt.setp(ax.get_xticklabels(), rotation=80, horizontalalignment='right', fontsize=6)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        word = [str(bit) for bit in chosenCodeword]
        chosenWordString = ''.join(word)

        ax.set_xlabel("Codeword")
        ax.set_ylabel("Frequency")
        ax.set_title("Codeword Frequency\nChosen Codeword: " + chosenWordString + "\nAccuracy: " + str(round(accuracy, 2)))
        plt.show()
        plt.clf()

    def graphCodewordFrequency_TopFive(self, listOfCodewords, chosenCodeword, accuracy):
        '''
        Graphs the frequency of the 5 most frequent codewords given in the list of codewords provided.

        This method is used for visualizing the number and frequency of codewords generated for
        data that the list of trained classifiers have never seen before.

        :param listOfCodewords: List of codewords generated using unknown/holdout data.
        :return: A histogram displaying the frequency of each codeword.
        '''
        #Convert list of lists (codewords) to list of strings
        stringCodewords = []
        for word in listOfCodewords:
            word = [str(bit) for bit in word]
            stringWord = ''.join(word)
            stringCodewords.append(stringWord)

        c = Counter(stringCodewords) # Used for making bar graph
        mostCommon = c.most_common(5)

        x_val = [x[0] for x in mostCommon]
        y_val = [x[1] for x in mostCommon]

        ax = plt.subplot(111)
        ax.bar(x_val, y_val, ec='black')
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize=15)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        word = [str(bit) for bit in chosenCodeword]
        chosenWordString = ''.join(word)

        ax.set_xlabel("Codeword")
        ax.set_ylabel("Frequency")
        ax.set_title("Top Five Most Frequent Codewords\nChosen Codeword: " + chosenWordString + "\nAccuracy: " + str(round(accuracy, 2)))
        plt.show()
        plt.clf()

    def graphBitFrequency(self, listOfCodewords, accuracy):
        '''
        Will create a histogram showing the frequency of 0's and 1's for each bit across multiple codewords.

        :param listOfCodewords: List of codewords generated using unknown/holdout data.
        :return: A histogram showing the frequency 0's and 1's for each index in a codeword
        '''
        ax = plt.subplot(111)
        numBits = len(listOfCodewords[0])
        barWidth = 0.20

        # Get lists containing frequencies of 1's and 0's in each index
        onesList = [0] * numBits
        zeroesList = [0] * numBits

        for codeword in listOfCodewords:
            index = 0
            for bit in codeword:
                if bit == 1:
                    onesList[index] += 1
                else:
                    zeroesList[index] += 1
                index += 1

        index = np.arange(numBits)
        ax.bar(index, zeroesList, barWidth, color='purple', label="0's")
        ax.bar(index + barWidth, onesList, barWidth, color='g', label="1's")
        ax.set_xticks(range(numBits))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("Codeword Index")
        ax.set_ylabel("Frequency")

        title = "Index Bit Frequency\nAccuracy: " + str(round(accuracy, 2))
        ax.set_title(title)

        # Setting up the legend
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        handles, labels = ax.get_legend_handles_labels()
        # For the line below, bbox_to_anchor manages where the legend will be located
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()
        plt.clf()

    def accuraciesPlot_ReinforcedVsInitial(self, initialCodewordAccuracies, reinforcedCodewordAccuracies, codeBook,
                                           knownTrain, allData, unknownData, knownSingleDataPoints, saveFolderPath,
                                           selectedModel, listOfSplits, codebookNum):
        '''
        Graphs the accuracies (for known/unknown predictions) for each split.

        :param knownAccMinDict: Dictionary with key = split and value = split's known accuracy (min across all holdouts)
        :param knownAccMaxDict: Dictionary with key = split and value = split's known accuracy (max across all holdouts)
        :param unknownAccMinDict: Dictionary with key = split and value = split's unknown accuracy (min across all holdouts)
        :param unknownAccMaxDict: Dictionary with key = split and value = split's unknown accuracy (max across all holdouts)
        :param initialCodewordAccuracies: Mean (across all holdouts) of the known prediction accuracies.
        :param reinforcedCodewordAccuracies: Mean (across all holdouts) of the unknown predictions accuracies.
        :param codeBook: Codebook being used.
        :param knownTrain: Data that was used for training the classifiers.
        :param allData: All of the data (regardless of the split it belongs to).
        :param unknownData: All data belonging to the unknown split.
        :param knownSingleDataPoints: The single samples of known data used to test the threshold.
        :param saveFolderPath: Path of the folder that will be used to save the figure.
        :param selectedModel: Model used to make the predictions.
        :param listOfSplits: All the splits used for testing.
        :param codebookNum: The number of the codebook you're currently on.
        :return: A figure showing the accuracies of known/unknown predictions across all desired splits.
        '''
        ax = plt.subplot(111)

        # Representation of the means.
        ax.plot(list(initialCodewordAccuracies.keys()), list(initialCodewordAccuracies.values()), marker='o', color='magenta',
                label='Initial Codeword', linestyle = '--')

        ax.plot(list(reinforcedCodewordAccuracies.keys()), list(reinforcedCodewordAccuracies.values()), marker='o', color='cyan',
                label='Reinforced Codeword', linestyle = '--')

        plt.xticks(listOfSplits)

        ax.set_title("Prediction Accuracy per Split")
        ax.set_xlabel("Percent Unknown")
        ax.set_ylabel("Accuracy")

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

        knownData = len(allData) - len(unknownData)
        percentTraining = round((len(knownTrain)/knownData), 2)
        models = ["SVM", "DT", "LDA", "KNN", "LogisticRegression", "NeuralNetwork", "NaiveBayes", "Random Forest"] # Corresponds to the number assigned for each classifier in Trainer.py
        # selectedModel has 1 subtracted from it because the models in the Trainer class are assigned with numbers
        # 1 - 4.
        saveInfo = saveFolderPath + "\\" + models[selectedModel - 1] +"_CB" + str(codebookNum) +"_CWLength(" + str(
            len(codeBook[0])) + ")" + "_UnknownHoldoutClasses1_KnownHoldoutSamples" \
            + str(len(knownSingleDataPoints))+ "_PercentTrainingData"+ str(percentTraining)  + ".png"

        plt.savefig(saveInfo, dpi = 300, bbox_extra_artists = (lgd,), bbox_inches = 'tight')
        plt.show()
        plt.clf()

    def graphErrorOverTime(self, timeOne, timeTwo, errorListOne, errorListTwo, splits, stdMasterListTwo, stdMasterListOne):
        fig, ax = plt.subplots()


        plt.xlabel("Time")
        plt.ylabel("Mean Cumulative Error")

        # For the Legend:
        # ax.plot(0,0, color='blue', label="Reinforcement Phase")
        # ax.plot(timeThree[0], errorListThree[0], color='green', label="Testing Phase")

        # 10%
        stdUpOne = [x1 + x2 for (x1, x2) in zip(errorListOne[0], stdMasterListOne[0])]
        stdDownOne = [x1 - x2 for (x1, x2) in zip(errorListOne[0], stdMasterListOne[0])]

        labelOneText_P1 = "" + str(int(splits[0]*100)) + "% Unknown"
        ax.plot(timeOne[0], errorListOne[0], color='green',label=labelOneText_P1 , linewidth=2) # Grouping with the Reinforcement Phase for now (can separate later).
        # plt.fill_between(timeOne[0], stdDownOne, stdUpOne, color='blue', alpha=0.3)
        # ax.plot(timeTwo[0], errorListTwo[0], color='blue', linewidth=2)

        ax.plot(timeTwo[0], errorListTwo[0], color='green', linewidth=2)

        stdUpTwo = [x1 + x2 for (x1, x2) in zip(errorListTwo[0], stdMasterListTwo[0])]
        stdDownTwo = [x1 - x2 for (x1, x2) in zip(errorListTwo[0], stdMasterListTwo[0])]

        # plt.fill_between(timeTwo[0], stdUpTwo, stdDownTwo, color='blue',
        #                  alpha=0.3)

        # 30%
        stdUpOne = [x1 + x2 for (x1, x2) in zip(errorListOne[1], stdMasterListOne[1])]
        stdDownOne = [x1 - x2 for (x1, x2) in zip(errorListOne[1], stdMasterListOne[1])]

        # plt.fill_between(timeOne[1], stdDownOne, stdUpOne, color='purple', alpha=0.30)
        labelTwoText_P1 = "" + str(int(splits[1]*100)) + "% Unknown"
        ax.plot(timeOne[1], errorListOne[1], 'k--' , color='green', label=labelTwoText_P1,
                linewidth=2)  # Grouping with the Reinforcement Phase for now (can separate later).

        # ax.plot(timeTwo[1], errorListTwo[1], 'k--' , color='blue', linewidth=2)
        stdUpTwo = [x1 + x2 for (x1, x2) in zip(errorListTwo[1], stdMasterListTwo[1])]
        stdDownTwo = [x1 - x2 for (x1, x2) in zip(errorListTwo[1], stdMasterListTwo[1])]
        # plt.fill_between(timeTwo[1], stdDownTwo, stdUpTwo, color='purple',
        #                  alpha=0.30)

        ax.plot(timeTwo[1], errorListTwo[1], 'k--', color='green', linewidth=2)

        # # # 50%
        stdUpOne = [x1 + x2 for (x1, x2) in zip(errorListOne[2], stdMasterListOne[2])]
        stdDownOne = [x1 - x2 for (x1, x2) in zip(errorListOne[2], stdMasterListOne[2])]

        # plt.fill_between(timeOne[2], stdDownOne, stdUpOne, color='red', alpha=0.30)
        labelThreeText_P1 = "" + str(int(splits[2]*100)) + "% Unknown"
        ax.plot(timeOne[2], errorListOne[2], ':' , color='green', label=labelThreeText_P1,
                linewidth=2)  # Grouping with the Reinforcement Phase for now (can separate later).

        # ax.plot(timeTwo[2], errorListTwo[2],':' , color='blue', linewidth=2)
        stdUpTwo = [x1 + x2 for (x1, x2) in zip(errorListTwo[2], stdMasterListTwo[2])]
        stdDownTwo = [x1 - x2 for (x1, x2) in zip(errorListTwo[2], stdMasterListTwo[2])]
        # plt.fill_between(timeTwo[2], stdDownTwo, stdUpTwo, color='red',
        #                  alpha=0.30)

        ax.plot(timeTwo[2], errorListTwo[2], ':', color='green', linewidth=2)



        # lims = [
        #     np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        #     np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        # ]
        # x = np.linspace(0, np.max(ax.get_xlim()), np.max(ax.get_ylim()))
        # y=0.5*x
        # ax.plot(x, y, 'k-.', color='black', alpha=0.50, label="50% Error")
        # ax.set_xlim(lims)
        # ax.set_ylim(lims)


        plt.legend(loc='upper left')
        plt.show()
        plt.clf()


    def graphErrorOverTime_ThreeAccuracies(self, time, newClassError, knownDetectionError, knownClassificationError):
            fig, ax = plt.subplots()
            plt.xlabel("Time")
            plt.ylabel("Mean Error")

            # New Class Detection Error
            ax.plot(time, newClassError, color='red', linewidth=2, label="New Class Detection Error")

            # Known Class Detection Error
            ax.plot(time, knownDetectionError, color='blue', linewidth=2, label="Known Class Detection Error")

            # Known Class Classification Error

            ax.plot(time, knownClassificationError, color='green', linewidth=2, label="Known Class Classification Error")

            plt.legend()
            plt.show()
            plt.clf()


