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
        self.cookie = False
        self.CookieCheck()
        self.database_ob = DataBase()

        # method        
        self.Loading()        
    
    def Loading(self):
        
        print('\nWelcome to the pymoeny\n')

        # not login
        if (not(self.cookie)):
           
            
            print('Do you want to (1 : Login) or (2 : Register) or (Other keyword: Exist) ? \n')
            mode = int(input('Please choose the number of features that you want: '))

            if (mode == 1):
                self.Login()                               

            elif (mode == 2):
                self.Register()

            else: 
                pass

        # already login
        else:
            mode = 0
            
            print(f'Hello {self.user_account}!\n\nWhich features do you want ?\n\n (1 : Add some financial records) or (2 : Show the history records) or (3 : Logout) or (Other keyword: Exist)\n')
            mode = int(input('Please choose the number of features that you want: '))

            if (mode == 1):
                self.database_ob.AddRecord(self.user_account) 
                
            elif (mode == 2):
                self.database_ob.ShowHistory(self.user_account)                   

            elif (mode == 3):
                self.Logout()                    

            else:
                pass



    # this is a user cookie check
    # that use to determine user has already login
    def CookieCheck(self):

        if (not(os.path.exists(cookie_path))):
            fh = open(cookie_path, 'w')
            fh.close()

        
        fh = open(cookie_path, 'r')
        data = fh.readline()
        if (data and data != '0' ):
            self.cookie = True
            self.user_account = data
            
        else:
            self.cookie = False 
        
    def Login(self):
            
        #input account data
        
        account = input('{:6s}'.format('Account: '))
        password = input('{:6s}'.format('Password: '))
        
        # CheckUserDataExist
        if (self.database_ob.AccountExist(account)):
            
            if (self.database_ob.CheckLogin(account, password)):                
                self.user_account = account
                self.WriteCookie(account)
                self.Loading()
                
            else:
                print("Account or Password doesn't match.")
        else :
            print('Account does not exist !!')                            
    
    def Register(self):
        #input account data
        print('Please enter some information to register\n')
        account = input('{:6s}'.format('Account: '))
        password = input('{:6s}'.format('Password: '))

        if (self.database_ob.AccountExist(account)):
            print('Account has already exist.')
        else :            
            self.database_ob.RegisterAccount(account, password)           
            
            #success register 
            self.user_account = account
            self.WriteCookie(account)
            self.Loading()

    def WriteCookie(self, account):

        # to set user cookie is active or inactive
        # if cookie is active, then it is mean that user has already been login
        # in other hand, user has not been login yet.        
        if (account):
            fh = open(cookie_path, 'w')
            fh.write(account)
            fh.close()
            self.cookie = True
        else:
            fh = open(cookie_path, 'w')
            fh.write('0')
            fh.close()
            self.cookie = False

    def Logout(self):
        self.WriteCookie('0')

class DataBase:

    def __init__(self):

        #member variable
        self.balance_data = {}
        self.financial_records = {}
        self.member_account = {}
        #member method
        self.ReadUserRecord()
        self.ReadBalanceData()
        self.ReadUserAccount()

    #############################################
    # About Read database                       #
    #############################################
    
    def ReadUserAccount(self):
        # check user account file exist
        if (not(os.path.exists(user_infomation_path))):
            fh = open(user_infomation_path, 'w')
            fh.close()
        
        # read user account data from file
        fh = open(user_infomation_path, 'r')
        file = fh.readlines()
        fh.close()
        
        for data in file:
            account, password = data.split()
            self.member_account[account] = password

    #read the record of the user    
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
        
        last = ''
        for i in range(0, len(data)):
            account, description, change = data[i].split()
            
            if (account != last):                
                self.financial_records[account] = {}
                self.financial_records[account]['balance'] = []
                self.financial_records[account]['change'] = []
                last = account
            self.financial_records[account]['balance'].append(description)
            self.financial_records[account]['change'].append(int(change))

    #read how many money user has  
    def ReadBalanceData(self):

        #check database whether has user financial balance  
        if (not(os.path.exists(user_balance))):
            fh = open(user_balance, 'w')
            fh.close()
        fh = open(user_balance, 'r')
        
        for temp in fh.readlines():
            data = temp.split()
            self.balance_data[data[0]] = int(data[1])
        fh.close()    

    #############################################
    # About Modify File                         #
    #############################################
    
    def RegisterAccount(self, account, password):
        
        #write data into database
        fh = open(user_infomation_path, 'r')
        if(len(fh.readlines()) > 0):
            fh = open(user_infomation_path, 'a')
            fh.write(f'\n{account}\t{password}')
            fh.close()
        else:
            fh = open(user_infomation_path, 'w')
            fh.write(f'{account}\t{password}')
            fh.close()
        
        self.member_account[account] = password
        
    #Add some financial records
    def AddRecord(self, account):

        # if don't have any reocrd then create one
        if (account not in self.balance_data):
            money = int(input('How much money do you have? '))
            self.balance_data[account] = money
            self.financial_records[account] = {}
            self.financial_records[account]['balance'] = []
            self.financial_records[account]['change'] = []

        # receive data and record it
        # maybe there are many reocrd that the user want to reocrd
        # then we use data_list that record seperated by ','
        # deal with data by sequence

        data_list = input('Add an expense or income record with description and amount:').split(',')
        #self.financial_records[account]['balance'].update([tuple(balance, int(change)) for data in data_list for balance, change in data.strip().split())
        
        for data in data_list:
            data = data.strip()
            description, change = data.split(' ')
            change = int(change)            
            self.financial_records[account]['balance'].append(description)
            self.financial_records[account]['change'].append(int(change))  

            self.balance_data[account] += change
            
        print(f'Now you have {self.balance_data[account]} dollars.')
        self.WriteRecord()
        self.ChangeBalance()

    # update record in database
    def WriteRecord(self):

        fh = open(user_data_record, 'w')        
        for account in self.financial_records:
            records = self.financial_records[account]
            for i in range(0, len(records['balance'])):                
                fh.write(f"{account}\t{records['balance'][i]}\t{records['change'][i]}\n")

        fh.close()
    
    def ChangeBalance(self):

        fh = open(user_balance, 'w')

        for account in self.balance_data:            
            fh.write(f'{account}\t{self.balance_data[account]}\n')
        
        fh.close()       
        
    #############################################
    # Useful Check Function                     #
    #############################################
    
    # Check user account whether has already existed
    def AccountExist(self, account):
        
        if (account in self.member_account):
            return True
        
        return False
    
    # check user account information whether is correct
    def CheckLogin(self, account, password):
        if (password == self.member_account[account]):
            return True
        
        return False
    
    #############################################
    # About Showing data                        #
    #############################################

    def ShowHistory(self, u_account):
        if (u_account in self.balance_data):
            print(f'Now you have {self.balance_data[u_account]} dollars.\n')
            print(f'------your record history------\n')

            for account in self.financial_records:
                
                if (u_account == account):
                    records = self.financial_records[account]            
                    for i in range(0, len(records['balance'])):            
                        print(f"{self.financial_records[account]['balance'][i]:10s}{self.financial_records[account]['change'][i]:10d}")  

            print(f'-------------------------------\n')

        else:            
            print(f"you don't have any record. please add new record first")
            
if __name__ == '__main__':   
    sys = System()