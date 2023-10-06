#! /usr/bin/env python3
import os

user_infomation_path = 'account.txt'
cookie_path = 'cookie.txt'
user_data_record = 'record.txt'
user_balance = 'balance.txt'

class System:

    def __init__(self):
        #member variable
        self.user_account = ''
        self.user_password = ''
        self.cookie = False
        self.database_ob = DataBase()

        # method        
        self.Loading()        

    def Loading(self):

        self.DataBaseCheck()
        self.CookieCheck()

        print('Welcome to the pymoeny\n')

        if (not(self.cookie)):
            print('Do you want to (1 : Login) or (2 : Register) ? \n')
            mode = input('Please choose the number of features that you want.')

            if (mode == '1'):
                self.Login()

            elif (mode == '2'):
                self.Register()
            else: 
                pass
        else:
            print(f'Hello {self.user_account:6s} \n')


    # check database dir exist or not
    # if don't exist then create a new one
    def DataBaseCheck(self):

        if (not(os.path.exists(user_infomation_path))):
            fh = open(user_infomation_path, 'w')
            fh.close()
        else :

            #load userdata
            fh = open(user_infomation_path, 'r')  
            user_data = fh.readline().split()
            fh.close()

            if(user_data):
                self.user_account = user_data[0]
                self.user_password = user_data[1]

    # this is a user cookie check
    # that use to determine user has already login
    def CookieCheck(self):

        if (not(os.path.exists(cookie_path))):
            fh = open(cookie_path, 'w')
            fh.close()

        else:
            fh = open(cookie_path, 'r')
            data = fh.readline()
            if (data):
                self.cookie = True 

    def Login(self):
            
        #input account data
        account = input('{:6s}'.format('Account: '))
        password = input('{:6s}'.format('Password: '))

        # CheckUserDataExist
        if (self.user_account and self.user_password):
            print('{:6s}{:6s}'.format((account, password)))
            if (account == self.user_account and password == self.user_password):
                self.WriteCookie(1)
            else:
                print("Account or Password doesn't match.\n")
        else :
            print('Account does not exist !!')                            
    
    def Register(self):
        #input account data
        print('Please enter some information to register\n')
        account = input('{:6s}'.format('Account: '))
        password = input('{:6s}'.format('Password: '))

        if (account == self.user_account):
            print('Account has already exist.')
        else :
            #write data into database
            fh = open(user_infomation_path, 'w')
            fh.write(f'{account}\t{password}')
            fh.close()

            #success register 
            self.WriteCookie(1)
            self.DataBaseCheck()
            self.Login()

    def WriteCookie(self, flag):

        # to set user cookie is active or inactive
        # if cookie is active, then it is mean that user has already been login
        # in other hand, user has not been login yet.        
        if (flag):
            fh = open(cookie_path, 'w')
            fh.write('1')
            fh.close()
            self.cookie = True
        else:
            fh = open(cookie_path, 'w')
            fh.write('0')
            fh.close()
            self.cookie = False

    def Logout(self):

        self.WriteCookie(0)

    def Exit(self):
        pass

class DataBase:

    def __init__(self):

        #member variable
        self.balance_data = {}
        self.financial_records = {}
        
        #member method
        self.ReadUserRecord()
        self.ReadBalanceData()
    
    def ReadUserRecord(self):
        #check database whether user financial records exist or not
        if (not(os.path.exists(user_data_record))):
            fh = open(user_data_record, 'w')
            fh.close()

        #read user financial records from file
        fh = open(user_data_record, 'r')
        data = fh.readlines()
        fh.close()

        # data is stored similarly to JSON Form
        # {
        #   'user_account' : {
        #        'balance': [],
        #        'change': [],
        #   },
        # }

        for i in range(0, len(data)):
            account, description, change = data[i].split()

            self.financial_records[account]['balance'] += description
            self.financial_records[account]['change'] += change                


               
    def ReadBalanceData(self):

        #check database  whether has user financial balance  
        if (not(os.path.exists(user_balance))):
            fh = open(user_balance, 'w')
            fh.close()
        fh = open(user_balance, 'r')
        
        for temp in fh.readlines():
            data = temp.split()
            self.balance_data[data[0]] = data[1]
        fh.close()



if __name__ == '__main__':   
    sys = System()
    ##money = int(input('How much money do you have? '))
    ##describe, change = input('Add an expense or income record with description and amount:').split()
    ##print(f'Now you have {money + int(change)} dollars.')