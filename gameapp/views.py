from django.shortcuts import render,HttpResponseRedirect,HttpResponse

from django.core.files.storage import FileSystemStorage
import webbrowser
import datetime

import MySQLdb
db=MySQLdb.connect("localhost","root","","game")
c=db.cursor()



def index(request):
    return render(request,"common/index.html")

def adminhome(request):
    return render(request,"admin/adminhome.html")

def userhome(request):
    return render(request,"user/userhome.html")


def login(request):
    return render(request,"common/login.html")

def login1(request):
    msg=""
    if request.POST:
        uname=request.POST.get("uname")
        password=request.POST.get("password")
       
        request.session['uname']=uname
        print(uname)
        print(password)
        query="select * from login where uname='"+uname+"' and password='"+password+"'"
        c.execute(query)
        data=c.fetchone()
        print(data)
        if data:
            if data[2]=='admin':
                return HttpResponseRedirect("/adminhome/")
            
            elif data[2]=='user' and data[3]=="approved":
                print("hello")
                a="select cid from user where email='"+str(uname)+"'"
                c.execute(a)
                userid=c.fetchone()
                print(a)
                print(userid)
                request.session['userid']=userid[0]
                return HttpResponseRedirect("/userhome/")
        else:
            msg="invalid username or password"
           


    return render(request,"common/login.html")


def userreg(request):
    if request.POST:
        name=request.POST.get("name")
        address=request.POST.get("address")
        district=request.POST.get("district")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        password=request.POST.get("password")
        query="insert into user(name,address,district,email,phoneno) values('"+str(name)+"','"+str(address)+"','"+str(district)+"','"+str(email)+"','"+str(phoneno)+"')"
        c.execute(query)
        db.commit()
        usertype='user'
        status='approved'
        query="insert into login(uname,password,usertype,status) values('"+str(email)+"','"+str(password)+"','"+str(usertype)+"','"+str(status)+"')"
        c.execute(query)
        db.commit()
       
    return render(request,"user/userreg.html")

# Create your views here.

#add category


def addcategory(request):
    if request.POST:
        categoryname=request.POST.get("categoryname")
        if request.FILES["image1"]:
                myfile=request.FILES["image1"]
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                image1=fs.url(filename)
        
        query="insert into category(categoryname,image) values('"+str(categoryname)+"','"+str(image1)+"')"
        c.execute(query)
        db.commit()
       
    return render(request,"admin/addcategory.html")



def adminviewuser(request):
    c.execute("select * from user")
    data=c.fetchall()   
    return render(request,"admin/viewusers.html",{"data":data})





def adminviewpayment(request):
    c.execute("SELECT product.*,payment.*,user.* FROM (payment inner join product on payment.pid=product.pid) inner join user on payment.uid=user.cid")
    data=c.fetchall()   
    return render(request,"admin/viewpayment.html",{"data":data})


def adminviewbooking(request):
    c.execute("select booking.*,product.* from booking join product on booking.pid=product.pid where booking.status='booked'")
    data=c.fetchall()   
    return render(request,"admin/viewbooking.html",{"data":data})




def adminaddproduct(request):
    c.execute("select * from category")
    data1=c.fetchall() 

    if request.POST:
        productname=request.POST.get("productname")
        category=request.POST.get("category")
        
        discription=request.POST.get("discription")
        price=request.POST.get("price")
        if request.FILES["image1"]:
                myfile=request.FILES["image1"]
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                image1=fs.url(filename)
        if request.FILES["image2"]:
                myfile=request.FILES["image2"]
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                image2=fs.url(filename)
        if request.FILES["image3"]:
                myfile=request.FILES["image3"]
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                image3=fs.url(filename)
        if request.FILES["game"]:
                myfile=request.FILES["game"]
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                game=fs.url(filename)
        
        

        
        query="insert into product (productname,category,description,image1,image2,image3,game,price) values('"+str(productname)+"','"+str(category)+"','"+str(discription)+"','"+str(image1)+"','"+str(image2)+"','"+str(image3)+"','"+str(game)+"','"+str(price)+"')"
        c.execute(query)
        db.commit()
        
       
    return render(request,"admin/addproduct.html",{"data":data1})


def adminviewdemand(request):
    c.execute("select * from demand")
    data=c.fetchall()   
    return render(request,"admin/viewdemand.html",{"data":data})











#user


