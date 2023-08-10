'''Gives details of a train number'''

train_number = 12002 # int(input("Enter a train number: "))

def conventions(t_num):
    '''Checks if the number matches as per the convention from IRFCA'''
    if t_num in range(1000, 10000):
        print("Special Trains")
        t_num = str(t_num)
        if t_num[1] in ("0", "1", "2"):
            

    if t_num in range(10000, 30000):
        print("Long Distance Train")

    if t_num in range(30000, 40000):
        print("Kolkata Suburban Train")
    
    if t_num in range(40000, 50000):
        print("suburban trains in Chennai, New Delhi, Secunderabad, and other metropolitan areas".capitalize())
    
    if t_num in range(50000, 60000):
        print("Passenger trains with conventional coaches")
    
    if t_num in range(60000, 70000):
        print("MEMU Trains")
    
    if t_num in range(70000, 80000):
        print("DEMU Trains")
    
    if t_num in range(90000, 100000):
        print("Mumbai area suburban trains")

