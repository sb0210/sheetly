from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from sheets.models import *
from django.http import HttpResponse
from django.utils import timezone
from django.core.signing import Signer
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.forms.models import model_to_dict
from django.db import connection
import sqlite3
import cgi
import base64
# Sign In/Sign Up ***************************************************************************************************

def login(request):
    user = request.user
    if user is not None and user.is_active:
        return redirect("/home/")
    return render(request,'login.html')

def signin(request):
    user = request.user
    if user is not None and user.is_active:
        return redirect("/home/")
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return redirect("/home/")
        else:
            return render(request,'login.html',{'error':"Wrong Credentials"})
    return HttpResponse("POST request required")

def signup(request):
    user = request.user
    if user is not None and user.is_active:
        return redirect("/home/")
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email_id = request.POST['email_id']

        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            return redirect("/home",{'error':"already registered"})    
        if "" in [username,password,name,email_id]:
            return render(request,"login.html",{'error':"Invalid form response. Missing one field."})

        users = User.objects.all()
        for u in users:
            if u.username == username:
                return render(request,'login.html',{'error':"Username Already taken"})
        _user = Users(username=username,password=password,name=name,email_id=email_id)
        _user.save()
        auth_user = User.objects.create_user(username=username,password=password,email=email_id,first_name=name)
        auth_user.save()

        return redirect("/login")
    return HttpResponse("POST request required")

def signout(request):
    auth.logout(request)
    return redirect("/")

def home(request):
    return redirect("/home/my_docs")

def my_docs(request):
    user = request.user
    print user
    if user.is_authenticated:
        user = Users.objects.get(username=user.username)
        docs = list(Documents.objects.raw("SELECT * FROM documents WHERE created_by=%s",[user.username]))
        signs = []
        permissions=[]
        signer = Signer(salt="GOD")
        for i in xrange(len(docs)):
            y = signer.sign(docs[i].doc_id)
            signs.append(signer.sign(docs[i].doc_id))
            signs[i] = "/home/docs/"+signs[i]+"/"
            permissions.append("edit")
        docs = serializers.serialize("json",docs)   
        return render(request,"home.html",{'docs':json.dumps(docs),'signs':json.dumps(signs),'permissions':json.dumps(permissions)})
    return redirect("/")    

def edit_data(request,  error=""):
    user = request.user
    print user
    if user.is_authenticated:
        user = Users.objects.get(username=user.username)
        name = request.POST['person']
        email = request.POST['mail']
        user.name = name
        user.email_id = email
        user.save()
        return redirect("/profile")
    return redirect("/")

def shared_docs(request):
    user = request.user
    print user
    if user.is_authenticated:
        user = Users.objects.get(username=user.username)
        docs = list(Documents.objects.raw("SELECT * FROM documents natural join ownership WHERE username=%s and created_by !=%s",[user.username,user.username]))      
        signs = []
        permissions=[]
        signer = Signer(salt="GOD")
        for i in xrange(len(docs)):
            y = signer.sign(docs[i].doc_id)
            signs.append(signer.sign(docs[i].doc_id))
            signs[i] = "/home/docs/"+signs[i]+"/"
            if(Ownership.objects.get(doc_id=docs[i].doc_id,username=user.username).rights=="edit"):
                permissions.append("edit")
            if(Ownership.objects.get(doc_id=docs[i].doc_id,username=user.username).rights=="view"):
                permissions.append("view")
        docs = serializers.serialize("json",docs)   
        return render(request,"share.html",{'docs':json.dumps(docs),'signs':json.dumps(signs),'permissions':json.dumps(permissions)})
    return redirect("/")    

def doc_create_page(request):
    user=check_auth(request)
    if user is not None:
        doc_name = request.POST['doc_name']
        created_on = timezone.now()
        created_by = Users.objects.get(username=user.username)
        doc = Documents(doc_name=doc_name,created_on=created_on,created_by=created_by)
        doc.save()
        owner =  Ownership(username=created_by,doc=doc,rights="edit")
        owner.save()
        return redirect("/home/")
    return HttpResponse("not authenticated")
        
