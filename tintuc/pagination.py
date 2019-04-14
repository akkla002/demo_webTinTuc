from .models import Tin


class pagination:
    theId = 0
    numItemsEachPage = 5
    totalItems = None
    maxPage = 0
    nowPage = 1

    
    def __init__(self, theId = 0):
        self.setId(theId)

    def setId(self, theID = 0):
        if self.theId == theID or theID == 0:
            return
        self.theId = theID
        self.totalItems = Tin.objects.filter(idLoaiTin=theID).count()
        self.setMaxpage()

    def setMaxpage(self):
        self.maxPage = self.totalItems / self.numItemsEachPage
        if self.totalItems % self.numItemsEachPage != 0:
            self.maxPage += 1
        self.maxPage = int(self.maxPage)
    
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
    