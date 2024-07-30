global checker
checker = False
c='CREDITED'
d='DEBITED'
#modules
import mysql.connector as sql
import time
import datetime as dt
from datetime import date
import random as rn
import sys
import maskpass as mp
from tabulate import tabulate
#--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**
#connect to sql
con= sql.connect(host='localhost',password=input('SQL CONNECTOR; ENTER YOUR PASSWORD: '),user='root')
if con.is_connected():
    print('done')
else:
    print('error')
cu = con.cursor(buffered=True) 
#creates table and database if it doesnt exist
cu.execute('create database if not exists testings')
cu.execute('use testings')
cu.execute('''create table if not exists bank(
        IDNO int primary key,
        Username varchar(255),
        Mobile bigint,
        Email varchar(255),
        Occupation varchar(255),
        DOR date,
        balance int,
        passw varchar(255),
        upi varchar(255))''')
cu.execute('''create table if not exists transactions(
        USERS_NAME VARCHAR(255),
        TRANSACTION_ID INT PRIMARY KEY,
        TRANSACTION_DATE DATETIME,
        TRANSACTION_AMT INT,
        CREDIT_OR_DEBIT VARCHAR(30),
        to_from_user varchar(30))''')
con.commit()
#user defined functions

def getint(x):
    global intchecker
    intchecker=False
    while True:
        try:
            global num
            num=int(input(x))
            intchecker=True
            break
        except:
            print('only digits are accepted!')
            time.sleep(1)

    
def CreateAcc():
    global phonechecker
    phonechecker=False
    idnolist=[]
    userl=[]
#generates bank id or id no(unique)
    cu.execute('select idno from bank')
    for i in cu:
        idnolist.append(i[0])
    while True:
        x=rn.randint(1000,999999)
        if x not in idnolist:
            var1=x
            break
#generates a bank pin        
    pinlist=[]
    cu.execute('select bankpin from bank')
    for i in cu:
        pinlist.append(i[0])
    while True:
        x2=rn.randint(1000,9999)
        if x2 not in pinlist:
            var2=x2
            break
        
#all the essential data        
    inplist=[var1,
             
             input('Enter name: '),
             
             input('enter email addr: '),
             
             input('Enter occupasion: '),
             
             date.today(), #date of registeration
             
             0,
             
             var2]
    while True:
        getint('enter your phone number: ')
        if intchecker:
            phonels=[]
            cu.execute(f'select mobile from bank')
            for i in cu:
                phonels.append(i[0])
            if num in phonels:
                print('registeration of this number already exists, please login or enter a new mobile number')
                time.sleep(1)
            else:
                phonechecker=True
                numb=num
                inplist.insert(2,numb)
                
            
                if len(str(inplist[2]))==10: #checks if number entered is correct(10 digits)
                    
                    if '@' in inplist[3]: #check for invalid email
                        spl=inplist[3].split('@')

                        upi=spl[0]+'@oktestbank' #generates upi


                        cu.execute('select email from bank')
                        for i in cu:
                            userl.append(i[0])
                        if inplist[3] not in userl:

                            while True:
                                x1=mp.askpass('enter password: ',mask='*')
                                x2=mp.askpass('enter password again: ',mask='*')

                                if x2==x1:
                                    print('generating your user id....')
                                    time.sleep(1)
                                    print('generating bank pin and upi id....')
                                    time.sleep(2)
                                    print('registering your account into the database....')
                                    time.sleep(2)
                                    inplist.insert(8,x1)
                                    inplist.append(upi)
                                    cu.execute('select * from bank')



                                    jn=' ,'.join('%s'for i in inplist)



                                    cu.execute(f"insert into bank values({jn})",(inplist))
                                    con.commit()

                                    print(f'''
                                    succesfully registered! here is your id number:{var1}, your bank id pin: {var2} 
                                    and your upi id: {upi}
                                    to generate a new/custom pin or upi id contact admin''')
                                    time.sleep(1)
                                    while True:
                                        try:
                                            virtual= int(input('PLEASE ENTER VIRTUAL MONEY TO BE CREDITED IN YOUR ACCOUNT(VALUE SHALL BE LESS THAN 10,00,000): '))
                                            if virtual > 1000000:
                                                print('less than 1000000 please')
                                            else:
                                                cu.execute(f'update bank set balance={virtual} where mobile={numb}')
                                                con.commit()
                                                print('updated successfully')
                                                break
                                        except ValueError:
                                            print('invalid input try again')
                                    break
                                    
                                else:
                                    print('enter again!')
                        else:
                            print('email has already been registered, try again')
                    else:
                        print('unknown email address')
                else:
                    print('invalid mobile number!')
        if phonechecker==True:
            break


        
