from django.conf.urls import url
from user import views

urlpatterns=[
    url(r'^login/',views.login,name='login'),
    url(r'^regist/',views.regist,name='regist'),
    url(r'^userDetail/',views.userDetail,name='userDetail'),
    url(r'^userList/',views.userList,name='userList'),
    url(r'^delete/',views.delete,name='delete'),
    url(r'^update/',views.update,name='update'),
    url(r'^quit/',views.quit,name='quit'),
    url(r'^userDetail1/',views.userDetail1,name='userDetail1'),
    url(r'^select/',views.select,name='select'),
    url(r'^verify/',views.verify,name='verify')
]