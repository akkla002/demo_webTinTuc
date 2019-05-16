from django.shortcuts import render
from django.http import HttpResponseRedirect
from .MyStaticFunction import *
#<<<<<<< HEAD
from .paginationOfLT import *
#=======
#>>>>>>> cfb7e0cad8314dd62f76cc0e1e3fd60327f97eca

# Create your views here.
thePagination = paginationOfLT(0)

# Hàm load page index
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
            if request.GET['commentContent'] != "":
                addNewComment(request.session['idUser'],idTinTuc, request.GET['commentContent'])
    Data = loadInfoOfChiTiet(idTinTuc)
    return render(request,'pages/chitiet.html',Data)



def LoadPage_dangky(request):
    error = 'None'
    finish = 0
    if request.method=='POST':
        if 'email' not in request.POST or 'name' not in request.POST or 'password' not in request.POST:
            error = 'Faile'
        else:
            email=request.POST['email']
            if users.checkAvailableEmail(email) != None:
                error = "Tồn tại email này!"
            else:
                name=request.POST['name']
                password=request.POST['password']
                createAccount(email,name,password)
                finish = 1
    data = {'error': error,'success': finish}
    return render(request,'pages/dangky.html', data)

# Hàm load page và xử lý đăng nhập
def LoadPage_dangnhap(request):
    error = 'None'
    # Kiểm tra thông tin đăng nhập có hay ko
    if request.method == "POST":
        if 'email' in request.POST:
            email = request.POST['email']
        if 'passWord' in request.POST:
            passWord = request.POST['passWord']     
            
        theUser = checkLogin(email,passWord)
        if theUser == None:
            error = "Wrong email or password, please try again!"
        else:
            request.session['userName'] = theUser['name']
            request.session['idUser'] = theUser['idUser']
            return LoadPage_index(request)
    Data = {'error': error}
    return render(request,'pages/dangnhap.html',Data)
def LoadPage_taikhoan(request):
    return render(request,'pages/taikhoan.html')

# Hàm đăng xuất
def LoadPage_logout(request):
    request.session.flush()
    request.session.modified = True
    return LoadPage_index(request)

def LoadCommentManagement(request):
    if request.session['userName'] != 'admin':
        return LoadPage_index(request)
    if request.method == 'GET':
        if 'listAns' in request.GET:
            print("ok")
            listAns = request.GET.getlist('listAns')
            print(listAns)
            processComment(input = listAns)
        else:
            print("KO vao duoc")
        #print('vao day')
    tempCMs = getListCommentForBrowse()
    data = {'listCMs': tempCMs}
    return render(request,'pages/commentManagement.html',data)