#! /usr/bin/env python3
import os

user_infomation_path = 'account.txt'
cookie_path = 'cookie.txt'

class System:

    def __init__(self):

        self.cookie = False        
        self.Loading()        

    def Loading(self):

        self.DataBaseCheck()
        self.CookieCheck()

    # check database dir exist or not
    # if don't exist then create a new one
    def DataBaseCheck(self):

        if (not(os.path.exists(user_infomation_path))):
            fh = open(user_infomation_path, 'w')
            fh.close()

    # this is a user cookie check
    # that use to determine user has already login
    def CookieCheck(self):

        if (not(os.path.exists(cookie_path))):
            fh = open(cookie_path, 'w')
            fh.close()

        else:
            self.cookie = True
class User:
    def __init__(self):
        pass

    
if __name__ == '__main__':   
    sys = System()
    ##money = int(input('How much money do you have? '))
    ##describe, change = input('Add an expense or income record with description and amount:').split()
    ##print(f'Now you have {money + int(change)} dollars.')