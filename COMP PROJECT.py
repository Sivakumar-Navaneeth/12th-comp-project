import mysql.connector as sql
con=sql.connect(host='localhost',user='root',passwd='omega',database='food')
if con.is_connected():
    print('connection success') 
print('''
FFFFFFF      A         SSSSSSSS    TTTTTTTTTT
F           A A        S               T
FFFFFFF    A   A       SSSSSSSS        T
F         AAAAAAA             S        T
F         A      A            S        T
F         A      A     SSSSSSSS        T



FFFFFFF    OOOOOOOO      OOOOOOOO     DDDD   
F          O      O      O      O     D   D
FFFFFFF    O      O      O      O     D    D
F          O      O      O      O     D    D  
F          O      O      O      O     D   D
F          OOOOOOOO      OOOOOOOO     DDDD
 ''')

c=con.cursor()

print('''
1) start of day
2) after break''')

choice=int(input('enter choice: '))

if choice==1:
    q1="delete from customer"
    c.execute(q1)
    con.commit()
    #change menu to change the selling price of each item of a day or add more items
    y=input('wanna change the menu?(y/n)')
    if y=='y':
        d='delete from menu'
        c.execute(d)
        con.commit()
        t=True
        sno=1
        while t:
            item=input('item:')
            price=int(input('price of 1 item: '))
            ins ='insert into menu(sno,item,price) values (%s,%s,%s)'
            f=(sno,item,price)
            c.execute(ins,f)
            con.commit()
            y=input('wanna add more items?(y/n)')
            sno+=1
            if y=='y':
                continue
            else:
                t=False
                break
    #change sales to change the buying price of each item of a day or add more items
    y=input('wanna change the sales table?(y/n)')
    if y=='y':
        d='TRUNCATE TABLE sales'
        c.execute(d)
        con.commit()
        t=True
        sno=1
        while t:
            item=input('item:')
            quantity=0
            price=int(input('price of 1 item: '))
            total=0
            ins ='insert into sales(sno,item,quantity,price,total) values (%s,%s,%s,%s,%s)'
            f=(sno,item,quantity,price,total)
            c.execute(ins,f)
            con.commit()
            y=input('wanna add more items?(y/n)')
            sno+=1
            if y=='y':
                continue
            else:
                t=False
                break
    else:
        u='update sales set quantity=%s'%(0)
        v='update sales set total=%s'%(0)
        c.execute(u)
        c.execute(v)
        con.commit()
        print('WELCOME')

if choice==2:
    print('WELCOME BACK')

ono=1
t=True  
while t:
    print('''
1) see menu
2) take order in
3) cancel order
4) break
5) end of day''')
    choice=int(input('enter choice: '))

    if choice==1:
        c.execute('select * from menu')
        m=c.fetchall()
        for i in m:
            print(i)
        y=input('wanna order?(y/n)')
        if y=='y':
            choice=2
        else:
            print('NEXT CUSTOMER PLS')
            continue

    if choice==2:
        tot=0
        orr=[]
        while True:
            order=input('name one item: ')
            q=int(input('quantity of that item: '))
            c.execute('update sales set quantity=quantity+%s where item="%s"'%(q,order))
            con.commit()
            c=con.cursor()
            c.execute('select price from menu where item="%s"'%(order))
            x=c.fetchall()
            t1=int(x[0][0])*q
            tot+=t1
            c.execute('select price from sales where item="%s"'%(order))
            x1=c.fetchall()
            t2=int(x1[0][0])*q
            c.execute('update sales set total=%s where item="%s"'%(t2,order))
            con.commit()
            print('check order \n',order,'\n',t1,'\n','total=',tot)
            y=input('wanna continue?(y/n)')
            if y=='y':
                continue
            else:
                print('total bill amt is ',tot)
                g=int(input('how much would you like to pay: '))
                print('give change:',g-tot)
                break
        cname=input('cname:')
        cno=int(input('cno (enter your number):'))
        total=tot
        ins=('insert into customer values(%s,"%s",%s,%s)')
        qz=(ono,cname,cno,total)
        c.execute(ins,qz)
        con.commit()
        ono+=1
      #EVERY 100TH PERSON WHO ORDERS GETS A FREE BURGER
        if ono%100==0:
            print('''
CONGRATULATIONS      * *
YOU WON A FREE BURGER o ''')
            a=1
            o='veg burger'
            c.execute('update sales set quantity=quantity+%s where item="%s"'%(a,o))
            con.commit()
            c=con.cursor()
        print('NEXT CUSTOMER PLS')
        
    if choice==3:
      #changes happen in customer table and not in sales table as it is a loss for the franchise
        print('CANCELLATION OF TOTAL BILL')
        o=int(input('your order no:'))
        de='delete from customer where ono=%s'%(o)
        c.execute(de)
        con.commit()
        print('NEXT CUSTOMER PLS')
        
    if choice==4:
        print('RUN PROGRAM AGAIN TO COME BACK')
        break
    
    if choice==5:
    #shows sales table to see the number of people opting each item
        bye='select * from sales'
        c.execute(bye)
        byebye=c.fetchall()
        bye1='select * from customer'
        c.execute(bye1)
        byebye1=c.fetchall()
        for i in byebye:
            print(i)
        print('\n'*3)
        for i in byebye1:
            print(i)
        total='select sum(total) from sales'
        c.execute(total)
        sum1=c.fetchall()
        s1=int(sum1[0][0])
    #total amount of sales that day
        c.execute('select sum(total) from customer')
        sum2=c.fetchall()
        s2=int(sum2[0][0])
        tsum=s2-s1
        print('total sales today is ',s2)
    #shows if the franchise had a profit or a loss
        if tsum>0:
            print('total profit today is ',tsum)
        elif tsum<0:
            print('total loss today is ',-1*tsum)
        else:
            print('no profit no loss')
        a=0
        c.execute("select item from sales")
        x=c.fetchall()
        for i in x:
            l=i[0]
            c.execute("update sales set quantity=%s where item='%s'"%(a,l))
        print('BYE BYE')
        t=False
    
    if choice not in(1,2,3,4,5):
        print("enter proper value")
        continue 