def sheet_update_page(request,sheet_number):
    user=check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        table_data_JSON = request.POST.get('sheet_data')
        table_data=json.loads(table_data_JSON)
        for row_data in table_data:
            for data in row_data:
                cell=Cell.objects.get(cell_id=data['id'])
                data_objects=DataObject.objects.raw("SELECT * from has natural join data_object where cell_id = %s",[cell.cell_id])
                for data_object in data_objects:
                    if(data_object.data_type=="text"):
                        text =Text.objects.get(data=data_object)
                        text.text_data=data['data']
                        text.save()
                    # if(data_object.data_type=="image"):
                        # text =Text.objects.get(data=data_object)
                        # text.text_data=data['data']
                        # text.save()
                    # if(data_object.data_type=="video"):
                        # text =Text.objects.get(data=data_object)
                        # text.text_data=data['data']
                        # text.save()
        response_data={}
        response_data['result']=True
        return redirect(request.META.get('HTTP_REFERER'),{'id'})
    return HttpResponse("not authenticated")   

def doc_page(request,sheet_number):
    user = check_auth(request)
    if user is not None:
        if('current_sheet' in request.session.keys()):
            del request.session['current_sheet']
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user).exists():
            return HttpResponse("You dont have enough permissions")

        share_users = Ownership.objects.filter(doc=doc)
        rights=Ownership.objects.get(username=user.username,doc_id=doc_id).rights
        request.session['current_sheet'] = doc_id
        sheets = Sheets.objects.raw("SELECT * FROM sheets natural join contained_in WHERE doc_id = %s",[doc_id])
        sheets_json = serializers.serialize("json", sheets)
        doc = serializers.serialize("json", [doc])
        data_list=[]
        sheet_len=0
        for sheet in sheets:
            print sheet
            data=[]
            data_objects = DataObject.objects.raw("SELECT * from is_in,has, data_object where is_in.cell_id = has.cell_id and has.data_id=data_object.data_id and is_in.sheet_id = %s ORDER BY is_in.cell_id ",[sheet.pk])
            for data_object in data_objects:
                if(data_object.data_type=="text"):
                    text =Text.objects.get(data=data_object)
                    text=model_to_dict(text)
                    text['type']="text"
                    data.append(text)
                if(data_object.data_type=="image"):
                    text = Image.objects.get(data=data_object)
                    text=model_to_dict(text)
                    text['type']="image"
                    data.append(text)
                if(data_object.data_type=="video"):
                    text = Video.objects.get(data=data_object)
                    text=model_to_dict(text)
                    text['type']="video"
                    data.append(text)
            data_list.append(data)
            sheet_len=sheet_len+1  
        cells_list=[];         
        for sheet in sheets:
            cells = Cell.objects.raw("SELECT * from is_in natural join cell where sheet_id=%s ORDER BY cell_id",[sheet.pk])         
            cells =  serializers.serialize("json", cells)
            cells_list.append(cells)
        error=" "
        if('err' in request.session.keys()):
            error = request.session['err']
            del request.session['err']
        return render(request,"doc.html",{'doc':json.dumps(doc),'app_user':user,'sheets':sheets,'sheet_len':sheet_len,'share_users':share_users,
            'sheets_json':json.dumps(sheets_json),'cells':cells_list,'data':json.dumps(data_list),'sign':sheet_number,'permission':rights,'err':error})        
    return HttpResponse("You dont have enough permissions")

def sheet_create_page(request,sheet_number):
    user = check_auth(request)
    if user is not None:
        doc_id=request.session['current_sheet']
        doc = Documents.objects.get(doc_id=doc_id)
        sheet_name=request.POST['sheet_name']
        total_columns=request.POST['total_columns']
        total_rows=request.POST['total_rows']
        sheet_created_on = timezone.now()
        sheet_last_modified = timezone.now()
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        if total_rows.isdigit() and total_columns.isdigit():
            sheet = Sheets(sheet_name=sheet_name,total_columns=total_columns,total_rows=total_rows,sheet_last_modified=sheet_last_modified,sheet_created_on=sheet_created_on)
            sheet.save()
            contained_in = ContainedIn(doc=doc,sheet=sheet)
            contained_in.save()
            for i in xrange(int(total_rows)):
                for j in xrange(int(total_columns)):
                    cell = Cell(cell_x=j,cell_y=i,cell_color="white")
                    cell.save()
                    isin =IsIn(cell=cell,sheet=sheet)
                    isin.save()
                    data_object = DataObject(data_size=100,data_type="text")
                    data_object.save()
                    has = Has(data=data_object,cell=cell)
                    has.save()
                    text = Text(data=data_object,text_data=str(i*int(total_columns)+j),text_font="verdana",font_size=15,text_color="blue")
                    text.save()
            if('err' in request.session.keys()):
                del request.session['err']
            return redirect(request.META.get('HTTP_REFERER'))
        request.session['err']="Invalid input";
        print request.session['err']
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("You dont have enough permissions")

