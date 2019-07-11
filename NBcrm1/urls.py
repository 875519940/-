"""NBcrm1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from nbapp1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index,name='index'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^get_valid_img/',views.get_valid_img,name='get_valid_img'),
    url(r'^logout',views.logout,name='logout'),
    url(r'^customers/list',views.CustomerView.as_view(),name='customers'),

    # url(r'^customers/list',views.customers,name='customers'),

    url(r'^customers/add/', views.AddCustomer.as_view(), name='addcustomer'),
    # 修改公共客户信息
    url(r'^customers/edit/(\d+)/', views.EditCustomer.as_view(), name='editcustomer'),
    # 删除公共客户信息
    url(r'^customers/delete/(\d+)/', views.DeleteCustomer.as_view(), name='deletecustomer'),
    # 私有客户信息展示
    # url(r'^mycustomers/',views.mycustomers,name='mycustomers'),
    url(r'mycustomers',views.CustomerView.as_view(),name='mycustomers'),
    # 测试分页
    url(r'^text/',views.text,name='text'),
    # 展示跟进记录页面
    # url(r'^genjin/',views.genjin,name='genjin'),
    # 跟进记录中的，添加记录按钮跳转
    # url(r'genjintiaozhuan/',views.genjintiaozhuan,name='genjintiaozhuan'),
    # 跟进记录
    url(r'^consultrecord/$',views.ConsultRecordView.as_view(),name='consultrecord'),
    # 跟进详情
    url(r'^consultrecord/(\d+)/',views.ConsultRecordView.as_view(),name='xiangqing'),
    # 获取添加页面，一个函数里筛选编辑或者添加页面
    url(r'^consultrecord/add/',views.AddRecord.as_view(),name='addrecord'),
    # 获取编辑页面
    url(r'^consultrecord/edit/(\d+)/',views.AddRecord.as_view(),name='edit'),

    # 获取班级信息结构表
    url(r'class/',views.ClassRecord.as_view(),name='class'),

    # 点击学详那个字段看到学生学习记录的表格的url
    url(r'^study_decord/(\d+)/', views.StudyRecordDeialView.as_view(), name='study_decord'),

    # 班级表里的添加记录url
    url(r'^banjitianjia/', views.YeTian.as_view(), name='yemiantianjia'),

    # 班级表里的删除
    url(r'^banjishanchu/(\d+)', views.BanShan.as_view(), name='banjishanchu'),

    # 班级表里的编辑
    url(r'^banjibianji/(\d+)', views.BianJi.as_view(), name='banjibianji'),











]
