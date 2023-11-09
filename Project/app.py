from flask import Flask, render_template, request,session,redirect
import datetime
current_datetime = datetime.datetime.now()
current_date = current_datetime.date()
from datetime import datetime
app = Flask(__name__)
app.secret_key ='cos'
tmp=0
a=''
b=''
c=''
dd=1
e=''
f=''
nam=''
na=''
uid=''
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;UID=ttj61869;PWD=YHlu0LMhc7RrrsgV","","")
print(conn)
print("connection success")
def inst(conn,name,date,time,slot,port,consume):
    sql= f"INSERT INTO {name} VALUES('{date}','{time}','{slot}','{port}','{consume}') "
    stmt = ibm_db.exec_immediate(conn,sql)
def tab(conn,a):
    sql= f"CREATE TABLE {a} (date DATE,time TIME,station VARCHAR(128),slot INT,consume VARCHAR(32))"
    stmt = ibm_db.exec_immediate(conn, sql)
def insertdb(conn,name,email,contact,address,brand,model,VIN,battery,ct,username,password):
    sql= "INSERT into auth VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(name,email,contact,address,brand,model,VIN,battery,ct,username,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))
    sql= f"CREATE TABLE {username} (date DATE,time TIME,station CHAR(128),slot INT,port CHAR(64),consume CHAR(64),totime CHAR(64))"
    stmt = ibm_db.exec_immediate(conn, sql)
def r1():
    return render_template('register.html')
@app.route('/')
def index():
    return render_template('entry.html')
@app.route('/get')
def ind():
    return render_template('entry.html')
@app.route('/home')
def home():
    return render_template('home.html',name=uid)