def passcheck():
    counter = 5
    cu.execute(f'select passw from bank where email="{user}"')
    for i in cu:
        while True:
            passw=mp.askpass('enter password: ',mask='*')
            if passw in i:
                print('succesfully logged in')
                global checker
                checker = True
                break
            else:
                print(f'wrong password, you have {counter} tries left')
                counter-=1
                if counter <0:
                    print(f'system haulted, try again after {sleep} seconds.')
                    break
                    
                    
                    
def login():
    listuser=[]
    global sleep
    sleep=10
    
    cu.execute(f'select email from bank')
    
    
    for i in cu:
        listuser.append(i[0])
        
    
    


    while True:
        if checker:
             break
        global user
        user=input('enter email address(enter E to exit): ')
        if user.upper()=="E":
            break
        if user in listuser:
            cu.execute(f'SELECT passw FROM bank where email = "{user}"')
                
            
            while True:
                counter=5
                if checker:
                    break
                
                for i in cu:
                    if checker:
                        break
                    while True:
                        if checker:
                            break
                        passcheck()
                        if checker==False:
                            time.sleep(sleep)
                            sleep+=5
                                        

        if user not in listuser:
            print('wrong username ')
            time.sleep(1)

            
            
            

def credit():
    if checker==False:
        print('LOGIN BEFORE PROCEEDING')
    
    
    else:
        cu.execute(f'select Username from bank where email="{user}"')
        for i in cu:
            print(f'logged in as: "{i[0]}"')
            time.sleep(2)
        exitchecker=False
        userslist=[]
        balchecker=True
        cu.execute(f'select idno,email from bank')
        for j in cu:
            if user in j:
                global idnumber
                idnumber=j[0]
        
        money=int(input('enter amount: '))
        cu.execute(f'select balance from bank where email="{user}"')
        for i in cu:
            print(f'current balance: "{i[0]}"')
            if i[0]<money:
                print('insufficient funds in your current bank account')
                break
            else:
        
                try:
                    cu.execute(f'select bankpin from bank where email="{user}"')
                    for i in cu:
                        pincount=3
                        while True:
                            if exitchecker:
                                break
                            else:
                                while True:
                                    try:
                                        global pin
                                        pin=int(mp.askpass('enter pin: ',mask='*'))
                                        break
                                    except:
                                        print('enter digits only!')
                                        time.sleep(1)
                            if pin in i:

                                

                                cu.execute(f'select idno,upi from bank')
                                for i in cu:
                                    userslist.append(i[1])
                                while True:
                                    touser=input('enter upi id of the user: ')
                                    if touser in userslist:
                                        time.sleep(1)
                                        print('found user')
                                        time.sleep(2)
                                        print('please wait while the payment is being processed...')

                                        cu.execute(f'select email from bank where email="{user}"')
                                        for names1 in cu:
                                            global namevar
                                            namevar=names1[0]
                        
                                        cu.execute(f'select email from bank where upi="{touser}"')
                                        for names2 in cu:
                                            global ccc
                                            ccc=names2[0]
                                        cu.execute(f'select upi from bank where email="{user}"')
                                        for users in cu:
                                            upiname=users[0]
                                        cu.execute(f'select idno from bank where upi="{touser}"')
                                        for jj in cu:
                                            global idnumberto
                                            idnumberto=jj[0]
                                        #generate transaction id
                                        idlist2=[]

                                        cu.execute('select transaction_id from transactions')
                                        for k in cu:
                                            idlist2.append(k[0])
                                        while True:
                                            x3=rn.randint(10000,999999)
                                            if x3 not in idlist2:
                                                var3=x3
                                                idlist2.append(x3)
                                                break
                                        while True:
                                            x4=rn.randint(10000,999999)
                                            if x4 not in idlist2:
                                                var4=x4
                                                idlist2.append(x4)
                                                break
                                        time.sleep(4)




                                        cu.execute(f'update bank set balance = balance-{money} where idno={idnumber}')

                                        cu.execute(f'update bank set balance = balance+{money} where idno={idnumberto}')

                                        cu.execute(f'''insert into transactions
                                        values
                                        
                                        ("{namevar}",{var3},"{dt.datetime.now()}",{money},
                                        
                                        "{d}","{touser}"),
                                        
                                        ("{ccc}",{var4},"{dt.datetime.now()}", {money},
                                        "{c}","{upiname}")''')
                                        con.commit()


                                        print(f'succesfully done, please check your balance!. Transaction id for reference: {var3}')
                                        exitchecker=True
                                        break
                                    
                                
                                    else:
                                        print('user not found, try again!')
                            else:
                                print(f'wrong pin!, you have {pincount} tries left')
                                pincount-=1
                                if pincount==-1:
                                    print('account locked')
                                    break

                except:
                    break
                            
                        
                
