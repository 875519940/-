

import re
from nbapp1 import models
from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets

class UserForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=6, label='用户名',
                               error_messages={'required': '这个字段必须填写!', 'max_length': '最大不能超过32位','min_length': '最小不能低于6位'}, )
    password = forms.CharField(max_length=32, min_length=6, label='密码',
                               error_messages={'required': '这个字段必须填写!', 'max_length': '最大不能超过32位','min_length': '最小不能低于6位'},
                               widget=widgets.PasswordInput
                               )

    r_password = forms.CharField(max_length=32, min_length=6, label='重复密码',
                                 error_messages={'required': '这个字段必须填写!', 'max_length': '最大不能超过32位','min_length': '最小不能低于6位'},
                                 widget=widgets.PasswordInput)
    email = forms.EmailField(max_length=32, label='邮箱',error_messages={'required': '这个字段必须填写!', 'max_length': '最大不能超过32位', 'invalid': '邮箱格式不对'}, )

    def clean_username(self):
        val = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=val).first()
        if user_obj:
            raise ValidationError('该用户名已经存在,请换个名字!')
        else:
            return val

    def clean_password(self):
        val = self.cleaned_data.get('password')
        if val.isdecimal():
            raise ValidationError('密码不能为纯数字')
        else:
            return val

    def clean_email(self):
        val = self.cleaned_data.get('email')
        if re.search('\w+@163.com$', val):
            return val
        else:
            raise ValidationError('必须是163网易邮箱!')

    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')

        if password != r_password:
            self.add_error('r_password', '两次密码不一致')  # 这是给r_password的错误添加这个错误信息
            # raise ValidationError('两次密码不一致!') #被总的错误拿到了

        else:
            return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        from multiselectfield.forms.fields import MultiSelectFormField
        for field in self.fields.values():
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({
                    'class':'form-control'
                })

# class GenJin(forms.ModelForm):
#     class Meta:
#         model=models.ConsultRecord
#         fields='__all__'
#         exclude=['delete_status']
#
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         from multiselectfield.forms.fields import MultiSelectFormField
#         for field in self.fields.values():
#             if not isinstance(field,MultiSelectFormField):
#                 field.widget.attrs.update({
#                     'class':'form-control'
#                 })

class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status',]


    def __init__(self,request,*args,**kwargs):
        # print('>>>>>',request)
        super().__init__(*args,**kwargs)

        self.fields['consultant'].queryset = models.UserInfo.objects.filter(pk=request.user.pk)
        self.fields['customer'].queryset = models.Customer.objects.filter(consultant=request.user)

        for key,field in self.fields.items():
            field.widget.attrs.update({
                'class':'form-control',
            })



class ClassStudyRecordModelForm(forms.ModelForm):
    class Meta:
        model=models.ClassStudyRecord
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        from multiselectfield.forms.fields import MultiSelectFormField
        for field in self.fields.values():
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({
                    'class':'form-control'
                })















