# Deep Learning with TensorFlow & Keras: http://nextgened.com/ds18/

## Tier 1 To do: 

1. look into __AskOski ML__ again:
	- https://drive.google.com/drive/folders/1iuzwHtryOW3QyTz1bw9HnbMC-ZVTIf7X
	- DKT with tensorflow: http://www.educationaldatamining.org/EDM2016/proceedings/paper_133.pdf 

1. Courses
	- Andrew Ng's course: https://www.coursera.org/learn/machine-learning?siteID=lVarvwc5BD0-COUZoGHjC2Z3A9.Vak.kFg&utm_campaign=lVarvwc5BD0&utm_content=2&utm_medium=partners&utm_source=linkshare
	-  look into more lazy programmer courses: 
	- https://deeplearningcourses.com/course_order#networkViewHeader

1. Watch calculus crashcourse: 
	- are all continuous functions differentiable?  are piecewise functions not continuous?  this doesn't imply not differentiable because converse doesn't necessarily have to be true
	- https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr
	- https://stackoverflow.com/questions/37953585/what-is-the-diffirence-between-sgd-and-back-propogation
	- review multivariable calculus

1. find your ML notes on the engineering paper

1. Siraj Ravel: "The Math of Intelligence" Playlist
https://www.youtube.com/watch?v=xRJCOz3AfYY&list=PL2-dafEMk2A7mu0bSksCGMJEmeddU_H4D
	- https://medium.com/@aerinykim/how-to-derive-chi-squared-pdf-from-normal-gaussian-c48d6d19b3d4

1. Comparing MSE and Var(Y) gives what information? 
- smaller MSE is better because that means the model captures a greater proportion of the variance
-  why is $$x / y > x^2 / y^2?$$   
- Prove: if $$p > q$$ then $$p^2 > q^2$$

1. What parts of 61A did you miss?
	- distributed data, databases & SQL, Declarative Programming & REPL, streams, promises, callbacks, REPL, interpreters, macros
	- https://inst.eecs.berkeley.edu/~cs61a/sp18/ 

1. look into functional programming
	- why is it different from multi-threading processing? 

1. Review Convolution in statistics: https://www.youtube.com/watch?v=yXwPUAIvFyg 
	- Can only do sums of random variables? - No, can do linear combinations
	- The convolution of probability distributions arises in probability theory and statistics as the operation in terms of probability distributions that corresponds to the addition of independent random variables and, by extension, to forming linear combinations of random variables. The operation here is a special case of convolution in the context of probability distributions.
	- Probability: https://stats.stackexchange.com/questions/2092/relationship-between-poisson-and-exponential-distribution 
	- https://stats.stackexchange.com/questions/33948/subsample-bootstrapping

## Tier 2

1. ML Model Cheatsheet: http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html 

1. Keras Cheatsheet: https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Keras_Cheat_Sheet_Python.pdf

1. RNNs --> Hidden Markov Models --> DBN (dynamic bayesian network) is a generalization of hidden Markov models and Kalman filters --> reinforcement learning --> dynamic programming --> mathematical optimization & computer programming
 
1. look into apache mahout: https://mahout.apache.org/ 
	- what is spark: https://www.qubole.com/blog/apache-spark-use-cases/ 
	- scalability, parallelizability, and production level

1. look into Pieter Abbeel: https://www2.eecs.berkeley.edu/Courses/CS188/ 
	- https://edge.edx.org/courses/course-v1:Berkeley+CS188+SP17/20021a0a32d14a31b087db8d4bb582fd/ 

1. Look into Caffe & BAIR: http://caffe.berkeleyvision.org/

1. https://www.quora.com/Why-cant-the-XOR-problem-be-solved-by-a-one-layer-perceptron 

1. https://www.quora.com/What-are-some-advantages-of-using-neural-networks-over-decision-trees

## Notes: 

1. Stability of a model can be approximated by stability of the validation score

1. you understand bias-variance tradeoff for estimators, how does it make sense for models? 

1. Backprop is calculating gradients for multiple layers of a neural net
	- SGD is one of many optimization methods, this one is based on analysis of the gradient of the objective: choosing weights that minimize the loss function
	- **https://stackoverflow.com/questions/37953585/what-is-the-diffirence-between-sgd-and-back-propogation**
	- Thus you have two layers of abstraction:

		gradient computation - where backprop comes to play

		optimization level - where techniques like SGD, Adam, etc. come into play, which (if they are first order or higher) use gradient computed above

	- once you find the proper weights, if some of them are zero is this closing down certain neurons in the networks

