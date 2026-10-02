import json
import random
import string
from  pathlib import Path 

class Bank:
    database = 'data.json'
    data = []
    try:
        if Path(database).exists():

            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print(" No such file Exists ")

    except Exception as err:
        print(f" An exception as {err} ")

    @classmethod  
    def __update(cls):
        with open( cls.database , 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod 
    def __accountGenerate(cls):
        alpha = random.choices(string.ascii_letters , k=3)
        num = random.choices(string.digits , k=3)
        spechar = random.choices("!@#$%^&*" , k=1)
        id = alpha + num + spechar
        random.shuffle(id)
        return "".join(id)

    def Create_Account(self):
        info = {
           "Name" : input("Enter Your Name :- "),
           "Age"  :int(input("Enter Your age :- ")),
           "Email" : input("Enter Your email :- "),
           "Pin" : int(input("Enter your 4 Number pin :- ")),
           "Account" : Bank.__accountGenerate(),
           "Balance" : 0
        }

        if info['Age'] < 18 or len(str(info['Pin'])) != 4 :
           print("Sorry You cannot create your Account")
        else:
            print("\nYour account has benn created successfully \n")
            for i in info:
                print(f"{i} : {info[i]} ")
  
            print("Please note down your Account Number")
            Bank.data.append(info)
            Bank.__update()

    def Deposit_Money(self):
        accNumber = input("please tell your Account Number ")
        pin = input("please tell your pin Number ")

        userdata =  [ i for i in Bank.data if i['Account'] == accNumber  and i['Pin'] == pin ]

        if userdata == False:
            print("Sorry , No data found ")
        else:
            amount = int(input("Enter how much Amount you want to deposit :- "))  
            if amount > 10000 or amount < 0:
                print("sorry , you can not deposit above 10000 amoun below 0")
            else:
                print("before deposit :- ")
                print(userdata)
                userdata[0]['Balance'] += amount
                print("after deposit :- ")
                print(userdata)
                Bank.__update()
                print("Amount deposited successfully ")

    def Withdraw_Money(self):
        accNumber = input("please tell your Account Number ")
        pin = input("please tell your pin Number ")
    
        userdata =  [ i for i in Bank.data if i['Account'] == accNumber  and i['Pin'] == pin ]
    
        if userdata == False:
            print("Sorry , No data found ")
        else:
            amount = int(input("Enter how much Amount you want to withdraw :- "))  
            if userdata[0]['Balance'] < amount :
                print("sorry , you have not that much money")
            else:
                print("before withdraw :- ")
                print(userdata)
                userdata[0]['Balance'] -= amount
                print("after withdraw :- ")
                print(userdata)
                Bank.__update()
                print("Amount withdraw successfully ")

    def Show_Details(self):
        accNumber = input("please tell your Account Number ")
        pin = input("please tell your pin Number ")
            
        userdata =  [ i for i in Bank.data if i['Account'] == accNumber  and i['Pin'] == pin ]
       
        if userdata == False:
            print("Sorry , No data found ")
        else:
            print("YOUR INFORMATION : ")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def Update_Details(self):
        accNumber = input("please tell your Account Number ")
        pin = input("please tell your pin Number ")
                    
        userdata =  [ i for i in Bank.data if i['Account'] == accNumber  and i['Pin'] == pin ]
               
        if userdata == False:
            print("Sorry , No user data found ")
        else:
            print("You can not change the AGE , ACCOUNT NUMBER , BALANCE")
            print("Fill the details if you want to change and keep empty foe no change ")

            newdata = {
                "Name" : input("Tell your name end press enter to skip :- "),
                "Email" : input("Tell your new email end press enter to skip :- "),
                "Pin" : input("Tell your new pin end press enter to skip :- ")
            }
            if newdata['Name'] == "":
                newdata['Name']  = userdata[0]['Name']
            if newdata['Email'] == "":
                newdata['Email']  = userdata[0]['Email']
            if newdata['Pin'] == "":   
                newdata['Pin']  = userdata[0]['Pin']
            newdata['Age']  = userdata[0]['Age']
            newdata['Balance']  = userdata[0]['Balance'] 
            newdata['Account']  = userdata[0]['Account']      

            if type(newdata['Pin']) == int:
                newdata['Pin'] = int(newdata['Pin'])

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i]  = newdata[i]
                       
            Bank.__update()
            print("Bank details updated successfully")




user = Bank()    
print("Press 1 for Creating an Account")
print("Press 2 for depositing The money in the Bank")
print("Press 3 for Withdrawing The money")
print("Press 4 for Details")
print("Press 5 for Updating Details")
print("Press 6 for Deleting The Account \n ")

check = int(input("Tell your Responce :- "))

if check == 1:
    user.Create_Account()
if check == 2:
    user.Deposit_Money() 
if check == 3:
    user.Withdraw_Money()       
if check == 4:
    user.Show_Details()  
if check == 5:
    user.Update_Details()           