# from myDropboxFunctions import put, get, view, newuser, login, create_folder, share
# from helloMydropbox import welcome
import base64
import requests
import os

def welcome():
    return """Welcome to myDropbox Application
======================================================
Please input command (newuser username password password, login
username password, put filename, get filename, view, or logout).
If you want to quit the program just type quit.
======================================================"""

def put(argument, username):
    """Upload files to mydropbox app storage.
    
    Put function receive two arguments that is filename(argument in function) & username. 
    First, start by loop over list of filename to iterate over each file. 
    For each file was encode by using base64.b64encode Python library and encode to string format 
    with encode_file.decode('utf-8'). And sent request to API gateway with requests.post with json format. 
    After that Lambda function will encode binary string and upload to S3 bucket.

    Args:
        argument (list of string): List of files you want to upload.
        username (string): your username ex.test@hotmail.com
    """
    upload_url = "https://wxlob71yg1.execute-api.us-west-2.amazonaws.com/default/upload"
    file_name = argument[0]
    print("Uploading {}".format(file_name))
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            encode_file = base64.b64encode(f.read())
            encode_string = encode_file.decode('utf-8')
            json_file = {"content":encode_string, "username":username}
            response = requests.post(upload_url, json=json_file, headers={"file-name":"{}".format(file_name)})
            if response.ok:
                print("Upload completed successfully!")
                print(response.text)
            else:
                print("Something went wrong!")
    else:
        print("{} is not exists in {}".format(file_name, os.getcwd()))
    return 0 

def get(username, filename, owner):
    """Download file to your local computer.
    
    Get function receive 3 arguments that are filename, username and owner. 
    And using requests.pot Python library to request post Lambda function with api gateway(download_url variable). 
    Then Lambda function call get_object from Amazon S3 with boto3 library from username/file path. 
    And encode the object to binary string with base64.b64encode python library. 
    After that decode the binary string with base64.b64decode and write to local computer.

    Args:
        argument (list of string): List of your files you want to download from your mydropboxx app storage.
        username (string): your username Ex. test@hotmail.com
        owner (string)

    """
    download_url = " https://x8f28qdsuf.execute-api.us-west-2.amazonaws.com/default/download"
    print("Downloading {}".format(filename))
    response = requests.post(download_url, json={"username": username, "filename": filename, "owner": owner}, headers={'Accept': 'application/json'})
    if response.ok:
        content = base64.b64decode(response.content)
        result =open(filename, 'wb')
        result.write(content)
        print("Download completed successfully!")
    else:
        print("Something went wrong!")
    return 0

def view(username):
    """View function receive 1 argument that is `username` and parsing to `requests.post` from
    request Python module with lambda api gateway http endpoint(`view_url` variable). 
    Loop over response JSON format(Python dictionary) name `res` and print out using python fstring.
    Moreover shared files are included in this function.
    Args:
        username (string): your username Ex. test@hotmail.com

    """
    view_url = "https://18ktp7k6oj.execute-api.us-west-2.amazonaws.com/default/view"
    response = requests.post(view_url, json={'username':username}  ,headers={'Accept': 'application/json'})
    res = response.json()
    if response.ok:
        if res:
            for key, value in res.items():
                name = str(value['key'])
                size = str(value['size'])
                date = str(value['date'])
                object_owner = str(value['object-owner'])
                print("{} {} {} {}".format(name, size, date, object_owner))  
        else:
            print("There is nothing in your storage")
    else:
        print("Something went")
    return 0

def newuser(username, password):
    #Check that username is not existing in myDropboxUser Table
    newuser_url = "https://18ktp7k6oj.execute-api.us-west-2.amazonaws.com/default/newuser"
    response = requests.post(newuser_url, json={"username": username, "password": password}, headers={'Accept': 'application/json'})
    response_json = response.json()
    if response_json["keynotexist"]:
        print("{} has beed created !".format(username))
        return True
    else:
        print("{} has been taken already!".format(username))        
        return False

def login(username, password):
    """Login to you account that you created with you username and password.
    
    This function receive "username" and "password" as string and sent through api to Lambda function.
    In the Lambda function we call DynamoDB to check that "username" and "password" are match or not.
    And then return result to user.

    Args:
        username (string): Your account username ex. user1@hotmail.com
        password (string): Your account password ex. 12Kvw31t!@#

    Returns:
        boolean
    """
    login_url = "https://18ktp7k6oj.execute-api.us-west-2.amazonaws.com/default/login"
    response = requests.post(login_url, json={"username": username, "password": password}, headers={'Accept': 'application/json'})
    response_json = response.json()
    if response_json["loginstatus"]:
        print("Login sucessful")
        return True
    else:
        print("You have entered an invalid username or password!")
        return False

