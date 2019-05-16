
# Để có thể truy cập vào module models

from tintuc.models import *

# Đây là module chứa những static function


theFolder='images/tintuc/'

# Lấy dữ liệu để tạo menu Side bên Giao diện

def loadMenuSide():
    return theloai.objects.all()


# Lấy dữ liệu phần Slide đẩy lên Giao diện

def loadTopSlide():
    arrSide=slide.objects.all()
    for sl in arrSide:
        sl.Hinh='images/slide/'+sl.Hinh
    return arrSide


# Lấy những tin mới nhất theo thời gian

def loadTopNews(page=None):
    numberOfRowToGet = 5
    theFolder = 'images/tintuc/'
    fromPage = 0
    if page == None:
        page = 1
    else:
        fromPage = numberOfRowToGet * (page-1)
    toPage = fromPage + numberOfRowToGet
    topNews = Tin.objects.all().order_by('-Created_at').values('idTin','TieuDe','TieuDeKhongDau','TomTat','Hinh','SoLuotXem','Created_at','idLoaiTin')[fromPage:toPage]
    arrLT = []
    for eachNew in topNews:
        eachNew['Hinh'] = theFolder + eachNew['Hinh']
        temp = eachNew['idLoaiTin']
        arrLT.append(loaitin.objects.get(idLoaiTin=temp))
    return zip(topNews,arrLT)



# Lấy những dữ liệu cần thiết cho trang chi tiết (Lấy tin, comment, tin liên quan với tin tức đó)

def loadInfoOfChiTiet(idTinTuc):
    tin = Tin.getTinWithFolderById(idTin=idTinTuc,folderString=theFolder)
    relatedNews = Tin.changeImageSource(tin.getRelatedNews(),theFolder)
    hotNews = Tin.changeImageSource(tin.getHotNews(), theFolder)
    cms = comment.objects.raw('Select * from tintuc_comment where idTintuc_id = ' + str(idTinTuc) + ' and allowed = 1 and show = 1')
    #cms = tin.comment_set.all().order_by('-Created_at') #comment.objects.filter(idTinTuc=idTinTuc).values('idUser','NoiDung','Created_at')
    if len(cms) == 0:
        return {'TinTrang': tin,'relatedNews': relatedNews,'hotNews': hotNews}
    arrUser = []
    for cm in cms:
        arrUser.append(cm.getUserOfComment())
    return {'TinTrang': tin, 'AllComments': zip(cms,arrUser),'relatedNews': relatedNews,'hotNews': hotNews}


# Kiểm tra thông tin khi đăng nhập

def checkLogin(userName, passWord):
    user = users.login(userName,passWord)
    if user is None:
        return None
    name = user.name
    id = user.idUser
    theUser = {'name': name, 'idUser': id}
    return theUser

# thêm comment vào tin tức

def addNewComment(idUser, idTin, commentContent):
    cm = comment()
    cm.idUser = users.objects.get(idUser=idUser)
    cm.idTinTuc = Tin.objects.get(idTin=idTin)
    cm.NoiDung = commentContent
    cm.show = False
    cm.allowed = True
    cm.Created_at = datetime.datetime.now()
    cm.save()
    #cm.changeStatus(True)
    
def createAccount(email,name,passWord):
    if users.checkAvailableEmail(email) != None:
        return False
    newUser = users()
    newUser.email = email
    newUser.name = name
    newUser.password = passWord
    newUser.Created_at = datetime.datetime.now()
    newUser.save()
    return True


def processComment(input):
    for value in input:
        nowStr = value.split('_')
        id = int(nowStr[0])
        theResult = int(nowStr[1])
        print("vao day")
        cm = comment.objects.get(id=id)
        cm.changeStatus(theResult)
    return

def getListCommentForBrowse():
    cms = comment.objects.raw("Select * from tintuc_comment where allowed = 1 and show = 0")[0:10]
    return cms
