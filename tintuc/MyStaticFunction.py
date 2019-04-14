from tintuc.models import *


numberOfRowToGet = 5
def loadMenuSide():
    return theloai.objects.all()
def loadTopSlide():
    arrSide=slide.objects.all()
    folder='images/slide/'
    for sl in arrSide:
        sl.Hinh=folder+sl.Hinh
    return arrSide
def loadTopNews(page=None):
    theFolder = 'images/tintuc/'
    fromPage = 0
    if page == None:
        page = 1
    else:
        fromPage = numberOfRowToGet * (page-1)
    toPage = fromPage + numberOfRowToGet
    topNews = Tin.objects.all().values('idTin','TieuDe','TieuDeKhongDau','TomTat','Hinh','SoLuotXem','Update_at','idLoaiTin')[fromPage:toPage]
    arrLT = []
    for eachNew in topNews:
        eachNew['Hinh'] = theFolder + eachNew['Hinh']
        temp = eachNew['idLoaiTin']
        arrLT.append(loaitin.objects.get(idLoaiTin=temp))
    return zip(topNews,arrLT)
def loadNewOfTLWithPage(idTL,page = None):  
    theFolder = 'images/tintuc/'
    if page == None:
        page = 1
    else:
        fromPage = numberOfRowToGet  * (page-1)
    toPage = fromPage + numberOfRowToGet
    arrNew = Tin.objects.filter(idLoaiTin=idTL).values('idTin','TieuDe','TieuDeKhongDau','TomTat','Hinh','SoLuotXem','Update_at')[fromPage:toPage]
    for eachNew in arrNew:
        eachNew['Hinh'] = theFolder + eachNew['Hinh']
    return arrNew 
def loadInfoOfChiTiet(idTinTuc):
    theFolder = 'images/tintuc/'
    tin = Tin.getTinWithFolderById(idTin=idTinTuc,folderString=theFolder)
    relatedNews = Tin.changeImageSource(tin.getRelatedNews(),theFolder)
    hotNews = Tin.changeImageSource(tin.getHotNews(), theFolder)
    cms = tin.comment_set.all() #comment.objects.filter(idTinTuc=idTinTuc).values('idUser','NoiDung','Created_at')
    if len(cms)==0:
        return {'TinTrang': tin,'relatedNews': relatedNews,'hotNews': hotNews}
    arrUser = []
    for cm in cms:
        arrUser.append(cm.getUserOfComment())
    return {'TinTrang': tin, 'AllComments': zip(cms,arrUser),'relatedNews': relatedNews,'hotNews': hotNews}

def login(userName, passWord):
    user = users.login(userName,passWord)
    if user is None:
        return None
    name = user.name
    id = user.idUser
    theUser = {'name': name, 'idUser': id}
    return theUser
def getMaxpageOfLoaiTin(idLoaiTin):
    return loaitin.objects.all().count() / numberOfRowToGet + 1