def doc_sharing_page(request,sheet_number):
    user = check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        rights=request.POST.get('rights')
        person=request.POST.get('person')
        persons=Users.objects.all()
        owners = Ownership.objects.raw("SELECT * FROM ownership WHERE doc_id = %s",[doc.pk])
        checker = None
        for own in owners:
            if own.username.username == person:
                if own.rights == rights:
                    request.session['err']="Already owns";
                    return redirect(request.META.get('HTTP_REFERER'))
                request.session['err']="Rights Changed";
                return redirect(request.META.get('HTTP_REFERER'))
                
        for per in persons:
            if per.username == person:
                owner =  Ownership(username=per,doc=doc,rights=rights)
                owner.save()
                if('err' in request.session.keys()):
                    del request.session['err']
                return redirect(request.META.get('HTTP_REFERER'))  
    request.session['err']="User Does not exist";
    return redirect(request.META.get('HTTP_REFERER'))          

def check_auth(request):
    user = request.user
    if user.is_authenticated and user.is_active:
        return user
    return None                   

def profile(request):
    user = check_auth(request)
    if user is not None:
        user =  Users.objects.get(username=user.username)
        print user
        return render(request,'profile.html',{'User':user})         
    return HttpResponse("You dont have enough permissions")

def add_column(request,sheet_number):
    user = check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        sheet_id = request.POST.get('sheet_number')
        sheet = Sheets.objects.get(sheet_id=sheet_id)
        total_rows=sheet.total_rows
        total_columns=sheet.total_columns
        sheet.total_columns=sheet.total_columns+1
        sheet.save()
        for i in xrange(int(total_rows)):
            cell = Cell(cell_x=sheet.total_columns-1,cell_y=i,cell_color="white")
            cell.save()
            isin =IsIn(cell=cell,sheet=sheet)
            isin.save()
            data_object = DataObject(data_size=100,data_type="text")
            data_object.save()
            has = Has(data=data_object,cell=cell)
            has.save()
            text = Text(data=data_object,text_data=str(i),text_font="verdana",font_size=15,text_color="blue")
            text.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("You dont have enough permissions")

def add_row(request,sheet_number):
    user = check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        sheet_id = request.POST.get('sheet_number')
        sheet = Sheets.objects.get(sheet_id=sheet_id)
        total_rows=sheet.total_rows
        total_columns=sheet.total_columns
        sheet.total_rows=sheet.total_rows+1
        sheet.save()
        for i in xrange(int(total_columns)):
            cell = Cell(cell_x=i,cell_y=sheet.total_rows-1,cell_color="white")
            cell.save()
            isin =IsIn(cell=cell,sheet=sheet)
            isin.save()
            data_object = DataObject(data_size=100,data_type="text")
            data_object.save()
            has = Has(data=data_object,cell=cell)
            has.save()
            text = Text(data=data_object,text_data=str(i),text_font="verdana",font_size=15,text_color="blue")
            text.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("You dont have enough permissions")

def delete_data(request,sheet_number):
    user= check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        sheet_id = request.POST.get('sheet_number')
        sheet= Sheets.objects.get(sheet_id=int(sheet_id))
        print request.POST
        cols = request.POST.get('selected_columns')
        rows = request.POST.get('selected_rows')
        if cols!=None: 
            total_columns = sheet.total_columns
            total_rows = sheet.total_rows
            cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
            print cols
            for cell in cells:
                if(cell.cell_x==int(cols)):
                    data_objects=DataObject.objects.raw("SELECT * from has natural join data_object where cell_id = %s",[cell.cell_id])
                    for data_object in data_objects:
                        if data_object.data_type=="text":
                            Text.objects.get(data=data_object).delete()
                        if data_object.data_type=="image":
                            Image.objects.get(data=data_object).delete()
                        if data_object.data_type=="video":
                            Video.objects.get(data=data_object).delete()
                    data_object.delete()
                    Cell.objects.get(cell_id=cell.cell_id).delete()
                if(cell.cell_x>int(cols)):
                    c = Cell.objects.get(cell_id=cell.cell_id)
                    c.cell_x=c.cell_x-1
                    c.save()
            cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
            if(sheet.total_columns>0):
                sheet.total_columns=sheet.total_columns-1
                sheet.save()
        if rows!=None: 
            total_columns = sheet.total_columns
            total_rows = sheet.total_rows
            cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
            print cols
            for cell in cells:
                if(cell.cell_y==int(rows)):
                    data_objects=DataObject.objects.raw("SELECT * from has natural join data_object where cell_id = %s",[cell.cell_id])
                    for data_object in data_objects:
                        if data_object.data_type=="text":
                            Text.objects.get(data=data_object).delete()
                        if data_object.data_type=="image":
                            Image.objects.get(data=data_object).delete()
                        if data_object.data_type=="video":
                            Video.objects.get(data=data_object).delete()
                    data_object.delete()
                    Cell.objects.get(cell_id=cell.cell_id).delete()
                if(cell.cell_y>int(rows)):
                    c = Cell.objects.get(cell_id=cell.cell_id)
                    c.cell_y=c.cell_y-1
                    c.save()
            cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
            if(sheet.total_rows>0):
                sheet.total_rows=sheet.total_rows-1
                sheet.save()

    return redirect(request.META.get('HTTP_REFERER'))

