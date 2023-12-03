

categories = []

def initialize_categories():
    def construct_multilist(data, root):
        if not(data.get(root)):
            return [root]
        else:
            result = []
            for i in data[root]:
                result += construct_multilist(data, i)
            return [root, result]
    try:
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

def append_category_data(parent_category, child_category):
    pass

def view_categories(L, level = 0):
    '''
        print categories by recursive with indent
    '''
    if type(L) in {list}:
        # if L is list, call recursive
        for item in L:
            view_categories(item, level + 1)
    else:
        # if type(L) is a element, then print indent result
        print(f'{" " * 4 * (level - 1)}-{L} ')

def is_category_valid(category, categories):
    '''
        this function is find category whether is in exists categories
    '''
    if type(categories) in {list}:

        for item in categories:
            if (is_category_valid(category, item)):
                return True
    else:
        return category == categories
    
    return False

def find_subcategories(category, categories):
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

categories = initialize_categories()
print(show_category_table(categories, "None"))
