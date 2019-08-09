from django.shortcuts import render,HttpResponse,redirect
from cnblog.settings import *
from blog.models import *
import json
from PIL import Image,ImageDraw,ImageFont
import random
from io import BytesIO
from django.http import JsonResponse
from django.contrib import auth
# Create your views here.
from blog.geetest import GeetestLib
from .forms import  *
from blog.paging.paging import Pagation #导入自己写的分页组件
import re
from django.db.models import F
from django.db import transaction

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"

def login(request):
    if request.method == "POST":
        ret = {}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        users=UserInfo.objects.filter(username=user).first()
        if users:
            user1 = auth.authenticate(username=user,password=pwd)
            if user1:
                auth.login(request, user1)  # 设置session
                ret={"num":1,"user":user1.username}
            else:
                ret = {"num": 2, "error_pwd": "密码错误"}
        else:
            ret={"num":0,"error_user":"用户不存在"}
        rec = json.dumps(ret)
        return HttpResponse(rec)
    return render(request, "login.html")

def index(request,**kwargs):
    if not kwargs:
        user=request.GET.get("user")
        article_list = Article.objects.all()
        category=SiteCategory.objects.all()
        biao=SiteDetaiCategory.objects.all()
        # return render(request, "class.html", {"list": lip, "page_fen": page_fen, "user": user})
        if user:
            d_page = int(request.GET.get("name", 1))
            page,item=divmod(len(article_list), 5)
            if item:
                page+=1
            obj = Pagation(d_page, 5, page, len(article_list),request.path_info + '?user=' + user)  # 分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
            lip = article_list[obj.start:obj.end]  # 直接引用strat和end方法获取每一页数据的头和尾
            page_fen = obj.huobiao()  # huobiao方法获取底下该出来的跳转分页码
            users=UserInfo.objects.get(username=user)
            lujing=users.avatar
            return render(request,"index.html",{"article_list":lip,"lujing":lujing,"site":category,"xiaobiao":biao, "page_fen": page_fen,})
        page, item = divmod(len(article_list), 5)
        if item:
            page += 1
        d_page = int(request.GET.get("name", 1))
        obj = Pagation(d_page, 5, page, len(article_list),request.path_info)  # 分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
        lip = article_list[obj.start:obj.end]  # 直接引用strat和end方法获取每一页数据的头和尾
        page_fen = obj.huobiao2()  # huobiao方法获取底下该出来的跳转分页码
        return render(request, "index.html", {"article_list": lip,"site":category,"xiaobiao":biao, "page_fen": page_fen,})
    else:
        user = request.GET.get("user")
        para=int(kwargs.get("para"))
        article_list = Article.objects.filter(siteDetaiCategory_id=para)
        category = SiteCategory.objects.all()
        biao = SiteDetaiCategory.objects.all()
        # return render(request, "class.html", {"list": lip, "page_fen": page_fen, "user": user})
        if user:
            d_page = int(request.GET.get("name", 1))
            page, item = divmod(len(article_list), 5)
            if item:
                page += 1
            obj = Pagation(d_page, 5, page, len(article_list),
                           request.path_info + '?user=' + user)  # 分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
            lip = article_list[obj.start:obj.end]  # 直接引用strat和end方法获取每一页数据的头和尾
            page_fen = obj.huobiao()  # huobiao方法获取底下该出来的跳转分页码
            users = UserInfo.objects.get(username=user)
            lujing = users.avatar
            return render(request, "index.html",
                          {"article_list": lip, "lujing": lujing, "site": category, "xiaobiao": biao,
                           "page_fen": page_fen, })
        page, item = divmod(len(article_list), 5)
        if item:
            page += 1
        d_page = int(request.GET.get("name", 1))
        obj = Pagation(d_page, 5, page, len(article_list),
                       request.path_info)  # 分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
        lip = article_list[obj.start:obj.end]  # 直接引用strat和end方法获取每一页数据的头和尾
        page_fen = obj.huobiao2()  # huobiao方法获取底下该出来的跳转分页码
        return render(request, "index.html",{"article_list": lip, "site": category, "xiaobiao": biao, "page_fen": page_fen, })



def get_valid_img(request):    #验证码
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def get_random_char():
        random_num = str(random.randint(0, 9))
        random_upper_alph = chr(random.randint(65, 90))
        random_lowwer_alph = chr(random.randint(97, 122))
        random_char = random.choice([random_num, random_lowwer_alph, random_upper_alph])
        return random_char

    image = Image.new(mode="RGB", size=(150, 34), color=get_random_color())
    draw = ImageDraw.Draw(image, mode="RGB")
    font = ImageFont.truetype("blog/static/dist/fonts/kumo.ttf", 32)
    valid_code_str = ""
    for i in range(1, 6):
        char = get_random_char()
        valid_code_str += char
        draw.text([i * 20, 5], char, get_random_color(), font=font)
    width = 150
    height = 34
    for i in range(80):
        draw.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()

    # 将验证码存放在session里
    request.session["valid_code_str"] = valid_code_str
    return HttpResponse(data)


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)



