from django.shortcuts import render, HttpResponse, redirect
from nbapp1 import form
from nbapp1 import models
from NBcrm1 import settings
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views import View
import os
from nbapp1 import page
from django.db.models import Q, F, Min, Max, Count


# Create your views here.

def index(request):
    return render(request, 'index.html')


# 注册

def register(request):
    if request.method == 'GET':
        l1 =form.UserForm()

        return render(request, 'register.html', {'l1': l1})
    else:
        form_obj = form.UserForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            data.pop('r_password')
            models.UserInfo.objects.create_user(**data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'form_obj': form_obj})


# 登陆
def login(request):
    response_msg = {'code': None, 'msg': None}
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_bode = request.POST.get('valid_code')
        # 1 首先验证验证码是否正确
        if valid_bode.upper() == request.session.get('valid_str').upper():
            # 2 验证用户名和密码是不是存在
            user_obj = auth.authenticate(username=username, password=password)
            # 用户名密码正确
            if user_obj:
                # 3 保存session
                auth.login(request, user_obj)
                response_msg['code'] = 1000
                response_msg['msg'] = '登录成功!'
            else:
                response_msg['code'] = 1002
                response_msg['msg'] = '用户名或者密码输入有误!'

        # 验证码失败报错
        else:
            response_msg['code'] = 1001
            response_msg['msg'] = '验证码输入有误!'

        return JsonResponse(response_msg)


def get_valid_img(request):
    import random
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    from PIL import Image, ImageDraw, ImageFont
    img_obj = Image.new('RGB', (200, 34), get_random_color())
    draw_obj = ImageDraw.Draw(img_obj)
    font_path = os.path.join(settings.BASE_DIR, 'statics/font/NAUERT__.TTF')
    font_obj = ImageFont.truetype(font_path, 16)
    sum_str = ''
    for i in range(6):
        a = random.choice(
            [str(random.randint(0, 9)), chr(random.randint(97, 122)), chr(random.randint(65, 90))])  # 4  a  5  D  6  S
        sum_str += a
    print(sum_str)
    draw_obj.text((64, 10), sum_str, fill=get_random_color(), font=font_obj)

    width = 200
    height = 34
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # # 添加噪点
    for i in range(10):
        # 这是添加点，50个点
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        # 下面是添加很小的弧线，看上去类似于一个点，50个小弧线
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    from io import BytesIO
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()

    # 验证码对应的数据保存到session里面
    request.session['valid_str'] = sum_str

    return HttpResponse(data)


# 注销

def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def index(request):
    # return render(request,'starter.html')
    return render(request, 'index.html')


# 查看客户所有信息
# def customers(request):
#     # all_customers = models.Customer.objects.all()
#     wd=request.GET.get('wd','')
#     condition=request.GET.get('condition','')
#     # current_page_num = request.GET.get('page', 1)
#     all_customers = models.Customer.objects.filter(consultant__isnull=True)
#     # 把销售这个字段里面为空的数据拿出来
#     if wd:
#         q=Q()
#         q.children.append((condition,wd))
#         all_customers=all_customers.filter(q)
#     current_page_num = request.GET.get('page', 1)
#
#     per_page_counts = 5
#     page_number = 11
#     total_count = all_customers.count()
#
#     page_obj = page.PageNation(request.path, current_page_num, total_count,request, per_page_counts, page_number)
#
#     all_customers = all_customers.order_by('pk')[page_obj.start_num:page_obj.end_num]
#
#     ret_html = page_obj.page_html()
#
#     return render(request, 'customers.html', {'all_customers': all_customers,'ret_html':ret_html})
# #
#     # return render(request,'customers.html',{'all_customers':all_customers})


class CustomerView(View):
    def get(self, request):
        wd = request.GET.get('wd', '')
        condition = request.GET.get('condition', '')
        # 这是过滤公户的,也就是没有销售的
        if request.path==reverse('customers'):
            flag=0
            all_customers = models.Customer.objects.filter(consultant__isnull=True)
        else:
            flag=1
            all_customers=models.Customer.objects.filter(consultant=request.user)
            print(all_customers)
        if wd:
            q = Q()
            # q.connector = 'or'
            # q.children.append((condition,wd))
            q.children.append((condition, wd))
            # 根据用户查询条件再次进行筛选
            all_customers = all_customers.filter(q)
        current_page_num = request.GET.get('page', 1)

        per_page_counts = 5
        page_number = 11
        total_count = all_customers.count()

        page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts, page_number)
        try:

            all_customers = all_customers.order_by('-pk')[page_obj.start_num:page_obj.end_num]

            ret_html = page_obj.page_html()

            return render(request, 'customers.html', {'all_customers': all_customers, 'ret_html': ret_html,'flag':flag})
        except Exception:
            return HttpResponse('搜索条件查询不到数据')

    def post(self, request):
        print(request.POST)
        self.data = request.POST.getlist('selected_id')
        print(self.data)
        action = request.POST.get('action')  # 'batch_delete'
        if hasattr(self, action):
            func = getattr(self, action)
            if callable(func):
                func(request)
                return redirect(request.path)
            else:
                return HttpResponse('不要搞事!!')
        else:
            return HttpResponse('不要搞事!!')

        # 批量删除

    def batch_delete(self, request):
        models.Customer.objects.filter(pk__in=self.data).delete()

    # 批量更新
    def batch_update(self, request):
        models.Customer.objects.filter(pk__in=self.data).update(name='科比')

    # 批量公户转私户
    def batch_reverse_gs(self, request):
        models.Customer.objects.filter(pk__in=self.data).update(consultant=request.user)

    # 批量私户转公户
    def batch_reverse_sg(self, request):
        models.Customer.objects.filter(pk__in=self.data).update(consultant=None)


