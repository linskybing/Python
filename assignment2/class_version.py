import sys

class System:
    
    def __init__(self):
        # member variable
        self.money = 0
        self.record = []

        self.initilize()

    def initilize(self):

        self.readFile()

        while(1):

            try:
                action = input('What do you want to do (add / view / delete / exit)?\n')

                #choose correspond to execute
                if (action == 'exit'): 
                    self.save()
                    break
                elif (action == 'add'):
                    self.add()

                elif (action == 'delete'):
                    self.delete()

                elif (action == 'view'):
                    self.view()

                else:
                    sys.stderr.write('Invaild command. Try again.\n')

            except AssertionError as e:
                #command not in the list
                print(str(e))
                print()

    def add(self):

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
            
            self.record.extend(temp)

            # calculate money
            self.money += sum([ e[1] for e in  temp])

        except AssertionError as e:
            # format error
            print(str(e))

        except ValueError:
            # invaild input
            print('Invaild value for money.\nFail to add a record.\n')


    def delete(self):

        try:

            # show position table
            self.delete_view()
            position = int(input('What record do you want to delete? (please input position number)\n'))
            
            assert position in range(0, len(self.record)), f"There's no record with postion No.{position}. Fail to delete a record."
            
            # delete the record and add value return money
            self.money -= int(self.record[position][1])

            del(self.record[position])
        except ValueError:
            print('Invaild format. Fail to delete a record.\n')
        
        except AssertionError as e:
            print(str(e))
            print()
    
    def delete_view(self):

        print()
        # print table
        print(f'{"Position":<10s} {"Description":<20s} {"Amount":<10s}')
        print(f'{"":=<10s} {"":=<20s} {"":=<10s}')

        # label the data position
        for i, item in enumerate(self.record):
            j, k = item
            print(f'{i:<10d} {j:<20s} {k:<10d}')

        print(f'{"":=<10s} {"":=<20s} {"":=<10s}')

    def view(self):

        print()
        # print table
        print(f'{"Description":<20s} {"Amount":<10s}')
        print(f'{"":=<20s} {"":=<10s}')

        for i, j in self.record:
            print(f'{i:<20s} {j:<10d}')

        print(f'{"":=<20s} {"":=<10s}')
        print(f'Now you have {self.money} dollars.')
    
    def save(self):

        with open('record.txt', 'w') as fh:
            fh.write(str(self.money))
            fh.write('\n')

            for i, j in self.record:
                string = i + ' ' + str(j) + '\n'
                fh.writelines(string)

    def readFile(self):
        try:
            
            with open('record.txt', 'r') as fh:

                # detect file whether is empty
                data = fh.readline()
                assert data, 'File is empty.'

                # read user money
                try:
                    self.money = int(data)
                except ValueError:
                    print('Invild value for money in file. Set to 0 by default')
                    self.money = 0
                
                for data in fh.readlines():
                    i, j = data.split()
                    self.record += [(i, int(j))]

                print('welcome back!\n')
        except ValueError:
            sys.stderr.write('Invild record value in the file.\n')

        except AssertionError as e:
            print(e)
            print()

        except FileNotFoundError:
            try:
                self.money = int(input('How much money do you have?\n'))

            except ValueError:
                print('Invalid value for money. Set to 0 by default.\n')
    
if __name__ == '__main__':
    
    sys = System()