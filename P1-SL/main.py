import warnings

import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn import neighbors
import matplotlib
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import validation_curve
from datetime import datetime

# show popup for graphs on mac

matplotlib.use("TKAgg")

import matplotlib.pyplot as plt

DATASET_1 = "data/wine.csv"
DATASET_2 = "data/winequality.csv"
DATASET_1_NAME = "Wine"
DATASET_2_NAME = "Wine Quality"


def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate 3 plots: the test and training learning curve, the training
    samples vs fit times curve, the fit times vs score curve.

    Parameters
    ----------
    estimator : estimator instance
        An estimator instance implementing `fit` and `predict` methods which
        will be cloned for each validation.

    title : str
        Title for the chart.

    X : array-like of shape (n_samples, n_features)
        Training vector, where ``n_samples`` is the number of samples and
        ``n_features`` is the number of features.

    y : array-like of shape (n_samples) or (n_samples, n_features)
        Target relative to ``X`` for classification or regression;
        None for unsupervised learning.

    axes : array-like of shape (3,), default=None
        Axes to use for plotting the curves.

    ylim : tuple of shape (2,), default=None
        Defines minimum and maximum y-values plotted, e.g. (ymin, ymax).

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

          - None, to use the default 5-fold cross-validation,
          - integer, to specify the number of folds.
          - :term:`CV splitter`,
          - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : int or None, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    train_sizes : array-like of shape (n_ticks,)
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the ``dtype`` is float, it is regarded
        as a fraction of the maximum size of the training set (that is
        determined by the selected validation method), i.e. it has to be within
        (0, 1]. Otherwise it is interpreted as absolute sizes of the training
        sets. Note that for classification the number of samples usually have
        to be big enough to contain at least one sample from each class.
        (default: np.linspace(0.1, 1.0, 5))
    """
    if axes is None:
        _, axes = plt.subplots(1, 3, figsize=(20, 5))

    plt.title(title)

    axes[0].set_title("Learning Curve")
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                       train_sizes=train_sizes,
                       return_times=True)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, 'o-')
    axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                         fit_times_mean + fit_times_std, alpha=0.1)
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    # Plot fit_time vs score
    axes[2].grid()
    axes[2].plot(fit_times_mean, test_scores_mean, 'o-')
    axes[2].fill_between(fit_times_mean, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1)
    axes[2].set_xlabel("fit_times")
    axes[2].set_ylabel("Score")
    axes[2].set_title("Performance of the model")


def plot_validation_curve(estimator, title, X, y, x_lab, y_lab, param_name, param_range,
                          ylim=None, cv=None, n_jobs=None):

    plt.figure()
    plt.title(title)

    if ylim is not None:
        plt.ylim(*ylim)

    # param_range = np.logspace(-6, -1, 5)
    train_scores, test_scores = validation_curve(
        estimator, X, y, param_name=param_name, param_range=param_range,
        scoring="accuracy", n_jobs=n_jobs, cv=cv)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    lw = 2

    # special case for ann passing tuples for hidden layer sizes
    if type(param_range[0]) is list or type(param_range[0]) is tuple:
        param_range = [r[0] for r in param_range]

    plt.plot(param_range, train_scores_mean, label="Training score",
                 color="darkorange", lw=lw)
    plt.fill_between(param_range, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color="darkorange", lw=lw)
    plt.plot(param_range, test_scores_mean, label="Cross-validation score",
                 color="navy", lw=lw)
    plt.fill_between(param_range, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.2,
                     color="navy", lw=lw)
    plt.legend(loc="best")


def run_dtc_1(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_1, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = DecisionTreeClassifier(criterion="entropy", random_state=0)

    # TODO run cost complexity pruning code to find alpha for ccp

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        "max_depth": [3, 5, 10, 12, 15, 20],
        "min_samples_split": [2, 5, 10],
        # ccp alpha for pruning as opposed to max depth, post vs pre pruning
    }

    basic = DecisionTreeClassifier(criterion="entropy", random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (Decision tree) ({DATASET_1_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with DT ({DATASET_1_NAME})"
    x_lab = "Depth"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="max_depth", param_range=range(1, 20), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_dtc_2(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_2, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = DecisionTreeClassifier(criterion="entropy", random_state=0)

    # TODO run cost complexity pruning code to find alpha for ccp

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        "max_depth": [3, 5, 10, 12, 15, 20],
        "min_samples_split": [2, 3, 4],
        # ccp alpha for pruning as opposed to max depth, post vs pre pruning
    }

    basic = DecisionTreeClassifier(criterion="entropy", random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=3, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (Decision tree) ({DATASET_2_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0.0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")

    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with DT ({DATASET_2_NAME})"
    x_lab = "Depth"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="max_depth", param_range=range(1, 20), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_ada_1(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_1, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = AdaBoostClassifier(n_estimators=300, random_state=0)
    clf = AdaBoostClassifier(random_state=0)

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # depth of decision classifier? or just optimize number of depth 1 stumps?
        # learning rate
        # "n_estimators": range(10,500, 10)
    }

    basic = AdaBoostClassifier(random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, resource='n_estimators', max_resources=500, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (Boosted Decision tree) ({DATASET_1_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with Boosted DT ({DATASET_1_NAME})"
    x_lab = "n_estimators"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="n_estimators", param_range=range(10, 500, 10), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_ada_2(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_2, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = AdaBoostClassifier(n_estimators=300, random_state=0)
    clf = AdaBoostClassifier(random_state=0)

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # depth of decision classifier? or just optimize number of depth 1 stumps?
        # learning rate
        # "n_estimators": range(10,500,10)
    }

    basic = AdaBoostClassifier(random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, resource='n_estimators', max_resources=500, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (Boosted Decision tree) ({DATASET_2_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with Boosted DT ({DATASET_2_NAME})"
    x_lab = "n_estimators"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="n_estimators", param_range=range(10, 500,10), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_svm_1(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_1, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = SVC(random_state=0)

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # at least kernels
        # C?
        # gamma?
        # "kernel": ["linear", "poly", "rbf", "sigmoid", "precomputed"]
    }

    basic = SVC(random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (SVM) ({DATASET_1_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")

    # validation curve won't really work here, just use a table
    for kernel in ["linear", "poly", "rbf", "sigmoid", "precomputed"]:
        # train svc with given kernel
        # cv sets to get average per kernel
        # dump results for table
        pass

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_svm_2(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_2, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = SVC(random_state=0)

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # at least kernels
        # C?
        # gamma?
    }

    basic = SVC(random_state=0).fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (SVM) ({DATASET_2_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # validation curve isn't helpful here, pull table code once svm1 is done

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_knn_1(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_1, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = neighbors.KNeighborsClassifier()

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # neighbors (k)
        # "n_neighbors": range(1,len(data_train), 5),
        # weights (uniform, distance)
        "weights": ["uniform", "distance"],
        # p (1 = manhattan, 2 = euclidian)
        "p": [1,2]
    }

    basic = neighbors.KNeighborsClassifier().fit(data_train, label_train)

    # 4 of the 5 folds use to train
    max_neigh = int(len(data_train)*0.8)

    sh = HalvingGridSearchCV(clf, param_grid, resource="n_neighbors", max_resources=max_neigh, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (KNN) ({DATASET_1_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with KNN ({DATASET_1_NAME})"
    x_lab = "Neighbors"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="n_neighbors", param_range=range(1, max_neigh), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_knn_2(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_2, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = neighbors.KNeighborsClassifier()

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # neighbors (k)
        # "n_neighbors": range(1, len(data_train), 5),
        # weights (uniform, distance)
        "weights": ["uniform", "distance"],
        # p (1 = manhattan, 2 = euclidian)
        "p": [1, 2]
    }

    basic = neighbors.KNeighborsClassifier().fit(data_train, label_train)

    # 4 of the 5 folds use to train
    max_neigh = int(len(data_train)*0.8)

    sh = HalvingGridSearchCV(clf, param_grid, resource="n_neighbors",max_resources=max_neigh, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (KNN) ({DATASET_2_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with KNN ({DATASET_2_NAME})"
    x_lab = "Neighbors"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="n_neighbors", param_range=range(1, max_neigh,5), ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_ann_1(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_1, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                        solver='sgd', verbose=10, random_state=0,
                        learning_rate_init=.1)
    clf = MLPClassifier(random_state=0)

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # hidden layers?
        "hidden_layer_sizes": [(i,) for i in range(5,50,5)]
        # alpha
        # learning rate
        # momentum
        # solver
    }

    basic = MLPClassifier().fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (ANN) ({DATASET_1_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with ANN ({DATASET_1_NAME})"
    x_lab = "hidden_layer_sizes"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="hidden_layer_sizes", param_range=[(i,) for i in range(5,50,5)], ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


def run_ann_2(fig_name = None, show_plots = False):
    # read in dataset from file
    with open(DATASET_2, 'r') as f:
        data = np.genfromtxt(f, delimiter=',')

    data, labels = data[:,:-1], data[:,-1]

    # split for training and testing
    data_train,data_test, label_train, label_test = train_test_split(
        data, labels, test_size=0.4, random_state=0, stratify=labels
    )

    # define model
    # fix hyperparameters as needed to avoid unneeded grid search
    clf = MLPClassifier(hidden_layer_sizes=(50,), max_iter=10, alpha=1e-4,
                        solver='sgd', verbose=10, random_state=0,
                        learning_rate_init=.1)
    clf = MLPClassifier(random_state=0)

    # pulled from sklearn plot mnist example
    # this example won't converge because of CI's time constraints, so we catch the
    # warning and are ignore it here
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning,
                                module="sklearn")

    # based off sklearn example for hp tuning
    # https://scikit-learn.org/stable/modules/grid_search.html#

    # define hyper parameter space to check over
    param_grid = {
        # hidden layers?
        "hidden_layer_sizes": [(i,) for i in range(5,50,5)]
        # alpha
        # learning rate
        # momentum
        # solver
    }

    basic = MLPClassifier().fit(data_train, label_train)

    sh = HalvingGridSearchCV(clf, param_grid, cv=5, factor=2).fit(data_train, label_train)
    print(sh.best_estimator_)
    # clf = sh.best_estimator_

    # based on sklearn learning curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    # plot learning curve for current model
    title = f"Learning Curves (ANN) ({DATASET_2_NAME})"
    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

    plot_learning_curve(clf, title, data_train, label_train, ylim=(0, 1.01),
                        cv=cv, n_jobs=4)

    if fig_name is not None:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        plt.savefig(f"{fig_name}_learn_{dt_string}")


    # based off sklearn validation curve example
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_validation_curve.html

    # plot validation curve
    title = f"Validation Curve with ANN ({DATASET_2_NAME})"
    x_lab = "hidden_layer_sizes"
    y_lab = "Score"

    plot_validation_curve(clf, title, data_train, label_train, x_lab, y_lab,
                          param_name="hidden_layer_sizes", param_range=[(i,) for i in range(5,50,5)], ylim=(0.0, 1.1))

    if fig_name is not None:
        plt.savefig(f"{fig_name}_val_{dt_string}")

    if show_plots:
        plt.show()

    plt.close('all')

    # run against test, uncomment for final analysis
    # !! don't touch during training/tuning !!
    # print(clf.score(data_test, label_test))

    # track accuracy and variance so later report can pull numbers as needed


if __name__ == '__main__':
    # dataset 1
    # run_dtc_1("charts/dtc_1_notune")
    # run_ada_1("charts/ada_1_notune")
    # run_svm_1("charts/svm_1_notune")
    # run_knn_1("charts/knn_1_notune")

    # pulled from sklearn plot mnist example
    # this example won't converge because of CI's time constraints, so we catch the
    # warning and are ignore it here
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning,
                                module="sklearn")
        run_ann_1("charts/ann_1_notune")

    # dataset 2
    run_dtc_2("charts/dtc_2_notune")
    run_ada_2("charts/ada_2_notune")
    run_svm_2("charts/svm_2_notune")
    run_knn_2("charts/knn_2_notune")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning,
                                module="sklearn")
        run_ann_2("charts/ann_2_notune")