def create_folder(username):
    """Create folder in S3 bucket with username
    
    Once you successful create your account, It will automatically execute this function.
    When this function was executed, Lambda function will connect to S3 bucket and create the folder with
    your input "username" to prevent duplicate object name.
    

    Args:
        username (string): your username ex. user1@hotmail.com
    """
    createfolder_url = "https://wxlob71yg1.execute-api.us-west-2.amazonaws.com/default/createfolder"
    response = requests.post(createfolder_url, json={'username': username})
    print("{} sign up successful!".format(response.text[1:-1]))
    
    
def share(username, file_name, shareduser):
    """Share your file to another user.
    
    This function call Lambda function by sending post request to connect dynamodb.
    DynamoDB collect data by using shared user as primary key and file_id(ex. username/file_name)
    as sort key. And another neccessary attributes are file name and file owner.
    

    Args:
        username (string): Your username
        file_name (string): Your filename that would like to share with
        shareduser (string): Username you would like to share with
    """
    share_url = "https://18ktp7k6oj.execute-api.us-west-2.amazonaws.com/default/sharefile"
    response = requests.post(share_url, json={'shared_user': shareduser, 'file_id': username + "/" + file_name, 'file_name': file_name, 'file_owner': username})
    print(response.text)

 ## define login variable for allow only newuser and login function
loggedIn = False

if __name__ == "__main__":
    print(welcome())
    while(True):
        userinput_sep = input(">>").strip().split() ## assign function & argument variables
        if len(userinput_sep) > 1:
            function = userinput_sep[0]
            argument = userinput_sep[1:]
            argument = list(argument) ## prevent one argument know as string
        elif len(userinput_sep) == 1: 
            function = userinput_sep[0]
        else:
            print("Please enter existing keyword")
            continue
        
        ## if user are not loggin yet, just allow only 3 commands (login, newuser and quit)
        if not loggedIn:
            ## call newuser function from myDropboxFunctions 
            if function == "newuser":
                if len(argument) == 3: #check that function got right arguement ex. ['guyrawit@hotmail.com', 'password', '12345678']
                    if argument[1] == "password": # if second argument is not "password", return commands not found
                        if newuser(argument[0], argument[2]): #call newuser function if create successful then return True else return False
                            create_folder(argument[0]) #call create_folder function to create folder in S3 bucket by using username as directory name
                        else:
                            print("signup failed")
                    else:
                        "Commands not found"
                else:
                    print("Please enter exist keyword and right order argument!")
            
            ## login username guyrawit@hotmail.com 12345678
            elif function == "login":
                if len(argument) == 2: #check that after login have only 2 argument that are username and password
                    username, password = argument[0], argument[1] # assign username and password
                    loggedIn = login(username, password) # call login function if login successful return True and assgin to loggedIn variable (change status to logged in)
                else:
                    print("No argument")
            ## quit the app so just break the while loop        
            elif function == "quit":
                print("="*55)
                break
            ## if you enter another commands just print "please login"
            else:
                print("please login first!")
                
        # If loggedIn change to True so that allow you to call another commands  
        else: 
            ## Eventhough you are logging in, you can call newuser function also.
            ## call newuser function from myDropboxFunctions
            if function == "newuser":
                if len(argument) == 3: #check that function got right arguement ex. ['guyrawit@hotmail.com', 'password', '12345678']
                    if argument[1] == "password": # if second argument is not "password", return commands not found
                        if newuser(argument[0], argument[2]): #call newuser function if create successful then return True else return False
                            create_folder(argument[0]) #call create_folder function to create folder in S3 bucket by using username as directory name
                        else:
                            print("signup failed")
                    else:
                        "Commands not found"
                else:
                    print("Please enter exist keyword and right order argument!")
            
            ## put the following file to your cloud storage
            elif function == "put":
                if len(argument) == 1: 
                    put(argument, username) # call put function and function will print out that what happend (ex. no file exists, file has been uploaded)
                else:
                    print("No argument")
            
            #download the follow file from your cloud storage with owner argument. 
            elif function == "get":
                if len(argument) == 2:
                    filename, owner = argument[0], argument[1]
                    get(username, filename, owner)
                elif len(argument) == 1: ## If you do not enter owner, it default is you. by assing "owner = username"
                    filename, owner = argument[0], username
                    get(username, filename, owner)
                else:
                    print("Please enter valid argument")
            
            #call view function
            elif function == "view":
                view(username)
            
            elif function == "logout":
                username, password = "", "" # clear the username and password variable to empty string
                loggedIn = False #change login status to False
            
            elif function == "quit":
                print("="*55)
                break
            
            elif function == "share":
                if len(argument) == 2: #if got right argument then call share function
                    share(username, argument[0], argument[1]) #share function will check that file and user are existing or not then print out what happended
                else:
                    print("Please enter valid argument!")
            else:
                print("Please use existing keyword") ## if user enter other keyword
                
                
            
                
        
        
        
        

