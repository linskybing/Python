#! /usr/bin/env python3
import sys

# The 5 function definitions here
def initialize():
    initial_money = 0
    records = []

    try:
        # try to read the exists file record.txt
        # if not exist would occur FileNotFoundError
        with open('record.txt', 'r') as fh:

            # detect file whether is empty
            data = fh.readline()
            # using assert to check data whether is empty
            # if empty that may occur some error, then thorw AssertionError
            assert data, 'File is empty.'

            # read user money
            try:
                # due to data is a string
                # so data should convert into int
                initial_money = int(data)
            except ValueError:
                # that mean data cannot convert into string
                # maybe it is a character
                # or some other label
                # not a number character
                print('Invild value for money in file. Set to 0 by default')
                initial_money = 0
                
            # read file for each line
            # data contain '{description} {amount}'
            # we should split it into i and j
            # due to j represent number, but it is character
            # so it should convert to int type
            for data in fh.readlines():
                i, j = data.split()
                records += [(i, int(j))]

            print('welcome back!')
    except ValueError:
        # during convert amount into int
        # amount is not a number character
        # or file that exists some empty filed
        # we call that is invaild record value
        sys.stderr.write('Invild record value in the file.\n')
    except AssertionError as e:
        # file is empty
        print(str(e))
        
        try:
            initial_money = int(input('How much money do you have?\n'))

        except ValueError:
            print('Invalid value for money. Set to 0 by default.\n')

    except FileNotFoundError:
        # when file cannot be found
        # we will require user to enter inital moeny
        try:
            initial_money = int(input('How much money do you have?\n'))

        except ValueError:
            print('Invalid value for money. Set to 0 by default.\n')
    return initial_money, records

def add(records):
    try:

        # split each line that seperated by ',' into list 
        raw_record = input('Add some expense or income records with description and amount:\n').split(',')

        # split each string that list element by ' '
        # use strip to eliminate left and right space
        temp = []

        for string in raw_record:
            # we can tolerate that user enter data that may consist some spaces
            # so ew strip space in left and right
            # after strip, using split() to seperate string into list
            i = string.strip().split()

            # each records should have two fields
            # if not contain two fields, it means records format error
            assert len(i) % 2 == 0, 'The format of a record should be like this: breakfast -50.\nFail to add a record.\n'

            # extend a new record(tuple) into list
            temp += [(i[0], int(i[1]))]

        # convert list element of list into tuple datastructure
        # extend record list
            
        records.extend(temp)

    except AssertionError as e:
        # format error
        print(str(e))

    except ValueError:
        # invaild input
        print('Invaild value for money.\nFail to add a record.\n')

    return records

def view(initial_money, records):

    # calculate money
    money = initial_money + sum([e[1] for e in records])
    print()

    # print table    
    print(f'{"Description":<20s} {"Amount":<10s}')
    print(f'{"":=<20s} {"":=<10s}')

    # print each records
    for i, j in records:
        print(f'{i:<20s} {j:<10d}')

    print(f'{"":=<20s} {"":=<10s}')
    print(f'Now you have {money} dollars.')

def delete(records):

    try:

        # show position table
        print()
        # print table
        print(f'{"Position":<10s} {"Description":<20s} {"Amount":<10s}')
        print(f'{"":=<10s} {"":=<20s} {"":=<10s}')

        # label the data position
        for i, item in enumerate(records):
            j, k = item
            print(f'{i:<10d} {j:<20s} {k:<10d}')

        print(f'{"":=<10s} {"":=<20s} {"":=<10s}')

        # select position to delete
        # if enter the format that is not invild, would occur value error
        # that means cannot convert into int
        position = int(input('What record do you want to delete? (please input position number)\n'))
        
        # if postion is not in the range of records
        # it cause AssertionError
        assert position in range(0, len(records)), f"There's no record at postion No.{position}. Fail to delete a record."

        # delete the data ot the position in list
        del(records[position])
    except ValueError:
        print('Invaild format. Fail to delete a record.\n')
        
    except AssertionError as e:
        print(str(e))
        print()
        
    return records

def save(initial_money, records):

    # using with-as to open file

    with open('record.txt', 'w') as fh:
        # write the initial money into file
        fh.write(str(initial_money))
        
        # add newline character, then the next data will begin in the next line
        fh.write('\n')

        # i is descriptino
        # j is amount
        # write for each records to each lines
        for i, j in records:
            string = i + ' ' + str(j) + '\n'
            fh.writelines(string)

initial_money, records = initialize()

while True:
    # inpute the command number
    command = input('\nWhat do you want to do (add / view / delete / exit)? ')

    if command == 'add':
        # add some records into current list
        records = add(records)
    elif command == 'view':
        # show the current records
        view(initial_money, records)
    elif command == 'delete':
        # return after change records
        records = delete(records)
    elif command == 'exit':
        # we should save file before exit
        save(initial_money, records)
        break
    else:
        # the entered commnad is not in defined command
        # print error to user
        # tell that it is not vaild
        sys.stderr.write('Invaild command. Try again.\n')