def payment(request):
    if request.GET.get("pid"):
        request.session["productid"]=request.GET.get("pid")
        pid=request.GET.get("pid")
        amount=request.session["amount"]
        request.session["pid"]=pid
        c.execute("select * from product where pid='"+str(pid)+"' ")
        data=c.fetchone()
        request.session["amount"]=data[4]
    if request.POST:
        return HttpResponseRedirect("/payment1/")

    return render(request,"user/payment1.html")


def payment1(request):
    amount=request.session["amount"]
    if request.POST:
        amount=request.session["amount"]
        
        bid=request.session["productid"]
        uid=request.session["userid"]
        date=datetime.date.today()
        print(date)
        query="insert into payment (uid,pid,amount,date) values('"+str(uid)+"','"+str(bid)+"','"+str(amount)+"','"+str(date)+"')"
        c.execute(query)
        db.commit()


        return HttpResponseRedirect("/payment2/")
    return render(request,"user/payment2.html",{"amount":amount})
def payment2(request):
    if request.POST:

        return HttpResponseRedirect("/payment3/")
    return render(request,"user/payment3.html")
def payment3(request):
    if request.POST:
        return HttpResponseRedirect("/payment4/")
    return render(request,"user/payment4.html")
def payment4(request):
    pid=request.session["pid"]
    c.execute("select * from product where pid='"+str(pid)+"'")
    data=c.fetchone() 
    return render(request,"user/downloadproduct.html",{"data":data})

def download(request):
    file_name = request.GET.get('file_name')
    path_to_file = "/media/".format(file_name)
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response 
    
    

    # return render(request,"user/downloadproduct.html",{"data":data})


def viewbookingbyuser(request):
    c.execute("select booking.*,product.* from booking join product on  booking.pid=product.pid where booking.uid='"+str(request.session['userid'])+"'")
    data=c.fetchall()   
    return render(request,"user/viewbookingsbyuser.html",{"data":data})



def viewcategory(request):
    c.execute("select * from category")
    data=c.fetchall()   
    return render(request,"user/viewcategory.html",{"data":data})

def viewgames(request):
    if request.GET.get("category"):
        category=request.GET.get("category")
        c.execute("select * from product where category='"+str(category)+"'")
        data=c.fetchall() 
        amount=data[0][4]  
        request.session["amount"]=amount
        return render(request,"user/viewgames.html",{"data":data})
    return render(request,"user/viewgames.html",{"data":data})




def demandgame(request):
    c.execute("select * from category")
    data1=c.fetchall() 
    if request.POST:
        productname=request.POST.get("productname")
        category=request.POST.get("category")
        discription=request.POST.get("discription")
        query="insert into demand (gamename,category,description) values('"+str(productname)+"','"+str(category)+"','"+str(discription)+"')"
        c.execute(query)
        db.commit()  
    return render(request,"user/demandgame.html",{"data":data1})



def askq(request):
    c.execute("select * from product")
    data1=c.fetchall() 
    if request.POST:
        game=request.POST.get("game")
        c.execute("select askq.*,answer.* from askq join answer on askq.askqid=answer.qid where game='"+str(game)+"'")
        data2=c.fetchall()
        return render(request,"user/askq.html",{"data":data1,"data2":data2})
        
    return render(request,"user/askq.html",{"data":data1})

def answerq(request):
    if request.GET.get("id"):
        idd=request.GET.get("id")
    if request.POST:
        answer=request.POST.get("answer")
        uid=request.session["userid"]    
        
        query="insert into answer (uid,qid,answer) values('"+str(uid)+"','"+str(idd)+"','"+str(answer)+"')"
        c.execute(query)
        db.commit()  
    return render(request,"user/answerq.html")

def question(request):
    c.execute("select * from product")
    data1=c.fetchall() 
    if request.POST:
        game=request.POST.get("game")
        question=request.POST.get("question")
        uid=request.session["userid"]    
        
        query="insert into askq (uid,game,question) values('"+str(uid)+"','"+str(game)+"','"+str(question)+"')"
        c.execute(query)
        db.commit()  
    return render(request,"user/question.html",{"data":data1})


def viewquestion(request):
    c.execute("select * from product")
    data1=c.fetchall() 
    if request.POST:
        game=request.POST.get("game")
        c.execute("select * from askq where game='"+str(game)+"'")
        data2=c.fetchall()
        return render(request,"user/viewquestion.html",{"data":data1,"data2":data2})
        
    return render(request,"user/viewquestion.html",{"data":data1})