import io
import os
from datetime import datetime
from django.conf import settings #读取上传的文件需导入settings
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from PIL import Image,ImageDraw,ImageFont
import random
# Create your views here.
from django.urls import reverse
from user.models import User
from user.reuse import login_check
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def login(request):
    if request.method=='POST':
        #获取用户输入的用户名和密码
        username=request.POST.get('username')
        password=request.POST.get('pwd')
        vcode=request.POST.get('vcode')  #从用户提交的form表单获取
        verifycode=request.session.get('verifycode')   #从服务器的session中获取，get请求打开login页面就自动生成验证码session
        #通过查询数据库中的用户名来判断用户名是否存在
        try:
            user=User.objects.get(username=username)
        except Exception:
            return redirect(reverse('user:login'))
        #判断密码和验证码是否正确
        if user.pwd == password and vcode == verifycode:
            request.session['username'] = username
            return redirect(reverse('user:userDetail'))
        else:
            return redirect(reverse('user:login'))
    else:
        return render(request,'login.html')


def regist(request):
    if request.method == 'POST':
        #step1:获取用户的注册信息
        username=request.POST.get('username')
        name=request.POST.get('name')     #真实姓名
        pwd=request.POST.get('pwd')
        age=request.POST.get('age')
        sex=request.POST.get('sex')
        phone=request.POST.get('phone')

        #判断用户名和密码非空
        if not username or not name or not pwd:
            return render(request,'regist.html')

        if (8 >= len(username) >= 6) and username.isalpha():
            # 将用户注册信息写入数据库,用户名字段是unique，若重名会报错
            try:
                user = User(username=username, name=name, pwd=pwd, age=age, sex=sex, phone=phone)
                user.save()
                return redirect(reverse('user:login'))
            except:
                    err = {'err': '用户名已存在！'}
                    return render(request, 'regist.html', context=err)
        else:
                err = {'err': '请输入正确的用户名!'}
                return render(request, 'regist.html', context=err)
    else:
            return render(request, 'regist.html')

@login_check
def userDetail(request):
    #头像操作
    #第一步：从form表单中取得头像文件
   # base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
   # filepath = f'{base_dir}/static/upload/img'
   # if request.method=='POST':
     #   img=request.FILES.get('file1')
    #    with open(filepath,'wb') as f:
     #       for fimg in img.chunks():
      #          f.write(fimg)
     #       f.close()
        # 显示头像
     #   return redirect(reverse('user:userDetail'))
 #   else:

    username = request.session.get('username')
        # 在数据库中匹配username的这条数据，查询数据库
    user = User.objects.get(username=username)
    now = datetime.now()
    context={
        'user':user,
        'now':now
        }
    return render(request,'userDetail.html',context=context)

@login_check
def userList(request):
        user_data = User.objects.all()  # 获取所有数据
        pig = Paginator(user_data, 5)  # 对谁分页，多少行数据为一页
        total_page = pig.num_pages  # 获取总页数
        current_page_num = int(request.GET.get('page', 1))  # 获取当前页数，默认为1
        current_page = Paginator.page(self=pig, number=current_page_num)  # 获取当前页的所有行数据

        if current_page_num <= 3:
            start, end = 1, min(7, total_page)
        elif current_page_num > (total_page - 3):
            start, end = max(total_page - 6, 1), total_page
        else:
            start, end = (current_page_num - 3), (current_page_num + 3)
        pages = range(start, end + 1)  # 页码索引

        now = datetime.now()
        context = {
            'user_list': user_data,
            'paginator': pig,
            'current_page': current_page,
            'current_page_num': current_page_num,
            'pages': pages,
            'now': now
        }
        return render(request, 'userList.html', context=context)

@login_check
def delete(request):
    #关键是你要删除谁？由谁来告诉你，在HTML页面中就要提交被删除的用户id
    uid=request.GET.get('uid')
    User.objects.get(pk=uid).delete()
    return redirect(reverse('user:userList'))   #这个地方必须要用重定向，如果用render重新加载就不对了

