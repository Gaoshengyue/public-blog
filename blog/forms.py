

from django import forms
from django.forms import widgets
from .models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
class RegForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request

    user=forms.CharField(min_length=5,max_length=12,
                         error_messages={"required": "用户名不能为空",
                             "min_length":"最小长度为5",
                                         "max_length": "最大长度为12" },
                         widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"5~12位不能为纯英文或纯数字"})
                         )
    pwd =forms.CharField(min_length=5,max_length=12,
                         error_messages={"required": "密码不能为空",
                             "min_length":"最小长度为5",
                                         "max_length": "最大长度为12" },
          widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"5~12位不能为纯英文或纯数字"})
    )

    repeat_pwd = forms.CharField(
        error_messages={"required": "密码验证不能为空"},
        widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "再次输入密码"})

    )

    email=forms.EmailField(error_messages={"invalid":"非邮箱格式！",
                                           "required": "邮箱不能为空"},
                           widget=widgets.EmailInput(attrs={"class": "form-control", "placeholder": "Email地址"})
                           )

    valid_code=forms.CharField(
        error_messages={"required": "验证码不能为空"},
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "valid_code"})
    )



    def clean_user(self):
        username = self.cleaned_data.get("user")
        if not username.isdigit() or not username.isalpha():
            user = UserInfo.objects.filter(username=self.cleaned_data.get("user"))
            if not user:
                return self.cleaned_data.get("user")

            else:
                raise ValidationError("用户名已经存在！")
        else:
            raise ValidationError("用户名不能是纯数字或者纯字母")

    def clean_pwd(self):
        pwd=self.cleaned_data.get("pwd")

        if pwd.isdigit() or pwd.isalpha():
            raise ValidationError("密码不能是纯数字或者纯字母")
        else:
            return pwd

    def clean_valid_code(self):

        val=self.cleaned_data.get("valid_code") # 用户输入的验证码

        if val.upper() == self.request.session.get("valid_code_str").upper():
            return self.cleaned_data.get("valid_code")

        else:
            raise ValidationError("valid code error！")


    def clean(self):
       if self.cleaned_data.get("pwd"):
           if self.cleaned_data.get("pwd") == self.cleaned_data.get("repeat_pwd"):
               return self.cleaned_data
           else:
               raise ValidationError("两次密码不一致！")

