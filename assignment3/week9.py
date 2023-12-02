

categories = []

def initialize_categories():

    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

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
