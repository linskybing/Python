import sys

# The 5 function definitions here
def initialize():
    initial_money = 0
    records = []

    try:
            
        with open('record.txt', 'r') as fh:

            # detect file whether is empty
            data = fh.readline()
            assert data, 'File is empty.'

            # read user money
            try:
                initial_money = int(data)
            except ValueError:
                print('Invild value for money in file. Set to 0 by default')
                initial_money = 0
                
            for data in fh.readlines():
                i, j = data.split()
                records += [(i, int(j))]

            print('welcome back!')
    except ValueError:
        sys.stderr.write('Invild record value in the file.\n')

    except AssertionError as e:
        print(e)
        print()

    except FileNotFoundError:
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

            i = string.strip().split()

            assert len(i) % 2 == 0, 'The format of a record should be like this: breakfast -50.\nFail to add a record.\n'

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
    money = initial_money + sum([e[1] for e in records])
    print()
    # print table
    print(f'{"Description":<20s} {"Amount":<10s}')
    print(f'{"":=<20s} {"":=<10s}')

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
        position = int(input('What record do you want to delete? (please input position number)\n'))
            
        assert position in range(0, len(records)), f"There's no record at postion No.{position}. Fail to delete a record."


        del(records[position])
    except ValueError:
        print('Invaild format. Fail to delete a record.\n')
        
    except AssertionError as e:
        print(str(e))
        print()
        
    return records

def save(initial_money, records):

    with open('record.txt', 'w') as fh:
        fh.write(str(initial_money))
        fh.write('\n')

        for i, j in records:
            string = i + ' ' + str(j) + '\n'
            fh.writelines(string)

initial_money, records = initialize()

while True:

    command = input('\nWhat do you want to do (add / view / delete / exit)? ')

    if command == 'add':
        records = add(records)
    elif command == 'view':
        view(initial_money, records)
    elif command == 'delete':
        records = delete(records)
    elif command == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invaild command. Try again.\n')