def delete_sheet(request,sheet_number):
    user= check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        sheet_id = request.POST.get('sheet_number')
        sheet = Sheets.objects.get(sheet_id=sheet_id)
        cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
        for cell in cells:
            data_objects=DataObject.objects.raw("SELECT * from has natural join data_object where cell_id = %s",[cell.cell_id])
            for data_object in data_objects:
                if data_object.data_type=="text":
                    Text.objects.get(data=data_object).delete()
                if data_object.data_type=="image":
                    Image.objects.get(data=data_object).delete()
                if data_object.data_type=="video":
                    Video.objects.get(data=data_object).delete()
            data_object.delete()
            cell.delete()
        sheet.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def delete_doc(request,sheet_number):
    user= check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        document = Documents.objects.get(doc_id=doc_id)
        sheets = Sheets.objects.raw("SELECT * FROM sheets natural join contained_in WHERE doc_id = %s",[doc_id])
        for sheet in sheets:
            cells = Cell.objects.raw("SELECT * FROM cell natural join is_in WHERE sheet_id = %s",[sheet.pk])
            for cell in cells:
                data_objects=DataObject.objects.raw("SELECT * from has natural join data_object where cell_id = %s",[cell.cell_id])
                for data_object in data_objects:
                    if data_object.data_type=="text":
                        Text.objects.get(data=data_object).delete()
                    if data_object.data_type=="image":
                        Image.objects.get(data=data_object).delete()
                    if data_object.data_type=="video":
                        Video.objects.get(data=data_object).delete()
                data_object.delete()
                cell.delete()
            sheet.delete()
        document.delete()
    return redirect("/home/")        

def rename_doc(request,sheet_number):
    user= check_auth(request)
    if user is not None:
        signer = Signer(salt="GOD")
        doc_id = signer.unsign(sheet_number)
        doc = Documents.objects.get(doc_id=doc_id)
        user = Users.objects.get(username=user.username)
        if not Ownership.objects.filter(doc=doc,username=user,rights="edit").exists():
            return HttpResponse("You dont have enough permissions")
        name = request.GET.get('new_name')
        document = Documents.objects.get(doc_id=doc_id)
        document.doc_name=name
        document.save() 
    return redirect("/home/")        

def delete_everything(request):
    user= check_auth(request)
    if user.username == 'admin':
        Text.objects.all().delete()
        Video.objects.all().delete()
        Image.objects.all().delete()
        DataObject.objects.all().delete()
        Cell.objects.all().delete()
        Sheets.objects.all().delete()
        Documents.objects.all().delete()

        return HttpResponse("Everything is deleted") 
    return HttpResponse("You dont have enough permissions")


def upload_image(request,sheet_number,data):
    user=check_auth(request)
    if user is not None:        
        image =  request.FILES['image']
        image_title =  request.FILES['image_title']
        row = request.post.get('row')
        col = request.post.get('col')

        cursor = connection.cursor()
        Image(data=data,image_data=sqlite3.Binary(image.read()),image_title=image_title)
        print row
        img ='<html><img  src="data:image/jpeg;base64,'+base64.b64encode(row[1])+'"/></html>'
        return HttpResponse(img)
    return HttpResponse("You dont have enough permissions")


def filesvideo(request):
    file1 =  request.FILES['video']
    cursor = connection.cursor()
    cursor.execute('INSERT into Video (video_data,video_title) values (?,?)',(sqlite3.Binary(file1.read())),"Video Random Title")
    return HttpResponse("successfully uploaded")