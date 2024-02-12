# BackendAppTest

This is the final version of a back-end application ready for its use. It has an API-Rest, JWT (Json Web Tokens), a DB (you´ll need to download SQLite3). Also, for testing you can use the application 
'Insomnia' to test all the methods: POST, PUT, GET, DELETE.

FIRST STEPS INSTRUCTIONS

Please NOTE the next first steps to start using this app:
First you need to create a folder where you will hold this application. After this you need to create the virtual environment. You will need to go to the 'cmd' (windows + r and type 'cmd'). After this, go to the location of the application and use the command 'python -m venv .'
Then go to the folder 'Scripts' (cd Scripts), this folder will be create once you create the virtual environment. Here you will active the virtual environment with the command: 'activate.bat'
Once this has been done we can go back (cd ..) and install the required libraries that come in the script 'requirements.txt', for this we will use the following command: 
'pip install -r requirements.txt' please NOTE that the libraries already come with the needed version. Further versions had not worked, you could try using further versions but they might 
bring issues to the application, in the meantime you can start testing the app with these versions. 
Moving forward, we need to create the document '.env', this repository has an example with the required variables that you can copy and paste, or just change its name. 
Lastly, you will need to execute or run the application, by using the following command 'python app.py'. 
Please NOTE that for running the app, you will need to have the virtual environment activated, in case you close all the windows or shut the computer, you can activate the virtual environment
again by going againg to the document 'Scripts' and this time using 'activate', once you confirm the enviroment has been activated you can go back (cd ..) and run the app with 'python app.py'
