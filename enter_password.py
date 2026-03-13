#defines a function called main()
def main():

    #calls userNameInput() to get username and password
    username, password = userNameInput()
    
    #calls test_user() to check credentials by variables "username" and "password" 
    result = test_user(username, password)
    
    #calls printOutput() with result message
    printOutput(result)

#defines a function called userNameInput()
def userNameInput():
    
    #asks for username by prompt, input is then assigned to username
    username = input("What is your user name? ")
    
    #asks for password by prompt, input is assigned to password
    password = input("What is your password? ")
    
    #returns both username and password
    return username, password

#defines a function called test_user()
def test_user(username, password):
    
    #assigns code as "admin" to valid_user
    valid_user = "Admin"
    
    #assigns pass to valid_pass
    valid_pass = "pass"
    
    #if statement if username is equal to valid_user and password is equal to valid_pass then go to next line
    if username == valid_user and password == valid_pass:
     
        #returns success message
        return "User Validated!"
    
    #else statement, all else follow next line
    else:
    
        #returns failure message
        return "Username or Password Incorrect"

#defines a function called printOutput()
def printOutput(message):
    
    #prints user friendly message
    print(message)

#calls main()
if __name__ == "__main__":
    main()