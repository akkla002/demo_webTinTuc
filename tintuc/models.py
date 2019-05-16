from django.db import models
import datetime



# Create your models here.
class theloai(models.Model):
    objects = models.Manager()
    idTheLoai = models.IntegerField(primary_key=True)
    Ten=models.CharField(max_length=255)
    TenKhongDau=models.CharField(max_length=255)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateField(null=True, blank=True)

class loaitin(models.Model):
    objects = models.Manager()
    idLoaiTin = models.IntegerField(primary_key=True)
    idTheLoai=models.ForeignKey(theloai,on_delete=models.CASCADE)
    Ten=models.CharField(max_length=255)    
    TenKhongDau=models.CharField(max_length=255)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateTimeField(null=True, blank=True)

    def SetValue(self, id, idTL, ten, tenKhongDau):
        self.idLoaiTin = id
        self.idTheLoai = idTL
        self.Ten = ten
        self.TenKhongDau = tenKhongDau
        self.Created_at = datetime.datetime.now()
        self.Update_at = None
    @staticmethod
    def GetListOfIDTL(idTL):
        arr = []
        for lt in loaitin.objects.filter(idTheLoai=idTL):
            arr.append(lt)
        return arr


        
class Tin(models.Model):
    objects = models.Manager()
    idTin = models.IntegerField(primary_key=True)
    idLoaiTin=models.ForeignKey(loaitin,on_delete=models.CASCADE)
    TieuDe =models.CharField(max_length=255)
    TieuDeKhongDau=models.CharField(max_length=255)
    TomTat=models.TextField()
    NoiDung=models.TextField()
    Hinh=models.CharField(max_length=255)
    NoiBat=models.IntegerField(max_length=11)
    SoLuotXem=models.IntegerField(max_length=11)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateTimeField(null=True, blank=True)

    


    def getRelatedNews(self):
        theIDLT = getattr(self.idLoaiTin, 'idLoaiTin')
        top4ofNewsRelated = Tin.objects.filter(idLoaiTin = theIDLT).values('idTin','TieuDe', 'Hinh', 'TomTat')[0:4]
        return top4ofNewsRelated



    @staticmethod
    def getTinWithFolderById(idTin, folderString):
        tin = Tin.changeImageSource(inputTin = Tin.objects.get(idTin = idTin),folderString=folderString)
        return tin
    @staticmethod
    def getHotNews():
        hotNewsArr = Tin.objects.order_by('NoiBat').values('idTin','TieuDe', 'Hinh', 'TomTat')[0:4]
        return hotNewsArr

    @staticmethod
    def changeImageSource(inputTin, folderString):
        if isinstance(inputTin, Tin):
            inputTin.Hinh = folderString + inputTin.Hinh
        else:
            for eachNew in inputTin:
                eachNew['Hinh'] = folderString + eachNew['Hinh']
        return inputTin

class users(models.Model):
    objects = models.Manager()
    idUser = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateTimeField(null=True, blank=True)

    @staticmethod
    def login(email, pwd):
        ur = users.checkAvailableEmail(email)
        if ur == None:
            return None
        passWord = ur.password
        if(pwd == passWord):
            return ur
        return None
    @staticmethod
    def checkAvailableEmail(theEmail):
        ur = users.objects.filter(email = theEmail)
        if ur.count() > 0:
            return ur[0]
        return None

        
        


class comment(models.Model):
    objects = models.Manager()
    idUser=models.ForeignKey(users,on_delete=models.CASCADE)
    idTinTuc=models.ForeignKey(Tin,on_delete=models.CASCADE)
    NoiDung=models.CharField(max_length=255)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateTimeField(null=True, blank=True)
    show = models.BooleanField(False)
    allowed = models.BooleanField(False)

    def getUserOfComment(self):
        idUser = getattr(self.idUser,'idUser')
        return users.objects.get(idUser=idUser)
    def changeStatus(self,allowed):
        if allowed == 1:
            self.show = True
            self.allowed = True
        else:
            self.allowed = False
        self.save()

class slide(models.Model):
    objects = models.Manager()
    idSlide = models.IntegerField(primary_key=True)
    Ten=models.CharField(max_length=255)
    Hinh=models.CharField(max_length=255)
    link=models.CharField(max_length=255)
    Created_at=models.DateTimeField(null=True, blank=True)
    Update_at=models.DateTimeField(null=True, blank=True)