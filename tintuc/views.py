from django.shortcuts import render
from django.http import HttpResponseRedirect
from .MyStaticFunction import *
#<<<<<<< HEAD
from .paginationOfLT import *
#=======
from .user import *
#>>>>>>> cfb7e0cad8314dd62f76cc0e1e3fd60327f97eca

# Create your views here.
thePagination = paginationOfLT(0)
def LoadPage_index(request):
    if 'userName' not in request.session:
        request.session['userName'] = 'NULL'
    topFiveNews = loadTopNews(4)
    theSlide = loadTopSlide()
    Data = {'theloai': loadMenuSide(),'Slide': zip(theSlide,range(len(theSlide))),'Top5New':topFiveNews}
    return render(request,'pages/home.html',Data)



def LoadPage_GioiThieu(request):
    topFiveNews = Tin.objects.all()[0:5]
    Data = {'theloai': loadMenuSide(),'TinTuc': topFiveNews}
    return render(request,'pages/GioiThieu.html',Data)


# Lấy thông tin trang loaitin
def LoadPage_loaitin(request, id, page = 1):
    thePagination.setId(id)
    loaiTinTen = loaitin.objects.get(idLoaiTin=id)
    thePagination.nowPage = page
    topNews = thePagination.getNewsInNowPage()
    Data = {'theloai': loadMenuSide(),'TopNews': topNews,'LoaiTinTen': loaiTinTen, 'idLoaiTin': id,
    'nowPage':thePagination.nowPage,'maxPage': thePagination.maxPage,'theRangePages':thePagination.getRangePage()}
    return render(request,'pages/loaitin.html',Data)



# Lấy view trang chitiet
def LoadPage_chitiet(request, idTinTuc):
    if request.method == "GET":
        if 'commentContent' in request.GET and 'idUser' in request.session:
            addNewComment(request.session['idUser'],idTinTuc, request.GET['commentContent'])
    Data = loadInfoOfChiTiet(idTinTuc)
    return render(request,'pages/chitiet.html',Data)



def LoadPage_dangky(request):
    if request.method=='POST':
        form=RegistrationFrom(request.POST)
        if form.is_valid():
            name=request.POST.get('name','')
            email=request.POST.get('email','')
            password=request.POST.get('password1','')
            user_obj=users(name=name,email=email,password=password)
            user_obj.save()
            return HttpResponseRedirect('/')
    else:
        form=RegistrationFrom()
    return render(request,'pages/dangky.html',{'form': form})


def LoadPage_dangnhap(request):
    error = 'None'
    # Kiểm tra thông tin đăng nhập có hay ko
    if request.method == "POST":
        if 'email' in request.POST:
            email = request.POST['email']
        if 'passWord' in request.POST:
            passWord = request.POST['passWord']     
            
        theUser = checkLogin(email,passWord)
        if theUser != None:
            request.session['userName'] = theUser['name']
            request.session['idUser'] = theUser['idUser']
            return LoadPage_index(request)
        error = "Wrong email or password, please try again!"
    Data = {'error': error}
    return render(request,'pages/dangnhap.html',Data)
def LoadPage_taikhoan(request):
    return render(request,'pages/taikhoan.html')


def LoadPage_logout(request):
    request.session.flush()
    request.session.modified = True
    return LoadPage_index(request)