def checkbal():
    if checker==False:
        print('LOGIN BEFORE PROCEEDING')
    
    
    else:
        cu.execute(f'select Username from bank where email="{user}"')
        for i in cu:
            print(f'logged in as: "{i[0]}"')
            time.sleep(2)
        balchecks=False
        cu.execute(f'select bankpin from bank where email="{user}"')
        for j in cu:
            counter2=3
            while True:
                while True:
                    try:
                        pin=int(mp.askpass('enter pin: ',mask='*'))
                        break
                    except:
                        print('enter digits only!')
                        time.sleep(1)
                    
                if pin in j:
                    cu.execute(f'select balance from bank where email="{user}"')
                    for i in cu:
                        print(f'current balance: {i[0]}')
                        balchecks=True
                if balchecks:
                    break
                
                else:
                    print(f'wrong pin, you have {counter2} tries left!')
                    counter2-=1
                    if counter2==-1:
                        print('locked!')
                        break

                    
                    
                    
                    
def viewtran():
    if checker==False:
        print('LOGIN BEFORE PROCEEDING')
    
    
    else:
        cu.execute(f'select Username from bank where email="{user}"')
        for i in cu:
            print(f'logged in as: "{i[0]}"')
            time.sleep(1.2)
        while True:
            
            
            print('''
            1: VIEW ALL TRANSACTION HISTORY
            2: SELECT BY FILTER
            3: EXIT
            ''')
            time.sleep(1)
            getint('ENTER YOUR CHOICE: ')
            if intchecker:
                inputs=num
                if inputs==1:
                    translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                    cu.execute(f'select * from transactions where users_name="{user}"')
                    print('FETCHING DATA...')
                    time.sleep(1.3)
                    for i in cu:
                        translist.append(list(i))
                    print(tabulate(translist))

                    
                elif inputs==2:
                    translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                    selecter=input('select by filter(DATE/TRANSACTION ID/TYPE/UPI OF USER/AMOUNT): ' )
                    if selecter.upper()=="DATE":
                        date=input('enter date(YYYY-MM-DD)(tip: you can only enter the year/month of the transactions to get the data of that month/year only): ')
                        cu.execute(f'select * from transactions where transaction_date like "{date}%" and users_name="{user}"')
                        print('FETCHING DATA...')
                        time.sleep(2)
                        for i in cu:
                            translist.append(list(i))
                        print(tabulate(translist))
                            
                            
                    elif selecter.upper()=='TRANSACTION ID':
                        translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                        cu.execute(f'''select * from transactions where transaction_id = {int(input("Enter your transaction id: "))}
                        and users_name="{user}"''')
                        print('FETCHING DATA...')
                        time.sleep(2)
                        for i in cu:
                            translist.append(list(i))
                        print(tabulate(translist))
                                   
                    elif selecter.upper()=='AMOUNT':
                        translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                        cu.execute(f'''select * from transactions where transaction_amt = {int(input("Enter the amount: "))}
                        and users_name="{user}"''')
                        print('FETCHING DATA...')
                        time.sleep(2)
                        for i in cu:
                                translist.append(list(i))
                        print(tabulate(translist))

                    elif selecter.upper()=='UPI OF USER':
                        translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                        cu.execute(f'''select * from transactions where to_from_user like "{input("Enter the upi of user: ")}%"
                        and users_name="{user}"''')
                        print('FETCHING DATA...')
                        time.sleep(2)
                        for i in cu:
                                translist.append(list(i))
                        print(tabulate(translist))
                        
                    elif selecter.upper()=='TYPE':
                        translist=[['YOUR ID','TRANSACTION ID','DATE','AMOUNT','TYPE','UPI OF USER']]
                        cu.execute(f'''select * from transactions where CREDIT_OR_DEBIT = "{input("Enter type(CREDITED/DEBITED): ")}"
                        and users_name="{user}"''')
                        print('FETCHING DATA...')
                        time.sleep(2)
                        for i in cu:
                                translist.append(list(i))
                        print(tabulate(translist))
                                   
                    else:
                        print('invalid option')
                elif inputs==3:
                    break
                time.sleep(1.4)
            

