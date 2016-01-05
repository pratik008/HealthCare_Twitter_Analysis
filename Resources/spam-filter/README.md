tweetclass
==========
This repository provides a self-contained environment and instructions for training a Bag of Words (+ soon Tweet metadata like No. followers, No. friends, etc.) tweet classifier.  This is an in-development prototype and we are still optimizing the algorithm in enhance performance.  Briefly, a large volume of twitter data is labeled accoding to user-input judgements of the derived *topics* in the data, which are generated using the Topic Modeling algorithm.  These assigned labels are then combined with PCA-reduced Bag-of-Words features for the training process (currently using gradient boosted regression trees).  New tweets would then to classified by applying the trained mode to new Bag of Words features.

The "Classes" of the classification are arbitrary, and are only based on the judgement of the user's input during the topic modeling stage.  Therefore the pipeline is general purpose and adaptable.  Example classes might be spam/not spam or doctor/patient.



Robert Lindner

Didier Dominguez

Jing Mao


Dependencies
--------------
1. Python 2.7
2. Numpy
3. Scikit-learn
4. mallet (http://mallet.cs.umass.edu/)
5. Bob's Classification Benchmarker:
```
git clone git@github.com/rlml/ml.git
```
6. Didier's Bag-of-Words parser 
```
git clone git@github.com/ddrbcn/tweetsfeatures.git
```

Installation
------------
Obtain the repo
```
$ git clone git@github.com:rlml/tweetclass.git
```
Install by adding the following line to
your .bashrc or equivalent:
```
export PATH=/path/to/tweetclass/:$PATH
```



Section I. Label the training data
---------------------------------------

1.) Obtain JSON training data.

E.g., run "my_twitterstream.py" or use
George Fisher's script to download JSON data.
Let's call it "data.json".


2.)
```
$ dump_tweet_text data.json
```

This will dump all tweet messages text into a 
folder named "tweet_text" containing separate 
files for all valid tweets.  The file names 
are "tweet_{ID}.txt", where {ID} is the tweet ID.
The program will also make a file called:
"all_tweets.txt" which lists all IDs and text
messages in a single file for easy data viewing.


3.)
```
$ mallet_load_data
```

This will read the tweets from directory **tweet_text**
into the mallet data format.
It expects to find the directory **tweet_text**.
If will create the file **tweet.mallet**, which is the tweet messages
transformed into the Mallet format.

4.) 
```
$ mallet_topic_model
```
This will run latent dirichlet topic modelling on
the tweet messages assuming 100 topics.
Takes ~15 minutes for  ~100k tweets.  The outputs are:
**doc_topics.txt** and **topic_keys.txt**

5.) Manually classify the topics

Edit the **topic_keys.txt** file.
Include a new "0th" column indicating the class as: 0  or 1.
Save the new file as **topic_keys_labels.txt**.
This is the important step where the nature of the
classes is implicitly determined by your choices.


6.) 
```
$ label_tweets
```
This will label all tweets in the training set.
It expects to find the two files: **doc_topics.txt**
and **topic_keys_labeled.txt**.

It creates **ids_and_labels**, the file indicating the 
class of all tweet ids (except those few which could
not be parsed by JSON; see revisions). The format will be:

       ID_0, [label_0] 
       ID_1, [label_1] 
        ...       ...   
       ID_N, [label_N] 





Section II. Extract features from training data
-----------------------------------------------
1.)  
```
$ gen_features data.json
```

This is produce dimensionally reduced 
Bag-of-Words features from the JSON data.
File will be produced: **ids_and_features.csv** 
with format

       ID_0, [features_0...] 
       ID_1, [features_1...] 
       ...              ...  
       ID_N, [features_N...] 



Section III. Generate training data
------------------------------------

1.)
```
$ gen_training_data
```

(Requires: **ids_and_features.csv** and **ids_and_labels.csv**; see above)

This will find the common IDs between the features and the
labels and produce pure numerical representations of the
design matrix X and target vector Y for training.

This step in required because the features and labels
are as of yet as necessarily in the same order, or even
have the same number of rows (see "revisions" # 4).

Files created: **X** and **Y**
I.e., design matrix and target vector


Section IV. Train the classifier model
--------------------------------------

1.) 
```
$ bench [paramfile] [X] [Y]
```

This will train a Gradient Boosted Decision Tree Classifier
(scikit-learn) on the X, Y data using the hyperparameter 
list set in the "paramfile".  To create the paramfile, make a 
CSV file with each of the hyperparameters of the model that 
you wish to be non-default, refer to documentation here:

     http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html

The example contents of a simple paramfile to scan over
five values of the the learning_rate hyperparameter 
would look like this:

      learning_rate,n_estimators,max_depth,n_folds
      0.1,100,4,2                                   
      0.2,100,4,2                                   
      0.3,100,4,2                                   
      0.4,100,4,2                                   
      0.5,100,4,2

After completion, a new paramfile is created with additional
columns describing the peformance of each model.
The file name is a time stamp.  

To make a plot of the F1 score for the training data and
cross validation data as a function of learning_rate, Run:

```
$ plot [new param file] learning_rate F1-train F1-cv
```
       (figure is displayed)






Revisions to make:
--------------------
1. Allow user to keep a trained model for use later

2.  Consider how to handle these characters during
   topic modeling:
    "@", "#", "\n", numbers

3.   Keep "#" character in the tweet text, 
    will help with identifying hashtags?

4.   Mallet is removing NUMBERS, leaving the letter fragments from URLS.
    Just remove everything after an "http"?

5.  Very rarely (about 1 out of 100,000 tweets) a JSON
   record is unable to be parsed by json.loads().
   Currently, the exception is caught and the tweet is ignored
   which is why the output file may have fewer lines than the
   original json file.  Correct this at some point...

6. Add meta-data features?

7. Use "conversations" instead of single tweets in topic modeling (E.g., see previous contributions by David Millis)
