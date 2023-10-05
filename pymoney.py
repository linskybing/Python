
if __name__ == '__main__':
    money = int(input('How much money do you have? '))
    describe, change = input('Add an expense or income record with description and amount:').split()
    print(f'Now you have {money + int(change)} dollars.')