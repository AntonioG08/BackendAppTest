from main import create_app, db
import os

"""PLEASE NOTE: once we run the app with 'python app.py' we can kill the server with CTRL + C """

"""We create the app in this script 'the main script' using the function we created in the script '__init__.py' and the 
   reason why we dont create the app here entirely is due to flask problems (investigate more about this)"""
app = create_app()


"""We use this method to be able to access to all the flask functions without having the need to call flask every time"""
app.app_context().push()

"""This is the flask sintaxis (investigate more about this)"""
if __name__ == '__main__':
   
    """With this we are requesting the program to create all the tables in the DataBase in case they dont exist already"""
    db.create_all()
    
    """For us to be able to run the app, we need to provide a port number, which we´ve done in the script '.env'
       also, the 'debug=True' means that we will be able to have a quick refresh in any change in the project without
       the need to stop and rerun the app"""
    app.run(port=os.getenv("PORT"), debug=True)