@login_check
def update(request):
    if request.method=='GET':
        uid=int(request.GET.get('uid'))
        user = User.objects.get(pk=uid)
        context = {
            'user': user
        }
        return render(request, 'update.html', context=context)
    elif request.method=='POST':
        #需要设置一个标签用来返回当前的用户id,用隐藏提交
        uid = int(request.POST.get('uid'))
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        phone = request.POST.get('phone')
        # 将用户注册信息写入数据库

        user=User.objects.get(pk=uid)
        user.name = name
        user.pwd = pwd
        user.age = age
        user.sex = sex
        user.phone = phone
        user.save()
        return redirect(reverse('user:userList'))


def quit(request):
    request.session.flush()
    return redirect(reverse('user:login'))

@login_check
def userDetail1(request):
    uid=request.GET.get('uid')
    user = User.objects.get(pk=uid)
    now = datetime.now()
    context = {
        'user': user,
        'now': now
    }
    return render(request, 'userDetail.html', context=context)


def select(request):
    #获取form表单数据
    uid = request.POST.get('ID')
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    age = request.POST.get('age')
    #若查询条件都为空，则重定向到userList，回到第一页
    # 定义十六种查询条件的组合
    if not uid and not name and not sex and not age:
        return redirect(reverse('user:userList'))
    elif uid and not name and not sex and not age:
        user_data = User.objects.filter(id=uid)
    elif not uid and name and not sex and not age:
        user_data = User.objects.filter(name=name)
    elif not uid and not name and sex and not age:
        user_data = User.objects.filter(sex=sex)
    elif not uid and not name and not sex and age:
        user_data = User.objects.filter(age=age)
    elif uid and name and not sex and not age:
        user_data=User.objects.filter(id=uid).filter(name=name)
    elif uid and not name and sex and not age:
        user_data=User.objects.filter(id=uid).filter(sex=sex)
    elif uid and not name and not sex and age:
        user_data=User.objects.filter(id=uid).filter(age=age)
    elif not uid and name and sex and not age:
        user_data=User.objects.filter(name=name).filter(sex=sex)
    elif not uid and name and not sex and age:
        user_data=User.objects.filter(name=name).filter(age=age)
    elif not uid and not name and sex and age:
        user_data=User.objects.filter(sex=sex).filter(age=age)
    elif uid and name and sex and not age:
        user_data=User.objects.filter(id=uid).filter(name=name).filter(sex=sex)
    elif uid and not name and sex and age:
        user_data = User.objects.filter(id=uid).filter(sex=sex).filter(age=age)
    elif uid and name and not sex and age:
        user_data = User.objects.filter(id=uid).filter(name=name).filter(age=age)
    elif not uid and name and sex and age:
        user_data = User.objects.filter(name=name).filter(sex=sex).filter(age=age)
    else:
        user_data = User.objects.filter(id=uid).filter(name=name).filter(sex=sex).filter(age=age)

    now = datetime.now()
    context = {
        'user_list': user_data,
        'now': now
    }

    return render(request, 'select.html', context=context)


def verify(request):
    bgcolor = (random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    width = 100
    height =45
    img = Image.new('RGB',(width,height),bgcolor)  #创建画面对象,模式，尺寸，背景色
    draw = ImageDraw.Draw(img)   #创建画笔对象
    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
    #以下定义验证码的备选值
    str = '123456789QWERTYUIOPASDFGHJKLZXCVBNM'

    rand_str = ''
    for i in range(0,4):  #左闭右开
        rand_str += str[random.randrange(0,len(str))]

    font=ImageFont.truetype("static/font/calibri.ttf",23)
    #构造字体颜色
    fontcolor1 =  (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5,2),   rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)

    del draw  #释放画笔
    #存入session，用于下一步验证，session可以保存任何字段的任何值，名字随便取
    request.session['verifycode'] = rand_str
    buf = io.BytesIO()
    img.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')


