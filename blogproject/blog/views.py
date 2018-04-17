from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Post, Tag
from comments.forms import CommentForm
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from django.core.paginator import Paginator

def home(request):
    return redirect('blog:index', pageid=1)

def index(request, pageid):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    # 得到当前页数据
    c_page = paginator.page(pageid)
    context = {'post_list': c_page}
    return render(request, 'blog/index.html', context=context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite', # 语法高亮扩展
            # 'markdown.extensions.toc', # 允许自动生成目录
            TocExtension(slugify=slugify)
        ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month,
    )
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})

from django.db.models import Q
def search(request):
    q = request.GET.get('q')
    error_msg = '您搜索的内容我们还有没有收录哟 !'

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render (request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})

import qrcode
from django.utils.six import BytesIO

def QRinput(request):
    return render(request, 'qrinput.html')
def createQR(request):
    # print(request.POST['QRcode'])
    word = request.POST.get('QRcode', 'http://39.106.125.164/')
    # 传入网站(文字)计算出二维码图片字节数
    img = qrcode.make(word)
    # 创建一个 BytesIO 临时保存生成的图片数据
    buf = BytesIO()
    # 将图片字节数据放到 BytesIO 中临时保存
    img.save(buf)
    # 在 BytesIo 临时拿出数据
    img_stream = buf.getvalue()
    response = HttpResponse(img_stream, content_type="image/jpg")
    return response

def TagView(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={'post_list': post_list})


