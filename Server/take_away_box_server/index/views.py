# encoding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
# Create your views here.


def toLogin_view(request):
    return render(request, 'login.html')


def Login_view(request):
    u = request.POST.get("user", '')
    p = request.POST.get("pwd", '')
    if u and p:
        cnt = IndexStaffInfo.objects.filter(stuff_name=u, staff_pwd=p).count()
        if cnt > 0:
            return render(request, 'write_dest.html')
        else:
            return HttpResponse("请输入正确的账号和密码")
    else:
        return HttpResponse("您还妹填完整呐！")


def type_in_dest_view(request):
    input_str_dest = request.POST.get("input_str_dest", '')
    input_str_phone_num = request.POST.get("input_str_phone_num", "")
    if input_str_dest and input_str_phone_num:
        dest = Dest(str_dest=input_str_dest, time_left=-
                    1, phone_num=input_str_phone_num, status=0)
        dest.save()
        return HttpResponse("目的地已设置，请您专心驾驶，我们会帮您联系顾客取餐。")
    else:
        return HttpResponse("咱也不知道您要去哪啊！")
