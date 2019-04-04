from django.shortcuts import render
from django.http import HttpResponseRedirect
from .MyStaticFunction import *

# Create your views here.
def LoadPage_index(request):
    if 'userName' not in request.session:
        request.session['userName'] = 'NULL'
    topFiveNews = loadTopNews(4)
    theSlide = loadTopSlide()
    Data = {'theloai': loadMenuSide(),'Slide': zip(theSlide,range(len(theSlide))),'Top5New':topFiveNews}
    return render(request,'pages/home.html',Data)
def LoadPage_GioiThieu(request):
    topFiveNews = Tin.objects.all()
    Data = {'theloai': loadMenuSide(),'TinTuc': topFiveNews}
    return render(request,'pages/GioiThieu.html',Data)
def LoadPage_loaitin(request,id):   
    topFiveNews = loadNewOfTLWithPage(id,3)
    loaiTinTen = loaitin.objects.get(idLoaiTin=id)
    Data = {'theloai': loadMenuSide(),'Top5New': topFiveNews,'LoaiTinTen': loaiTinTen}
    return render(request,'pages/loaitin.html',Data)
def LoadPage_chitiet(request, idTinTuc):
    Data = loadInfoOfChiTiet(idTinTuc)
    return render(request,'pages/chitiet.html',Data)
def LoadPage_dangky(request):
    if request.method == "POST":
        return render(request,'pages/dangky.html')
    return render(request,'pages/dangky.html')


def LoadPage_dangnhap(request):
    if request.method == "POST":
        if 'email' in request.POST:
            email = request.POST['email']
        if 'passWord' in request.POST:
            passWord = request.POST['passWord']      
        #request.session['userName'] = userName
        theUser = login(email,passWord)
        if theUser != None:
            request.session['userName'] = theUser['name']
            request.session['idUser'] = theUser['idUser']
        return LoadPage_index(request)       
    return render(request,'pages/dangnhap.html')
def LoadPage_taikhoan(request):
    return render(request,'pages/taikhoan.html')


def LoadPage_logout(request):
    request.session.flush()
    request.session.modified = True
    return LoadPage_index(request)



def LoadPage_test(request, idTin):
    a = Tin.objects.get(idTin=idTin)
    cms = a.comment_set.all()
    theUsers = []
    if cms:
        for cm in cms:
            idUser = getattr(cm.idUser,'idUser')
            name = users.objects.get(idUser = idUser)
            theUsers.append(name)
    dt = {'tin': a, 'comments': cms,'userName': theUsers}
    return render(request,'pages/justWatchInfo.html', dt)