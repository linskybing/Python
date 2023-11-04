
import os
import sys

if __name__ == '__main__':
    
    #read and convet into int
    money = int(input('How much money do you have?\n'))

    # split each line that seperated by ',' into list 
    raw_record = input('Add some expense or income records with description and amount:\n').split(',')

    # split each string that list element by ' '
    # use strip to eliminate left and right space
    raw_record = [string.strip().split() for string in raw_record]

    # convert list element of list into tuple datastructure
    record = [(i, int(j)) for i, j in raw_record]

    #calculate expence and income
    money += sum([e[1] for e in record])

    # output record to user 
    for e in raw_record:
        print(' '.join(e))
    
    print(f'Now you have {money} dollars.')