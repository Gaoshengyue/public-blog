
#使用方法：
# d_page=int(request.GET.get("name",1))
#     obj=Pagation(d_page,10,11,len(li),request.path_info)  #分别要传的值(当前页，每一页放多少数据，每一页放多少个跳转按钮，数据的长度，当前的url)
#
#     lip = li[obj.start:obj.end]      #直接引用strat和end方法获取每一页数据的头和尾
#     page_fen=obj.huobiao()           #huobiao方法获取底下该出来的跳转分页码
#     return render(request, "class.html", {"list": lip, "page_fen": page_fen, "user": user})



class Pagation(object):
    def __init__(self, d_page,put_page,page_xi,all_c,r_url):
        self.d_page=d_page
        self.put_page=put_page
        self.page_xi=page_xi
        self.all_c=all_c
        self.r_url=r_url
    @property
    def start(self):
        start = (self.d_page - 1) * self.put_page
        return start
    @property
    def end(self):
        end = (self.d_page) * self.put_page
        return end
    def huobiao(self):
        all_page, tem = divmod(self.all_c, self.put_page)
        if tem:
            all_page += 1
        pa_half = int((self.page_xi - 1) / 2)
        if self.d_page <= pa_half:
            pager_start = 1
            pager_end = self.page_xi
        elif self.d_page >= all_page - pa_half:
            if all_page - pa_half<=0:
                pager_start = 1
                pager_end = self.page_xi
            elif self.d_page==all_page:
                pager_start = 1
                pager_end = self.page_xi
            else:
                pager_start = all_page - self.page_xi
                pager_end = all_page
        else:
            pager_start = self.d_page - pa_half
            if pa_half==0:
                pager_end=self.d_page+1
            else:
                pager_end = self.d_page + pa_half+1
        page_fen = []
        first = '<li><a href="%s&name=1">首页</a></li>' % (self.r_url)
        page_fen.append(first)
        if self.d_page > 1:
            prev = '<li><a href="%s&name=%s">上一页</a></li>' % (self.r_url, self.d_page - 1)
            page_fen.append(prev)
        for i in range(pager_start, pager_end + 1):
            if i == self.d_page:
                temp = '<li class="active"><a href="%s&name=%s">%s</a></li>' % (self.r_url, i, i,)
            else:
                temp = '<li><a href="%s&name=%s">%s</a></li>' % (self.r_url, i, i,)
            page_fen.append(temp)
        if self.d_page < all_page:
            prev = '<li><a href="%s&name=%s">下一页</a></li>' % (self.r_url, self.d_page + 1)
            page_fen.append(prev)
        last = '<li><a href="%s&name=%s">尾页</a></li>' % (self.r_url, all_page)
        page_fen.append(last)
        return  page_fen

    def huobiao2(self):
        all_page, tem = divmod(self.all_c, self.put_page)
        if tem:
            all_page += 1
        pa_half = int((self.page_xi - 1) / 2)
        if self.d_page <= pa_half:
            pager_start = 1
            pager_end = self.page_xi
        elif self.d_page >= all_page - pa_half:
            if all_page - pa_half<=0:
                pager_start = 1
                pager_end = self.page_xi
            elif self.d_page==all_page:
                pager_start = 1
                pager_end = self.page_xi
            else:
                pager_start = all_page - self.page_xi
                pager_end = all_page
        else:
            pager_start = self.d_page - pa_half
            if pa_half == 0:
                pager_end = self.d_page + 1
            else:
                pager_end = self.d_page + pa_half
        page_fen = []
        first = '<li><a href="%s?name=1">首页</a></li>' % (self.r_url)
        page_fen.append(first)
        if self.d_page > 1:
            prev = '<li><a href="%s?name=%s">上一页</a></li>' % (self.r_url, self.d_page - 1)
            page_fen.append(prev)
        for i in range(pager_start, pager_end + 1):
            if i == self.d_page:
                temp = '<li class="active"><a href="%s?name=%s">%s</a></li>' % (self.r_url, i, i,)
            else:
                temp = '<li><a href="%s?name=%s">%s</a></li>' % (self.r_url, i, i,)
            page_fen.append(temp)
        if self.d_page < all_page:
            prev = '<li><a href="%s?name=%s">下一页</a></li>' % (self.r_url, self.d_page + 1)
            page_fen.append(prev)
        last = '<li><a href="%s?name=%s">尾页</a></li>' % (self.r_url, all_page)
        page_fen.append(last)
        return page_fen