import sys


class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""

    def __init__(self):
        self._amount = 0
        self._records = []
        self.initialize()
    
    # setter and getter
    # getter amount attribute
    def get_amount(self):
        return self._amount
    
    # setter amount attribute
    def set_amount(self, amount):
        self._amount = amount

    # getter records attribute
    def get_records(self):
        return self._records
    
    # setter records attribute    
    def set_records(self, records):
        self._records = records    
    
    amount = property(lambda self: self.get_amount(), \
                          lambda  self, amount: self.set_amount(amount))
    records = property(lambda self: self.get_records(), \
                          lambda  self, records: self.set_records(records))
    
    def initialize(self):
        try:
            # try to read the exists file record.txt
            with open('record.txt', 'r') as fh:

                # detect file whether is empty
                data = fh.readline()
                # using assert to check data whether is empty
                # if empty that may occur some error, then thorw AssertionError
                assert data, 'Invalid format in records.txt. Deleting the contents.'

                # read user money
                try:
                    self.amount = int(data)
                except ValueError:
                    print('Invalid format in records.txt. Deleting the contents.')
                    try:
                        self.amount = int(input('How much money do you have?\n'))
                    except ValueError:
                        print('Invalid value for money. Set to 0 by default.\n')
                    
                # read file for each line
                for data in fh.readlines():
                    c, i, j = data.split()
                    self.records += [(c, i, int(j))]

                print('welcome back!')
        except ValueError:
            print('Invalid format in records.txt. Deleting the contents.')
            try:
                self.amount = int(input('How much money do you have?\n'))
                self.records = []
            except ValueError:
                print('Invalid value for money. Set to 0 by default.\n')    
        except AssertionError as e:
            # file is empty
            print(str(e))        
            try:
                self.amount = int(input('How much money do you have?\n'))
            except ValueError:
                print('Invalid value for money. Set to 0 by default.\n')

        except FileNotFoundError:
            # when file cannot be found
            # we will require user to enter inital moeny
            try:
                self.amount = int(input('How much money do you have?\n'))

            except ValueError:
                print('Invalid value for money. Set to 0 by default.\n')
    
    def add(self, categories):
        try:

            # split each line that seperated by ',' into list 
            raw_record = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n').split(',')

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
                assert len(i) % 3 == 0, 'The format of a record should be like this:food breakfast -50.\nFail to add a record.\n'

                assert categories.is_category_valid(i[0]), 'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.'

                # extend a new record(tuple) into list
                temp += [(i[0], i[1], int(i[2]))]

            # convert list element of list into tuple datastructure
            # extend record list
                
            self.records += temp

        except AssertionError as e:
            # format error
            print(str(e))

        except ValueError:
            # invaild input
            print('Invaild value for money.\nFail to add a record.\n')
        
    def find(self, categories):
        """ 
        using paging method to show records
        each page contain five record
        user can choose any action to filter record
        """
        # each page maximum size
        paging_size = 5
        # current page
        page = 0
        # raw paging data
        paging_list = self.view_paging(self.records)       
        # start postion
        start_page = paging_size * page
        # ending position
        end_page = min(paging_size * (page + 1), len(paging_list))
        # extract range(start_page, end_page)
        paging_window = paging_list[start_page:end_page]

        while(1):  
            #show 
            print()
            # print table
            print(f'{"Category":<20s} {"Description":<20s} {"Amount":<10s}')
            print(f'{"":=<20s} {"":=<20s} {"":=<10s}')

            for _, i, j in paging_window:
                print(f'{_:<20s} {i:<20s} {j:<10d}')

            print(f'{"":=<20s} {"":=<20s} {"":=<10s}')


            pages = int(len(paging_list) / paging_size)

            if(pages < len(paging_list)/paging_size): pages +=1
            if(pages == 0): pages = 1

            print(f'Page {page + 1} of {pages}\n')

            print(f'The total amount above is {sum(map(lambda e: e[2], paging_list))}.\n')

            action = input('\nWhat do you want to do? ( previous / next / keyword / category / end)? \n')
            if (action == 'next'):
                #next page
                if(page < pages-1):
                    page += 1    
                # start postion
                start_page = paging_size * page
                # ending position
                end_page = min(paging_size * (page + 1), len(paging_list))
                # show list item from start_page to end_page
                paging_window = paging_list[start_page:end_page]
            elif (action == 'previous'):
                #previous page
                if(page > 0):
                    page -= 1                
                 # start postion
                start_page = paging_size * page
                # ending position
                end_page = min(paging_size * (page + 1), len(paging_list))
                # show list item from start_page to end_page
                paging_window = paging_list[start_page:end_page]

            elif (action == 'keyword'):
                keyword = input('\nWhich keyword do you want to find?\n')
                # reset paing number
                page = 0
                # get paging
                paging_list = self.view_paging(self.records, keyword = keyword)
                # start postion
                start_page = paging_size * page
                # ending position
                end_page = min(paging_size * (page + 1), len(paging_list))
                # extract range(start_page, end_page)
                paging_window = paging_list[start_page:end_page]

            elif (action == 'category'):
                category = input('\nWhich category do you want to find?\n')

                category_list = categories.find_subcategories(category)

                # reset paing number
                page = 0
                # get paging
                paging_list = self.view_paging(self.records, category_list)
                # start postion
                start_page = paging_size * page
                # ending position
                end_page = min(paging_size * (page + 1), len(paging_list))
                # extract range(start_page, end_page)
                paging_window = paging_list[start_page:end_page]

            elif (action == 'end'):
                break
            else:
                sys.stderr.write('Invaild command. Try again.\n')

    @staticmethod
    def view_paging(records, categories = [], keyword = ''):
        """
        return paging list and filter with categories or keyword
        """
        # extract range(start_page, end_page)
        if (keyword):
            paging_window = list(filter(lambda record: ( record[0].find(keyword) != -1 or record[1].find(keyword) != -1), records))
        elif (categories):
            paging_window = list(filter(lambda record: (record[0] in categories), records))
        else:
            paging_window = records

        return paging_window

    def view(self):
        """
        show all record in one page
        """
        
        # calculate money
        money = int(self.amount) + sum([e[2] for e in self.records])
        print()

        # print table
        print(f'{"Category":<20s} {"Description":<20s} {"Amount":<10s}')
        print(f'{"":=<20s} {"":=<20s} {"":=<10s}')

        # print each record
        for _, i, j in self.records:
            print(f'{_:<20s} {i:<20s} {j:<10d}')

        print(f'{"":=<20s} {"":=<20s} {"":=<10s}')

        print(f'Now you have {money} dollars.')

    def delete(self):
        """
        delete certain record in self._record by setter
        """
        try:

            # show position table
            self.show_delete_paging()

            # select position to delete
            # if enter the format that is not invild, would occur value error
            # that means cannot convert into int
            position = int(input('What record do you want to delete? (please input position number)\n'))
            
            # if postion is not in the range of records
            # it cause AssertionError
            assert position in range(0, len(self.records)), f"There's no record at postion No.{position}. Fail to delete a record."

            # delete the data ot the position in list
            del(self.records[position])
        except ValueError:
            print('Invaild format. Fail to delete a record.\n')
            
        except AssertionError as e:
            print(str(e))
            print()

    def show_delete_paging(self):
        """
        show record in paging methon and label each record a unique number
        user can use number to select the record that want to delete
        """
        #paging list
        temp = self.enumerate_custom(self.records)
        # current page
        page = 0
        # each page maximum size
        paging_size = 5
        # start postion
        start_page = paging_size * 0
        # end position
        end_page = min(paging_size * (page + 1), len(temp))
        # extract range(start_page, end_page)
        temp2 = temp[start_page:end_page]

        while(1):
            # show position table
            print()
            # print table
            print(f'{"Position":<10s} {"Category":<20s} {"Description":<20s} {"Amount":<10s}')
            print(f'{"":=<10s} {"":=<20s} {"":=<20s} {"":=<10s}')
            # enumerate list of temp
            
            # label the data position
            for i, item in temp2:
                c, j, k = item
                print(f'{i:<10d} {c:<20s} {j:<20s} {k:<10d}')

            print(f'{"":=<10s} {"":=<20s} {"":=<20s} {"":=<10s}')
            pages = int(len(temp) / paging_size)
            if(pages < len(temp)/paging_size): pages +=1
            if(pages == 0):pages = 1
            print(f'Page {page + 1} of {pages}')

            action = input('\nWhat do you want to do? (next / find / end)? \n')
            if (action == 'next'):
                #next page
                if(page < pages-1):
                    page += 1

                # show list item from start_page to end_page
                start_page = paging_size * page
                end_page = min(paging_size * (page+1), len(temp))
                temp2 = temp[start_page:end_page]

            elif (action == 'find'):
                keyword = input('\nPlease enter the keyword to find certain record: \n')
                temp = [e for e in self.enumerate_custom(self.records) if(e[1][1].find(keyword) != -1)]
                # calculate paing number
                page = 0
                start_page = paging_size * page
                end_page = min(paging_size * (page+1), len(temp))

                #paging
                temp2 = temp[start_page:end_page]

            elif (action == 'end'):
                break

            else:
                sys.stderr.write('Invaild command. Try again.\n')

    def save(self):
        """
        save record to the file
        """
        with open('record.txt', 'w') as fh:
            # write the initial money into file
            fh.write(str(self.amount))
            
            # add newline character, then the next data will begin in the next line
            fh.write('\n')

            # i is descriptino
            # j is amount
            # write for each records to each lines
            for c, i, j in self.records:
                string = c + ' ' + i + ' ' + str(j) + '\n'
                fh.writelines(string)

    @staticmethod
    def enumerate_custom(seq):
        """
        label the record with index
        """
        temp = []
        for i in range(0, len(seq)):
            temp += [(i, seq[i])]
        return temp

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = self.initialize_categories()   
        self._file = []        
        self.init_file()

    # getter categories attribute
    def get_categories(self):
        return self._categories
    
    # setter categories attribute
    def set_categories(self, categories):
        self._categories = categories

    # getter file attribute
    def get_file(self):
        return self._file
    
    # setter file attribute
    def set_file(self, file):        
        self._file = file
    
    categories = property(lambda self: self.get_categories(), \
                          lambda  self, categories: self.set_categories(categories))
    file = property(lambda self: self.get_file(), \
                          lambda  self, file: self.set_file(file))
    
    @staticmethod
    def initialize_categories():
        """
            get category from file
        """
        # using recursive to contruct multilist
        def construct_multilist(data, root):
            if not(data.get(root)):
                return [root]
            else:
                result = []
                for i in data[root]:
                    result += construct_multilist(data, i)
                return [root, result]
        try:
            #read file
            temp = {}
            with open('category.txt', 'r') as fh:
                    # detect file whether is empty
                    for it in fh.readlines():
                        parent, child = it.strip().split()
                        if not(temp.get(parent)): temp[parent] = []
                        temp[parent] += [child]

            return construct_multilist(temp, 'None')[1]
        except:
            return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']] 

    def init_file(self):
        # using innner function to contruct file content
        # file will be used in turn out system to write file
        def show_category_table(category, root):
            if type(category) in {list}:
                result = []
                parent = ""
                for child in category:
                    if type(child) in {list}:
                        result += show_category_table(child, parent)
                    else:
                        result += [f"{root} {child}\n"]
                        parent = child
                return result
            else:
                return [f"{root} {category}\n"]
            
        self.file = show_category_table(self.categories, "None")

    def add_category(self):
        try:
            # split each line that seperated by ',' into list 
            raw_record = input('Add new category with parent category and new category (separate by spaces):\ncat1 cat2\n').split(',')
            temp = []
            for string in raw_record:
                i = string.strip().split()
                # each records should have two fields
                # if not contain two fields, it means records format error
                assert len(i) % 2 == 0, 'The format of a category should be like this:food breakfast.\nFail to add a category.\n'

                assert (categories.is_category_valid(i[0])) or i[0] == "None", 'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a category.'
                
                assert not(categories.is_category_valid(i[i])), 'The child category already exist.\n'
                # extend a new record(tuple) into list
                temp += [f"{i[0]} {i[1]}\n"]
            # convert list element of list into tuple datastructure
            # extend record list
            self.file += temp

        except AssertionError as e:
            # format error
            print(str(e))

    def save(self):
        """
        save category to the file
        """
        with open('category.txt', 'w') as fh:
            fh.writelines(self.file)
    
    def view(self):
        """
        print categories by recursive with indent
        """
        def view_categories(L, level = 0):
            if type(L) in {list}:
                # if L is list, call recursive
                for item in L:
                    view_categories(item, level + 1)
            else:
                # if type(L) is a element, then print indent result
                print(f'{" " * 4 * (level - 1)}-{L} ')

        view_categories(self.categories)

    def is_category_valid(self, category):
        """
        this function is find category whether is in exists categories
        """
        # inner function to check category whether already exist
        def valid(category, categories):
            if type(categories) in {list}:
                for item in categories:
                    if (valid(category, item)):
                        return True
            else:
                return category == categories
            
            return False
        
        return valid(category, self.categories)
    
    def find_subcategories(self, category):
        """
        return category and its subcategory
        """
        def subcategories(category, categories):
            # generator inner function
            def find_subcategories_gen(category, categories, found = False):
                if type(categories) in {list}:
                    for index, child in enumerate(categories):
                        yield from find_subcategories_gen(category, child, found)
                        if child == category and index + 1 < len(categories) \
                            and type(categories[index + 1]) in {list}:
                            # When the target cateogry is found,
                            # recursively call this generator on the subcategories
                            # with the flag set as True
                            found = True
                            yield from find_subcategories_gen(category, categories[index + 1], found)
                            found = False

                else:
                    #base case
                    #only yield target category or already found
                    if category == categories or found:
                        yield categories
            # using generator and list comprehension return subcategories
            return [i for i in find_subcategories_gen(category, categories)]
        
        return subcategories(category, self.categories)


records = Records()
categories = Categories()

while True:
    command = input('\nWhat do you want to do (add / view / view categories / add categories / find / delete / exit)： ')
    if command == 'add':        
        records.add(categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':        
        records.delete()        
    elif command == 'view categories':
        categories.view()
    elif command == 'add categories':
        categories.add_category()
    elif command == 'find':
        records.find(categories)
        pass
    elif command == 'exit':
        records.save()
        categories.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')