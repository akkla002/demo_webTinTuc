# Cần kết nối với class Tin bên module models để có thể lấy dữ liệu từ database

from .models import Tin


class paginationOfLT:
    theIdOfLT = 0
    numItemsEachPage = 5
    totalItems = None
    maxPage = 0
    nowPage = 1
    theFolder = 'images/tintuc/'  # để trỏ tới file lưu hình ảnh

    

    # Đây là hàm khởi tạo của Class này
    def __init__(self, theId = 0):
        self.setId(theId)



    #  Mỗi khi thay đổi idLoaiTin của object này thì sẽ chỉnh sửa thông tin trong đó

    def setId(self, theID = 0):
        # Nếu id mới nhập vào trùng với idLT hoặc là 0 thì sẽ tự động bỏ qua
        if self.theIdOfLT == theID or theID == 0:
            return
        self.theIdOfLT = theID
        self.totalItems = Tin.objects.filter(idLoaiTin=self.theIdOfLT).count()
        self.setMaxpage()

    # Dựa vào số lượng Tin của LoaiTin đó thì sẽ tính có bao nhiêu page
    def setMaxpage(self):
        self.maxPage = self.totalItems / self.numItemsEachPage
        if self.totalItems % self.numItemsEachPage != 0:
            self.maxPage += 1
        self.maxPage = int(self.maxPage)
    

    # Tạo danh sách trang
    def getRangePage(self):
        if self.maxPage == 1:
            return 1
        if self.maxPage < 5:
            return range(1,self.maxPage+1)
        a = []
        for x in range(-2,3):
            temp = self.nowPage + x
            if temp >= 1 and temp <= self.maxPage:
                a.append(temp)
        return a
    

    # Mỗi trang đều có những tin khác nhau nên sẽ lấy tin của trang hiện tại
    def getNewsInNowPage(self):
        toNews  = self.nowPage * self.numItemsEachPage
        fromNews = toNews - self.numItemsEachPage
        arrNew = Tin.objects.filter(idLoaiTin=self.theIdOfLT).values('idTin','TieuDe','TieuDeKhongDau','TomTat','Hinh','SoLuotXem','Update_at')[fromNews:toNews]
        for eachNew in arrNew:
            eachNew['Hinh'] = self.theFolder + eachNew['Hinh']
        return arrNew 
    