@app.route('/login' ,methods=['POST','GET'])
def login():
    if request.method == "POST":
        userid=request.form['userid']
        password=request.form['password']
        sql= "select * from  auth where username='{}' and password='{}'".format(userid,password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        if userdetails:
            session['register'] =userdetails["USERNAME"]
            session['register'] =userdetails["PASSWORD"]
            global uid
            uid=userdetails["USERNAME"]
            return render_template('home.html',name=uid)
        else:
            msg = "Incorrect Email id or Password"
            return render_template("login-page.html", msg=msg)

    return render_template('login-page.html')
@app.route('/register' ,methods=['POST','GET'])
def register():
    print(r1())
    abc = "Registered successfully"
    cc="Login Here"
    if request.method == "POST":
        name=request.form['name'] 
        print("welc")
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']
        brand=request.form['brand']
        model=request.form['model']
        VIN=request.form['vin']
        battery=request.form['Battery']
        ct=request.form['connector-type']
        if ct=="0":
            ct="Type 1 (J1772)"
        elif ct=="1":
            ct="Type 2 (Mennekes)"
        elif ct=="2":
            ct="CHAdeMO" 
        elif ct=="3":
            ct="CCS (Combined Charging System)"
        elif ct=="4":
            ct="Tesla Supercharger Connector"
        elif ct=="5":
            ct="GB/T (Guan Biao/T-Plug)"
        elif ct=="6":
            ct="IEC 60309 (Industrial Red/Blue Plugs)"
        elif ct=="7":
            ct="GB/T 20234.2-2011"
        elif ct=="8":
            ct="Three-Phase"
        elif ct=="9":
            ct="Single-Phase"
        username=request.form['username']
        password=request.form['password']
        sql= "select * from  auth where username='{}' ".format(username)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        if userdetails:
            session['register'] =userdetails["USERNAME"]
            return render_template('register.html',abc="Username Already Exist")
        else:
            insertdb(conn,name,email,contact,address,brand,model,VIN,battery,ct,username,password)
            return render_template("register.html", abc=abc)
    return render_template("register.html")
@app.route('/reserve')
def reserve():
    return render_template('index.html')
@app.route('/view')
def view():
    sql= "select name,location,port from STATIONS"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    n=0
    list=[]
    while dictionary != False:
        st=dictionary["NAME"]
        st1=str(st)
        st=dictionary["LOCATION"]
        st2=str(st)
        st=dictionary["PORT"]
        st3=str(st)
        list.append([st1,st2,st3])
        n+=1
        dictionary = ibm_db.fetch_both(stmt)
    return render_template('viewall.html',items=n,list=list)
@app.route('/part' ,methods=['POST','GET'])
def show1():
    if request.method == 'POST':
        a=request.form['sub']
        a=int(a)
        sql= "select name from STATIONS"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        n=0
        list=[]
        while dictionary != False:
            st=dictionary["NAME"]
            list.append(st)
            n+=1
            dictionary = ibm_db.fetch_both(stmt)
        s=list[a-1]
        sql=f"SELECT * FROM stations where name= '{s}' "
        stmt=ibm_db.exec_immediate(conn,sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            global na
            na=dictionary["NAME"]
            global nam
            nam=na
            global b
            b=dictionary["LOCATION"]
            global c
            c=dictionary["CONTACT"]
            global dd
            d=dictionary["SLOTS"]
            dd=int(d)
            global e
            e=dictionary["PORT"]
            global f
            f=dictionary["ID"]
            dictionary = ibm_db.fetch_both(stmt)
        print(na)
        return render_template('particular.html',a=na,b=b,c=c,d=dd,e=e,f=f,abc="Make a Reservation")
    print(na,b,c,dd,e)
    return render_template('particular.html',a=na,b=b,c=c,d=dd,e=e,f=f,abc="Slot already taken ")
@app.route('/resconfirm', methods=['POST','GET'])
def conf():
    if request.method == 'POST' :
        global name
        name=request.form['name']
        global date
        date=request.form['date']
        global time
        time=request.form['time']
        global units
        units=request.form['units']
        global port
        port=request.form['port']
        global slot
        slot=request.form['slot']
        print(name,date,time,slot,port,units)
        sql=f"SELECT date,time,slot FROM {name} WHERE date='{date}' and time='{time}' and slot={slot}"
        stmt=ibm_db.exec_immediate(conn,sql)
        dict=ibm_db.fetch_both(stmt)
        if dict:
            session['register'] =dict["DATE"]
            session['register'] =dict["TIME"]
            session['register'] =dict["SLOT"]
            print(dict["DATE"])
            return redirect('/part')
        else :
            global tmp
            tmp=int(units)/15
            print(na)
            cost=int(units)*12;
            print(units,cost)
            return render_template('con.html',a=na,b=b,c=port,d=date,e=time,f=f"{tmp:.2f}",h=slot,cost=cost)
@app.route('/confirm')
def final():
    return render_template('estimate.html')
@app.route('/est')
def esti():
    tm=f"{tmp:.2f}"
    inst(conn,name,date,time,slot,port,units)
    sql=f"INSERT INTO {uid} VALUES('{date}','{time}','{na}','{slot}','{port}','{units}','{tm}')"
    stmt=ibm_db.exec_immediate(conn,sql)
    return render_template('estimate.html')
@app.route('/search' , methods=['POST','GET'])
def search():
    if request.method == 'POST':
        sn=request.form['see']
        sql=f"SELECT * FROM stations where name= '{sn}' "
        stmt=ibm_db.exec_immediate(conn,sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            na=dictionary["NAME"]
            global b
            b=dictionary["LOCATION"]
            global c
            c=dictionary["CONTACT"]
            global dd
            d=dictionary["SLOTS"]
            dd=int(d)
            global e
            e=dictionary["PORT"]
            global f
            f=dictionary["ID"]
            dictionary = ibm_db.fetch_both(stmt)
        return render_template('particular.html',a=na,b=b,c=c,d=dd,e=e,f=f,abc="Make a Reservation")
@app.route('/fav',methods=['POST','GET'])
def fav():
    sql= "select * from  favstations where username='{}' and station='{}'".format(uid,nam)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    n=0
    l=[]
    if userdetails:
        session['register'] =userdetails["USERNAME"]
        session['register'] =userdetails["STATION"]
        sql1=f"SELECT * FROM favstations where username='{uid}' "
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_assoc(stmt1)
        while True:
            la=[]
            for i,j in st.items():
                la.append(j)
            l.append(la)
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
            if not st:
                break
            print(n)
        return render_template('fav.html',n=int(n),l=l)
    else:
        num=0
        sql= "SELECT username FROM favstations"
        stmt=ibm_db.exec_immediate(conn,sql)
        dict=ibm_db.fetch_both(stmt)
        while dict!=False:
            num=num+1
            dict=ibm_db.fetch_both(stmt)
        print(num)
        sql=f"SELECT * FROM stations where name= '{nam}' "
        stmt=ibm_db.exec_immediate(conn,sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            b=dictionary["LOCATION"]
            c=dictionary["CONTACT"]
            d=dictionary["SLOTS"]
            dd=int(d)
            q=dictionary["ID"]
            qq=q
            dictionary = ibm_db.fetch_both(stmt)
        sql1=" INSERT INTO favstations VALUES('{}','{}','{}','{}','{}','{}')".format(uid,qq,nam,b,c,dd)
        stmt1=ibm_db.exec_immediate(conn,sql1)
        sql1=f"SELECT * FROM favstations where username='{uid}' "
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_assoc(stmt1)
        while True:
            la=[]
            for i,j in st.items():
                la.append(j)
            l.append(la)
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
            if not st:
                break
            print(n)
        return render_template('fav.html',n=int(n),l=l)
@app.route('/fav1')
def dis():
    l=[]
    n=0
    sql1=f"SELECT * FROM favstations where username='{uid}' "
    stmt1=ibm_db.exec_immediate(conn,sql1)
    st=ibm_db.fetch_assoc(stmt1)
    while True:
        la=[]
        for i,j in st.items():
            la.append(j)
        l.append(la)
        n+=1
        st=ibm_db.fetch_assoc(stmt1)
        if not st:
            break
    return render_template('fav.html',n=int(n),l=l)
@app.route('/favdelt',methods=['POST','GET'])
def delt():
    print("welcome")
    if request.method == 'POST':
        print("oye")
        tpp=request.form['del']
        tp=int(tpp)
        print(tpp)
        n=0
        sql1=f"SELECT * FROM stations"
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_both(stmt1)
        while st:
            if(n!=int(tp)):
                print("count")
            else:
                stm=st["NAME"]
                p="SELECT station FROM favstations WHERE username='{uid}' "
                q=ibm_db.exec_immediate(conn,p)
                r=ibm_db.fetch_both(q)
                flag=0
                while r:
                    y=r["STATION"]
                    if y!=stm:
                        flag=1
                    r=ibm_db.fetch_both(q)
                if flag==1:
                    tp+=1
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
        n=0
        print(stm)
        sql1=f"SELECT * FROM favstations where username='{uid}' and station='{stm}' "
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_both(stmt1)
        while st:
            if(n!=int(tpp)):
                print("count")
            else:
                sql=f" DELETE FROM favstations WHERE username='{uid}' and station='{stm}' "
                stmt=ibm_db.exec_immediate(conn,sql)
                print("defe")
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
        return redirect('/fav1')
@app.route('/favins',methods=['POST','GET'])
def favins():
    if request.method == 'POST':
        print("oye")
        tpp=request.form['del']
        tp=int(tpp)
        print(tpp)
        n=0
        sql1=f"SELECT * FROM stations"
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_both(stmt1)
        while st:
            if(n!=int(tp)):
                print("count")
            else:
                stm=st["NAME"]
                print(stm)
                p="SELECT station FROM favstations WHERE username='{uid}' "
                q=ibm_db.exec_immediate(conn,p)
                r=ibm_db.fetch_both(q)
                flag=0
                while r:
                    y=r["STATION"]
                    if y!=stm:
                        flag=1
                    r=ibm_db.fetch_both(q)
                if flag==1:
                    tp+=1
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
        n=0
        sql=f"SELECT * FROM stations where name= '{stm}' "
        stmt=ibm_db.exec_immediate(conn,sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            global na
            na=dictionary["NAME"]
            global b
            b=dictionary["LOCATION"]
            global c
            c=dictionary["CONTACT"]
            global dd
            d=dictionary["SLOTS"]
            dd=int(d)
            global e
            e=dictionary["PORT"]
            global f
            f=dictionary["ID"]
            dictionary = ibm_db.fetch_both(stmt)
        return render_template('particular.html',a=na,b=b,c=c,d=dd,e=e,f=f,abc="Make a Reservation")
@app.route('/status',methods=['POST','GET'])
def status():
    l=[]
    n=0
    sql1=f"SELECT * FROM {uid} "
    stmt1=ibm_db.exec_immediate(conn,sql1)
    st=ibm_db.fetch_assoc(stmt1)
    while True:
        la=[]
        for i,j in st.items():
            la.append(j)
        l.append(la)
        n+=1
        st=ibm_db.fetch_assoc(stmt1)
        if not st:
            break
    current_time = current_datetime.time()
    ask=current_time
    ft=current_time.strftime("%H:%M:%S")
    current_time=datetime.strptime(ft,"%H:%M:%S")
    ask=current_time.time()
    print("check")
    print(l)
    return render_template('station-status.html',n=int(n),l=l,cd=current_date,ct=ask)
@app.route('/statusdel',methods=['POST','GET'])
def statusdel():
    if request.method == 'POST':
        print("oye")
        tpp=request.form['del']
        tp=int(tpp)
        print(tpp)
        n=0
        sql1=f"SELECT * FROM stations"
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_both(stmt1)
        while st:
            if(n!=int(tp)):
                print("count")
            else:
                stm=st["NAME"]
                p=f"SELECT * FROM {uid} "
                q=ibm_db.exec_immediate(conn,p)
                r=ibm_db.fetch_both(q)
                flag=0
                while r:
                    y=r["STATION"]
                    if y==stm:
                        flag=1
                    print(stm,y)
                    r=ibm_db.fetch_both(q)
                if flag!=1:
                    tp+=1
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
        n=0
        sql1=f"SELECT * FROM {uid} "
        stmt1=ibm_db.exec_immediate(conn,sql1)
        st=ibm_db.fetch_both(stmt1)
        while st:
            if(n!=int(tpp)):
                print("count")
            else:
                sql=f" DELETE FROM {uid} WHERE station= '{stm}' "
                stmt=ibm_db.exec_immediate(conn,sql)
                print("defe")
            n+=1
            st=ibm_db.fetch_assoc(stmt1)
        return redirect('/status')
@app.route('/history' ,methods=['POST','GET'])
def hist():
    l=[]
    n=0
    sql1=f"SELECT * FROM {uid} "
    stmt1=ibm_db.exec_immediate(conn,sql1)
    st=ibm_db.fetch_assoc(stmt1)
    while True:
        la=[]
        for i,j in st.items():
            la.append(j)
        l.append(la)
        n+=1
        st=ibm_db.fetch_assoc(stmt1)
        if not st:
            break
    current_time = current_datetime.time()
    ask=current_time
    ft=current_time.strftime("%H:%M:%S")
    current_time=datetime.strptime(ft,"%H:%M:%S")
    ask=current_time.time()
    return render_template('chargehist.html',n=int(n),l=l,cd=current_date,ct=ask)
@app.route('/prof',methods=['POST','GET'])
def profile():
    sql=f"SELECT * FROM auth where username= '{uid}' "
    stmt=ibm_db.exec_immediate(conn,sql)
    dict=ibm_db.fetch_both(stmt)
    while dict:
        name=dict["NAME"]
        mail=dict["EMAIL"]
        contact=dict["CONTACT"]
        location=dict["ADDRESS"]
        brand=dict["BRAND"]
        model=dict["MODEL"]
        vin=dict["VIN"]
        bt=dict["BATTERY"]
        ct=dict["CT"]
        dict=ibm_db.fetch_both(stmt)
    return render_template('profile.html',name=name,mail=mail,contact=contact,location=location,brand=brand,model=model,vin=vin,battery=bt,port=ct)
@app.route('/trip',methods=['POST','GET'])
def tripp():
    return render_template('trip.html')
if __name__ =='__main__':
    app.run(debug = True)