1. setting the random state produces the same **sequence** of numbers

1. One-hot encoding: https://towardsdatascience.com/the-dummys-guide-to-creating-dummy-variables-f21faddb1d40 
	- want to just label each factor as a numeric than categorical
	- don't use a hashcode because then you'd be capturing features of the word itself (ASCII code) not in the context of the data

1. KNN Regression vs Linear Regression
	- The reason why kNN is non-parametric is the model parameters actually grows with the training set, so linear regression is much more compact 
	- "kNN and similar models that retain a lot of data can be useful. But in today’s world of big data it can be impractical to work with a “model” that involves any large proportion of the full data set.

	It’s hard to move around, hard to search or calculate over, and in some sense it misses out on a key goal of AI: learning and abstracting patterns from the data in an elegant, performant way, for future use."
	- https://www.quora.com/Why-is-kNN-considered-a-nonparametric-method

	- Remark: for exponential distributions (e.g. Diamond prices histogram), if you do a log transform on the response variable, then fitting a linear model instead of a non linear model and then converting back might have some decent accuracy


### High Lvl Overview

- Reinforcement Learning combines different types of neural nets
- Generative networks are a spin on LSTMs
- Keras:
	- 30 second intro: https://keras.io/
- Deep Learning is where the GPU & parallelization comes in 
	- TensorFlowOnSpark offers parallel processing: https://github.com/yahoo/TensorFlowOnSpark 
- Note the distinction from producing a model to productionization of the that model 
	- apache Nifi
- Data Engineering vs Data Science? 
	- ETL: https://en.wikipedia.org/wiki/Extract,_transform,_load 
- Spark vs Scala? 
	- "When using Apache Spark for cluster computing, you'll need to choose your language. ... Apache Spark is a great choice for cluster computing and includes language APIs for Scala, Java, Python, and R"
- Functional vs Reactive Programming Paradigms
	- Spark (pythonic java) = Spark 
	- Spark not for neural nets usually
	- Markov Chain on Restricted Boltzmann Machine
- Web Notebooks: Jupyter vs Zeppelin
	- REPL (read, eval, print, loop)
	- for web notebooks, the loop part just goes to the next cell
	- Java has no REPL implementation (shell)
	- Can embed graphs & visualizations in the HTML
	- Remark: Angular & D3 are more fancy HTML embedders

## Training Logistical overhead:

1. how to open json files on zeppelin on your own local machine - not possible
	- Convert to jupyter notebooks?  Not possible, but should be bc .ipynb is just glorified json

- Your server cluster with 4 nodes: ec2-54-200-40-178.us-west-2.compute.amazonaws.com/ (ambari server) - different than your zeppelin server
- have to set the interpreter using %sh / %spark2.pyspark


ec2-34-219-12-139.us-west-2.compute.amazonaws.com	MatthewD
SJC331-DEL806-CV-DWS-109	AmbariNode	34.221.41.1		

http://ec2-...amazonaws.com:8080

Ambari Password:
admin
BadPass#1

Lower-left menu - Choose "Zeppelin Notebook", then the "Quick Links" menu in the center-top, then "Zeppelin UI"


Zeppelin Login:
admin
admin

"admin" menu in  upper right, then "Interpreter", then scroll down to "spark2"
"Edit" button are in upper-right hand corner of this section.
Edit key for "zeppelin.pyspark.python" from "python" to "python3.6"
"Save" button is on the bottom
Say "yes" to restart the Spark2 Interpreter


ssh admin@ec2-...amazonaws.com
Password is BadPass#1
pip3 uninstall --yes tensorflow-gpu


sudo yum install -y python36 python36-tools python36-devel python36-libs python34-pip

sudo yum install -y python34 python34-tools python34-devel python34-libs python34-pip


pip3 uninstall --yes tensorflow-gpu tensorflow
pip install --upgrade pip ; pip3 install tensorflow tensorboard numpy pandas matplotlib scikit-learn

https://www.quora.com/Why-cant-the-XOR-problem-be-solved-by-a-one-layer-perceptron


Download Diamonds Data

%sh
curl -O http://nextgened.com/ds18/data/diamonds.csv

%sh
mkdir -p data
mv diamonds.csv data

### Command to connect because bc of version issue 

- what is the -i doing? 
`ssh -i ./training-keypair.pem centos@ec2-34-215-140-3.us-west-2.compute.amazonaws.com`