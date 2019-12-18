# AWS MNIST Web App

In this project, we will deploy a web application and a web server to read manually drawn digits. Calibration of the model is done on the MNIST dataset.

## Expected Output

From your web browser, you will be able to draw a digit on a canvas and get the model to predict the output as shown on the picture below.

![Alt](https://github.com/fredericferriere/AWS_MNIST_webApp/webpage2.png)


## AWS Architecture

A public instance to calibrate the model, ie train a CNN on the MNIST dataset.  
A public instance hosting our web server.  
A public instance hosting our web application (based on the Flask framework).

## Steps we will follow

1- Calibrate the model: we'll use a Jupyter notebook (mnistCalib.ipynb). Code requires different libraries, so we'll install Anaconda on top of Jupyter so we can create a virtual environment.
Output of this step will be a keras file (cnn-mnist) with model specification (CNN architecture + model weights).  

2- Run a web app (Flask framework) that listens to our web server requests, takes the canvas image as input and uses our model (cnn-mnist) to determine which digit was drawn in the canvas. We'll also need to install some Python libraries so the model can run.

3- Run a web server (Apache) that will serve our html document (a canvas to draw a digit + a box to see the result of the model prediction). The webserver calls a Flask App sitting on a different machine.  

## Model Calibration

Instance Type: Ubuntu Server 18.04  
Instance Name: mnistCalibration  
We'll install Jupyter and Anaconda to create a virtual environment containing all the required libraries for our model (keras, tensorflow), so make sure to include enough storage when creating your instance (20GB)
Also, you can initially create a micro instance to do all the required installations. We'll switch to a more performant machine just before running the calibration.

For a more detailed description of how to install Jupyter and create virtual environments, please refer to my following github repository: Ubuntu_Jupyter_and_Virtual_Environments  

We'll calibrate the model with code sitting in a jupyter notebook

Once connected to the instance:  
$ sudo apt update -y  
$ python --version

Please make sure your Python version is 3.6+ (in our setup, version used is 3.6.8). Just run sudo pip install Python3 if your Python version is not compatible.

We need to install pip, then Jupyter, then Anaconda  
$ sudo apt install python-pip  
$ sudo pip install Jupyter  

To install Anaconda:  
$wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh  
$sudo bash Anaconda3-2019.03-Linux-x86_64.sh

Next we'll create a virtual environment called mnistCalib.
$conda create --name=mnistCalib python=3.6

Note: If you get an error message "Conda command not found", just run the following command and you should be ok.
$export PATH=~/anaconda3/bin:$PATH

$conda activate mnistCalib
$conda install ipykernel
$ipython kernel install --user --name=mnistCalib

$pip install keras
$pip install tensorflow

Note: all packages are listed in mnistCalib_pipfreeze.txt, so you can run:  
$sudo pip install -r mnistCalib_pipfreeze.txt  
and all packages should be installed.

We're now ready to proceed with model calibration. The training is based on 60,000 images and testing is performed on 10,000 images. It's time to upgrade to a more performant machine.  
Recommended instance type: m5.xlarge (app 0.20 USD/hour)
Just stop your instance, upgrade and restart your instance. You're now good to proceed to the last steps.

$jupyter notebook --ip=0.0.0.0

Just copy/paste the provided URL/token to access your remote Jupyter.

From Remote Jupyter:  
Upload the file mnistCalib.ipynb  
Open this file with the mnistCalib ipykernel

Just run all the cells. This will save a file cnn-mnist in the current directory, which our web app will consume to determine which digit was drawn by the user. We'll need to upload this file to the web app instance, so you might want to save a copy locally.


## Web App

Instance type: Ubuntu Server 18.04 (t2.micro type should be enough).  
Instance Name: webApp

Copy the files flaskDigitReader.py and cnn-mnist to the remote instance.

Once connected to the instance, and after making sure you have python 3.6 installed, we'll need to install several packages.

$sudo apt update -y  
$sudo apt install python-pip  
$pip install keras  
$pip install --no-cache-dir tensorflow  
$pip install pillow  
$pip install flask  

We can now run the webapp:  
$python flaskDigitReader.py

## Web Server

Instance type: Linux2 AMI(t2.micro type ok)
Instance Name: webServer.  
Correct the file index.html and change the local IP 127.0.0.1 with the public IP of the Web App.  
Copy files index.html and the 'static' folder containing files index.hs and style.css

$sudo yum update -y  
$sudo yum -y install httpd php  
$sudo chkconfig httpd on  

we can now start the server  
$sudo service httpd start


## Results

Just enter the public IP of you web server in a browser. This will take you to index.html, which allows you to draw a digit inside a canvas.  
Just click predict and the result will be displayed.

![](./webpage2.png)


## Next steps

Host the web app on a private instance. This may require setting up a second Flask application on the web server.