#for组件版
def zhuce(request):
    # ajax请求：
    if request.is_ajax():
        regForm = RegForm(request,request.POST)

        regResponse={"user":None,"errors":None}
        if regForm.is_valid():
            # 注册
            data=regForm.cleaned_data
            user=data.get("user")
            pwd=data.get("pwd")
            email=data.get("email")
            avatar_img=request.FILES.get("file_img")
            if not avatar_img:
                avatar_img="avatar/default.jpg"
            user_obj=UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_img)
            regResponse["user"]=user

        else:
            regResponse["errors"]=regForm.errors
        return JsonResponse(regResponse)
    #  get请求：
    regForm=RegForm(request)
    return render(request,"zhuce.html",locals())


def headp(request):
    if request.method == "POST":
        username = request.POST.get("user")
        user=UserInfo.objects.filter(username=username).first()
        if not username:
            user=None
        if user:
            lujing=str(user.avatar)
            return HttpResponse("/media/" + lujing)
        else:
            return HttpResponse('/media/avatar/default.jpg')

def log_out(request):
    auth.logout(request)
    return redirect("/index/")

def home_site(request,username,**kwargs):

   # username: 访问的个人站点的用户名称，区别request.user.username
    # 查询当前站点用户对象
    user=UserInfo.objects.filter(username=username).first()
    # 查询当前站点对象
    blog=user.blog
    if blog:
        # 方式1：当前站点(用户)下的所有分类名称
        cate_list=blog.homecategory_set.all()

        # 当前站点(用户)下的每一个分类名称以及对应文章个数
        # 方式2：
        from django.db.models import Count
        # ret=HomeCategory.objects.filter(blog=blog).annotate(c=Count("article__nid")).values_list("title","c")
        # 查询当前站点的每一个标签的名称以及对应的文章数
        tags_list=Tag.objects.filter(blog=blog).annotate(c=Count("article__nid")).values_list("title","c","nid")

        # 查询每一个年月以及对应的文章数    if sqlite: strftime      mysql: date_format

        dated=Article.objects.filter(user=user).extra(select={"create_year_month":"strftime('%%Y/%%m',create_time)"})


        date_list=dated.values("create_year_month").annotate(c=Count("nid")).values_list("create_year_month","c")

        # for i in ret:
        #     print(i.title,i.create_time,i.create_year_month)

       # 查询当前站点下的所有文章（当前站点用户所有文章）
        if not kwargs:  #  kwargs 为空字典   ----- > 个人站点首页请求
            article_list = user.article_set.all() # Article.objects.filter(user=user)
        else:           #  kwargs不为空      -------> 分类请求下的一个跳转
             if kwargs.get("condition")=="cate":
                 para=kwargs.get("para")
                 article_list=Article.objects.filter(user=user).filter(homeCategory__nid=para)
             elif kwargs.get("condition")=="tag":
                 para = kwargs.get("para")
                 article_list = Article.objects.filter(user=user).filter(tags__nid=para)
             elif kwargs.get("condition")=="archive":
                 para = kwargs.get("para")
                 article_list=[]
                 for item in dated:
                    if item.create_year_month==para:
                        article_list.append(item)

        page, item = divmod(len(article_list), 5)
        if item:
             page += 1
        d_page = int(request.GET.get("name", 1))
        obj = Pagation(d_page, 5, page, len(article_list),
                        request.path_info)  # 分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
        lip = article_list[obj.start:obj.end]  # 直接引用strat和end方法获取每一页数据的头和尾
        page_fen = obj.huobiao2()  # huobiao方法获取底下该出来的跳转分页码

        return render(request,"home_site.html",locals())
    else:
        return redirect("/zblog/")

def article(request,username,aid):
    user = UserInfo.objects.filter(username=username).first()

    if not user:
        return render(request, "NotFound.html")
    # 查询当前站点对象
    blog = user.blog
    # 方式1：当前站点(用户)下的所有分类名称
    cate_list = blog.homecategory_set.all()

    # 当前站点(用户)下的每一个分类名称以及对应文章个数
    # 方式2：
    from django.db.models import Count
    # ret=HomeCategory.objects.filter(blog=blog).annotate(c=Count("article__nid")).values_list("title","c")
    # print(ret)# <QuerySet [('yuan的数据库', 2), ('yuan的Django', 0), ('yuan的python基础', 1)]>

    # 查询当前站点的每一个标签的名称以及对应的文章数
    tags_list = Tag.objects.filter(blog=blog).annotate(c=Count("article__nid")).values_list("title", "c","nid")

    # 查询每一个年月以及对应的文章数    if sqlite: strftime      mysql: date_format

    dated = Article.objects.filter(user=user).extra(select={"create_year_month": "strftime('%%Y/%%m',create_time)"})

    date_list = dated.values("create_year_month").annotate(c=Count("nid")).values_list("create_year_month", "c")

    # for i in ret:
    #     print(i.title,i.create_time,i.create_year_month)

    # 查询当前站点下的所有文章（当前站点用户所有文章）

    article = Article.objects.get(nid=aid)  # Article.objects.filter(user=user)
    path=request.path

    comment_list = Comment.objects.filter(article__nid=aid)
    return render(request,"article.html",locals())

