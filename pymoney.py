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
        self.DataBaseCheck()
        self.CookieCheck()

        # method        
        self.Loading()        

    def Loading(self):

        print('Welcome to the pymoeny\n')

        if (not(self.cookie)):
           
            
            print('Do you want to (1 : Login) or (2 : Register) or (Other keyword: Exist) ? \n')
            mode = int(input('Please choose the number of features that you want: '))

            if (mode == 1):
                self.Login()
                self.Loading()                

            elif (mode == 2):
                self.Register()

            else: 
                mode = -1
        else:
            mode = 0
            
            print(f'Hello {self.user_account:5s}!\n Which features do you want ?\n (1 : Add some financial records) or (2 : Show the history records) or (3 : Logout) or (-1: Exist)\n')
            mode = int(input('Please choose the number of features that you want: '))

            if (mode == 1):
                pass                    

            elif (mode == 2):
                pass                    

            elif (mode == 3):
                self.Logout()                    

            else:
                pass



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

        
        fh = open(cookie_path, 'r')
        data = fh.readline()
        if (data == '1'):
            self.cookie = True 
        else:
            self.cookie = False 
        
    def Login(self):
            
        #input account data
        account = input('{:6s}'.format('Account: '))
        password = input('{:6s}'.format('Password: '))
        print()

        # CheckUserDataExist
        if (self.user_account and self.user_password):
            
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

    #Add some financial records
    def AddRecord(self, account):

        # if don't have any reocrd then create one
        if (account not in self.balance_data):
            money = int(input('How much money do you have? '))
            self.balance_data[account] = money
            self.financial_records[account]['balance'] = []
            self.financial_records[account]['change'] = []

        # receive data and record it
        data_list = input('Add an expense or income record with description and amount:').split(',')

        # maybe there are many reocrd that the user want to reocrd
        # then we use data_list that record seperated by ','
        # deal with data by sequence

        for data in data_list:

            description, change = data.split(' ')
            change = int(change)
            self.financial_records[account]['balance'] += description
            self.financial_records[account]['change'] += change

            self.balance_data[account] += change
            print(f'Now you have {self.financial_records[account]} dollars.')

            # modify change into database file
            self.WriteRecord(self, account, description, change)

    def WriteRecord(self, account, describe, change):

        # how many the user record has
        record_number = len(self.financial_records[account]['balance'])

        fh = open(user_data_record, 'r+')
        fh_content = fh.readlines()

        #find the user data in which line        
        index = 0
        for line in fh_content:
            record = line.split()
            index += 1
            if (record[0] == account): break
    ############################################################################     
    
    def ReadBalanceData(self):

        #check database whether has user financial balance  
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