# 跳转获取添加页面
class AddCustomer(View):
    def get(self, request):
        form_obj = form.CustomerModelForm()
        return render(request, 'addcustomer.html', {'form_obj': form_obj})

    # 接受提交的客户信息，并验证
    def post(self, request):
        form_obj = form.CustomerModelForm(request.POST)
        # {'qq':'11111','name':'xiaohei'}
        if form_obj.is_valid():
            form_obj.save()
            return redirect('customers')

        else:
            return render(request, 'addcustomer.html', {'form_obj': form_obj})


# 跳转获取编辑页面

class EditCustomer(View):
    def get(self, request, pk):
        custome_obj = models.Customer.objects.filter(pk=pk).first()
        form_obj = form.CustomerModelForm(instance=custome_obj)

        return render(request, 'editcustomer.html', {'form_obj': form_obj})

    def post(self, request, pk):
        custome_obj = models.Customer.objects.filter(pk=pk).first()
        form_obj = form.CustomerModelForm(request.POST, instance=custome_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('customers')

        else:
            return render(request, 'editcustomer.html', {'form_obj': form_obj})


# 删除单条公共客户信息
class DeleteCustomer(View):
    def get(self, request, pk):
        models.Customer.objects.filter(pk=pk).delete()
        return redirect('customers')


# 点击展示私有客户信息
# def mycustomers(request):
#     my_customers = models.Customer.objects.filter(consultant=request.user)
#
#     return render(request, 'mycustomer.html', {'my_customers': my_customers})


# 分页测试
def text(request):
    current_page_num = request.GET.get('page', 1)
    per_page_counts = 10
    page_number = 5

    all_data = models.Customer.objects.all()
    total_count = all_data.count()
    ret_html, start_num, end_num = page.pagenation(request.path,
                                                   current_page_num, total_count, per_page_counts, page_number)
    all_data = models.Customer.objects.all()[start_num:end_num]

    return render(request, 'test.html', {'all_data': all_data, 'ret_html': ret_html})



# def genjin(request):
#     # form_obj = form.GenJin()
#     print(111)
#     l1=models.ConsultRecord.objects.all()
#     return render(request,'genjin.html')
#
# def genjintiaozhuan(request):
#     form_obj = form.GenJin()
#     if request.method=='GET':
#         return render(request,'genjintiaozhuan.html',{'form_obj':form_obj})
#
# 跟进记录
class ConsultRecordView(View):
    def get(self,request,pk=None):
        wd = request.GET.get('wd', '')
        condition = request.GET.get('condition', '')
        print(request.user)
        # print(wd,condition)
        # 这是过滤公户的,也就是没有销售的
        if pk:
            # all_records = models.ConsultRecord.objects.filter(consultant=request.user)
            all_records = models.ConsultRecord.objects.filter(customer_id=pk)
            # print(all_records)
        else:
            # all_records=models.ConsultRecord.objects.filter(consultant_id=pk)
            all_records = models.ConsultRecord.objects.filter(consultant=request.user)


        if wd:
            q = Q()
            q.children.append((condition, wd))
            print(q)

            all_records = all_records.filter(q)
            print(all_records)
        current_page_num = request.GET.get('page', 1)

        per_page_counts = 5
        page_number = 11
        total_count = all_records.count()

        page_obj = page.PageNation(request.path, current_page_num, total_count, request, per_page_counts, page_number)

        all_records = all_records.order_by('-pk')[page_obj.start_num:page_obj.end_num]

        ret_html = page_obj.page_html()

        return render(request, 'genjin.html',
                      {'all_records': all_records, 'ret_html': ret_html, })

    def post(self, request):
        print(request.POST)
        self.data = request.POST.getlist('selected_id')
        action = request.POST.get('action') # 'batch_delete'
        print(action)
        if hasattr(self, action):
            func = getattr(self, action)
            if callable(func):
                ret = func(request)
                if ret:
                    return ret

                return redirect(request.path)
            else:
                return HttpResponse('不要搞事!!')
        else:
            return HttpResponse('不要搞事!!')

        # 批量删除

    def batch_delete(self, request):
        print(self.data)
        models.Customer.objects.filter(pk__in=self.data).delete()
        return HttpResponse('ok')


        # 批量更新

    def batch_update(self, request):
        models.Customer.objects.filter(pk__in=self.data).update(name='雄哥')



class AddRecord(View):

    def get(self,request,pk=None):
        print(pk)
        consultrecordobj = models.ConsultRecord.objects.filter(pk=pk).first()
        form_obj = form.ConsultRecordModelForm(request,instance=consultrecordobj)
        return render(request,'genjintiaozhuan.html',{'form_obj':form_obj})
    def post(self,request,pk=None):
        consultrecordobj = models.ConsultRecord.objects.filter(pk=pk).first()
        form_obj = form.ConsultRecordModelForm(request,request.POST,instance=consultrecordobj) #QueryDict
        if form_obj.is_valid():
            form_obj.save()
            return redirect('consultrecord')

        else:
            return render(request,'genjintiaozhuan.html',{'form_obj':form_obj})


# 自定义批量创建学习记录

class ClassRecord(View):
    def get(self,request):
        all_obj=models.ClassStudyRecord.objects.all()

        return render(request,'banji.html',{'all_obj':all_obj})
    def post(self,request):
        action = request.POST.get('action')
        print(action)
        selected_id = request.POST.getlist('selected_id')
        print(selected_id)
        if hasattr(self, action):
            ret = getattr(self, action)(selected_id)
        return self.get(request)

    def ba_create(self, selected_id):

        for course_record_id in selected_id:
            all_students = models.ClassStudyRecord.objects.get(pk=course_record_id).class_obj.students.all()
            l1 = []
            for student in all_students:
                obj = models.StudentStudyRecord(
                    student=student,
                    classstudyrecord_id=course_record_id,
                )

                l1.append(obj)
            models.StudentStudyRecord.objects.bulk_create(l1)


# 点击学详走的视图函数
class StudyRecordDeialView(View):
    def get(self,request,class_record_id):
        #找到课程记录
        class_record_obj = models.ClassStudyRecord.objects.get(pk=class_record_id)
        #找到这个课程记录所生成的所有学生学习记录
        all_study_recored = models.StudentStudyRecord.objects.filter(
            classstudyrecord=class_record_obj,

        )
        score_choices = models.StudentStudyRecord.score_choices

        return render(request,'study_record_detail.html',{'class_record_obj':class_record_obj,'all_study_recored':all_study_recored,'score_choices':score_choices})


    def post(self,request,class_record_id):
        data = request.POST
        # data.pop('csrfmiddlewaretoken  ')
        '''
            {
                1:{'score':85,'homework_note':'333'},
                2:{'score':85,'homework_note':'333'}
            }

        '''
        data_dict = {}
        for key, val in data.items():  # {'score_1':90}
            print(key, val)
            if key == 'csrfmiddlewaretoken':
                continue

            field, pk = key.rsplit('_', 1)
            if pk in data_dict:
                data_dict[pk][field] = val
            else:
                data_dict[pk] = {
                    field: val,
                }

            print('>>>>', data_dict)

        for spk, sdata in data_dict.items():
            # print(field,pk)
            models.StudentStudyRecord.objects.filter(**{'pk': spk}).update(**sdata)

        # return self.get(request,class_record_id)
        return redirect(reverse('study_decord', args=(class_record_id,)))

# 班级表里的跳转添加页面
class YeTian(View):
    def get(self, request):
        form_obj = form.ClassStudyRecordModelForm()
        return render(request, 'banjitianjia.html', {'form_obj': form_obj})

            # 接受提交的客户信息，并验证

    def post(self, request):
        form_obj = form.ClassStudyRecordModelForm(request.POST)
        # {'qq':'11111','name':'xiaohei'}
        if form_obj.is_valid():
            form_obj.save()
            return redirect('class')

        else:
            return render(request, 'banjitianjia.html', {'form_obj': form_obj})


# 班级表里的删除视图函数
class BanShan(View):
    def get(self,request,pk):
        models.ClassStudyRecord.objects.filter(pk=pk).delete()
        return redirect('class')

# 班级表里的编辑

class BianJi(View):
    def get(self,request,pk):
        content=models.ClassStudyRecord.objects.filter(pk=pk).first()
        form_obj=form.ClassStudyRecordModelForm(instance=content)
        return render(request,'banjitianjia.html',{'form_obj':form_obj})