def up(request):
    response = {"state": False, "error": None}
    article_id=request.POST.get("article_id")
    try:
        user_id=request.user.nid
        try:
            with transaction.atomic():
                ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_down=False)
                Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
                response["state"] = True
        except Exception as e:
            response["error"] = "已经进行过投票"
    except AttributeError:
        response = {"error": "用户未登录"}

    return JsonResponse(response)

def down(request):

    article_id=request.POST.get("article_id")
    try:
        user_id=request.user.nid
        response={"state":False,"error":None}
        try:
            with transaction.atomic():
                ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=False)
                Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)
                response["state"]=True
        except Exception as e:
            response["error"]="已经进行过投票"
    except AttributeError:
        response = {"error": "用户未登录"}

    return JsonResponse(response)

def comment(reuqest):

    try:
        user_id=reuqest.user.nid
        article_id = reuqest.POST.get("articleid")
        content = reuqest.POST.get("content")
        parent_comment_id = reuqest.POST.get("parent_comment_id")
        lou = reuqest.POST.get("louceng")
        users = str(reuqest.user.username)
        uig=str(UserInfo.objects.get(username=users).avatar)
        uname=Article.objects.get(nid=article_id).user.username
        if uname==users:
            response = {"error2": "不能评论自己"}
            return JsonResponse(response)
        else:

            if parent_comment_id:  # 提交子评论
                name = Comment.objects.get(nid=parent_comment_id).user.username
                if name == users:
                    response = {"error2": "不能评论自己"}
                    return JsonResponse(response)
                with transaction.atomic():
                    content = str(content).split("\n")[1]
                    current_comment = Comment.objects.create(user_id=user_id, article_id=article_id, content=content,parent_comment_id=parent_comment_id)
                    Article.objects.filter(nid=article_id).update(comment_count=F("comment_count") + 1)
                    time = current_comment.create_time.strftime("%Y-%m-%d %H:%M")
                    content = str(current_comment.content)
                    nid = current_comment.nid
                    pname=current_comment.parent_comment.user.username
                    pid = current_comment.parent_comment.nid
                    pc = current_comment.parent_comment.content
                    if lou:
                        louceng = ''
                        for item in lou:
                            if item.isdecimal():
                                louceng+=item
                        louceng = int(louceng) + 1
                    else:
                        louceng=1
                    li = {"time": time, "content": content, "users": users, "lou": str(louceng),"pname":pname,"pc":pc,"nid":nid,"pid":pid,"uig":uig}
                    return JsonResponse(li)
            else:  # 提交根评论
                with transaction.atomic():
                    current_comment = Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
                    Article.objects.filter(nid=article_id).update(comment_count=F("comment_count") + 1)
                    time = current_comment.create_time.strftime("%Y-%m-%d %H:%M")
                    nid=current_comment.nid
                    content = str(current_comment.content)
                    if lou:
                        louceng=''
                        for item in lou:
                            if item.isdecimal():
                                louceng+=item
                        louceng = int(louceng) + 1
                    else:
                        louceng=1
                    li = {"time": time, "content": content, "users": users, "lou": str(louceng),"nid":nid,"uig":uig}
                    return JsonResponse(li)
    except AttributeError:
        response = {"error": "用户未登录"}
        return JsonResponse(response)

def get_comment_tree(request,id):

    comment_list=Comment.objects.filter(article__nid=id).values("nid","content","parent_comment_id","create_time","user__username","user__avatar")
    comment_dict = {}

    for comment in comment_list:
        comment["childern_list"] = []
        comment["aid"] = comment["nid"]
        comment_dict[comment["nid"]] = comment
    result = []
    for key, comment in comment_dict.items():
        pid = comment["parent_comment_id"]
        comment['create_time']=comment["create_time"].strftime("%Y-%m-%d %H:%M")
        if pid:  # 子评论：comment
            comment_dict[pid].get("childern_list").append(comment)  # 哈希查询 comment的父comment: comment_dict[pid]
        else:
            result.append(comment)
    print(result)

    return JsonResponse(result,safe=False)

###########后台管理页面

def backend(request,username):
    article_list=Article.objects.filter(user__username=username)
    blog=Blog.objects.filter(userinfo__username=username).first()
    if blog:
        bid=blog.nid
        return render(request,"backend.html",locals())
    else:
        return redirect('/zblog/')
