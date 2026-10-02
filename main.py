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
                if amount > 10000 or amount < 0:
                    print("sorry , you only can withdraw above 0 amount below your current amount")
                else:
                    print("before withdraw :- ")
                    print(userdata)
                    userdata[0]['Balance'] -= amount
                    print("after withdraw :- ")
                    print(userdata)
                    Bank.__update()
                    print("Amount withdraw successfully ")
    


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