def logout():
    global checker
    checker=False
    print('successfully logged out')
                

                    
            
            
            
                


def finalexecution():
    while True:
        if checker:
            
            print(f'''
            WELCOME TO BANK SIMULATION
            PLEASE PRESS THE BUTTONS ACCORIDING TO YOUR NEED:

            1: VIEW TRANSACTION HISTORY

            2: CHECK BALANCE 

            3: TRANSFER MONEY

            4: LOG OUT

            5: EXIT THE SIMULATION''')

            getint('ENTER YOUR CHOICE: ')
            if intchecker:
                inn=num

                if inn==1:
                    viewtran()
                elif inn==2:
                    checkbal()
                elif inn==3:
                    credit()
                elif inn==4:
                    logout()
                elif inn==5:
                    print('''
                        THANK YOU FOR USING THIS SIMULATION:
                        -DIVYANSH BHATIA: CREATOR OF THE CODE
                        -XII B SCIENCE
                        -THE KALYANI SCHOOL''')
                    time.sleep(2)
                    print('EXITING NOW...')
                    time.sleep(1)
                    sys.exit()
                time.sleep(1.3)

                b=input('EXIT? (Y/N)')
                if b.upper()=='Y':
                    print('''
                        THANK YOU FOR USING THIS SIMULATION:
                        -DIVYANSH BHATIA: CREATOR OF THE CODE
                        -XII B SCIENCE
                        -THE KALYANI SCHOOL''')
                    time.sleep(2)
                    print('EXITING NOW...')
                    time.sleep(1)
                    sys.exit()
        else:
            print(f'''
            WELCOME TO BANK SIMULATION:
            I)- PRESS 1 TO CREATE A NEW ACCOUNT
            
            II)- PRESS 2 TO LOGIN INTO YOUR ACCOUNT

            ''')
            
            inps=input('ENTER YOUR CHOICE(enter E to exit the code):  ')
            if inps=='1':
                CreateAcc()
            elif inps=='2':
                login()
                if checker:
                    cu.execute(f'select username from bank where email="{user}"')
                    for i in cu:
                        time.sleep(0.7)
                        print(f'WELCOME {i[0]} , redirecting you to the main page....')
                    time.sleep(2)
            elif inps.upper()=='E':
                print('''
                        THANK YOU FOR USING THIS SIMULATION:
                        -DIVYANSH BHATIA: CREATOR OF THE CODE
                        -XII B SCIENCE
                        -THE KALYANI SCHOOL''')
                time.sleep(0.5)
                print('exiting now...')
                time.sleep(2)
                sys.exit()
            
            



finalexecution()
