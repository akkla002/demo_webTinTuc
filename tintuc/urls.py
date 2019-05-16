from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.LoadPage_index, name='home'),
    path('GioiThieu/',views.LoadPage_GioiThieu, name='GioiThieu'),
    path('loaitin/<int:id>/',views.LoadPage_loaitin, name='loaitin'),
    path('loaitin/<int:id>/<int:page>/',views.LoadPage_loaitin, name='loaitin'),
    path('chitiet/<int:idTinTuc>/',views.LoadPage_chitiet, name='chitiet'),
    path('dangky/',views.LoadPage_dangky, name='dangky'),
    path('dangnhap/',views.LoadPage_dangnhap, name='dangnhap'),
    path('taikhoan/',views.LoadPage_taikhoan, name='taikhoan'),
    path('logout/', views.LoadPage_logout, name='dangxuat'),
    path('admin/cmdt', views.LoadCommentManagement, name='cmdt')
]