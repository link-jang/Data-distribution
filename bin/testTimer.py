'''

@author: conny

'''


from Timer import Timer



def  testAction(args = []):
    for arg in args:
        print arg

if __name__ == '__main__':
    timer = Timer(1, 10, testAction, ['a', 'b'])
    timer.run()