def backendd(request):

    return redirect("/login/")


import datetime
def add_article(request):
    users=request.user.username
    if request.method=="POST":
        title=request.POST.get("title")
        content=request.POST.get("content")

        from bs4 import BeautifulSoup

        soup=BeautifulSoup(content,"html.parser")
        desc=soup.text[0:145]

        user_id=request.user.nid
        username=request.user.username
        sitedetaicategory_id=request.POST.get("site_cate")
        homecategory_id = request.POST.get("blog_cate")
        hometag_id = request.POST.getlist("blog_tag")
        article_obj=Article.objects.create(title=title,user_id=user_id,create_time=datetime.datetime.now(),desc=desc,siteDetaiCategory_id=sitedetaicategory_id,homeCategory_id=homecategory_id)
        for item in hometag_id:
             Article2Tag.objects.create(article=article_obj,tag_id=item)
        ArticleDetail.objects.create(content=content,article=article_obj)

        return redirect("/backend/%s"%username)
    blog = Blog.objects.filter(userinfo__username=users).first()
    if blog:
        siteCategoryList=SiteCategory.objects.all()
        cate_list=HomeCategory.objects.filter(blog__userinfo__username=users)
        tag_list=Tag.objects.filter(blog__userinfo__username=users)
        return render(request,"add_article.html",locals())
    else:
        return redirect('/zblog/')


from cnblog import settings
import os
def upload_img(request):
    file_obj=request.FILES.get("article_img")

    path=os.path.join(settings.MEDIA_ROOT,"img",file_obj.name)

    with open(path,"wb") as f:
        for line in file_obj:
            f.write(line)

    import json

    res={
        "error":0,
        "url":"/media/img/"+file_obj.name
    }

    return HttpResponse(json.dumps(res))
def zblog(request):
    if request.method=="POST":
        title=request.POST.get("title")
        site=request.POST.get("site")
        css = request.POST.get("blogcs")
        user=request.user.username
        blog=Blog.objects.create(title=title,site=site,theme=css)
        UserInfo.objects.filter(username=user).update(blog_id=blog.nid)
        return redirect('/'+user+'/')
    return render(request,"zhuceblog.html")
def addcate(request):
    if request.method=="POST":
        bid=request.POST.get("bid")
        print("bid is",bid)
        cname = request.POST.get("title")
        cc=HomeCategory.objects.create(title=cname,blog_id=bid)
        if cc:
            return HttpResponse("1")
        else:
            return HttpResponse("2")

def addtag(request):
    if request.method=="POST":
        bid=request.POST.get("bid")
        cname = request.POST.get("title")
        cc=Tag.objects.create(title=cname,blog_id=bid)
        if cc:
            return HttpResponse("1")
        else:
            return HttpResponse("2")

def logedit(request):
    user = request.user.username
    if request.method == "POST":
        pre_pwd = request.POST.get("old_pwd")
        new_pwd = request.POST.get("new_pwd")
        user=auth.authenticate(username=user,password=pre_pwd)
        if user:
            user.set_password(new_pwd)
            user.save()
            auth.logout(request)
            return redirect("/index/")
    return render(request,"logedit.html",locals())
def adelete(request):
    if request.method=='POST':
        aid=request.POST.get('nid')
        ac=Article.objects.filter(nid=aid).first()
        if ac:
            Article.objects.filter(nid=aid).delete()
            return HttpResponse("1")
        else:
            return HttpResponse("2")
def edit_article(request,id):
    if request.method=='POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        desc = soup.text[0:145]
        user_id = request.user.nid
        username = request.user.username
        sitedetaicategory_id = request.POST.get("site_cate")
        homecategory_id = request.POST.get("blog_cate")
        hometag_id = request.POST.getlist("blog_tag")
        Article.objects.filter(nid=id).update(title=title,create_time=datetime.datetime.now(),
                                             desc=desc, siteDetaiCategory_id=sitedetaicategory_id,
                                             homeCategory_id=homecategory_id)
        for item in hometag_id:
            Article2Tag.objects.filter(article_id=id).update(tag_id=item)
        ArticleDetail.objects.filter(article_id=id).update(content=content)
    users = request.user.username
    siteCategoryList = SiteCategory.objects.all()

    cate_list = HomeCategory.objects.filter(blog__userinfo__username=users)
    tag_list = Tag.objects.filter(blog__userinfo__username=users)
    ar=Article.objects.filter(nid=id).first()
    ad=ArticleDetail.objects.filter(article_id=id).first()
    tas_id=Article2Tag.objects.filter(article_id=ar.nid).first()
    blog = Blog.objects.filter(userinfo__username=users).first()
    bid = blog.nid

    return render(request, "edit_article.html", locals())



