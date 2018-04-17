
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import  Comment
from .forms import CommentForm

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中, 这是一个类字典对象.
        # 构建 CommentForm 实例, 这样 Django 的表单就生成了.
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False 的作用是仅仅生成 Comment 模型类的实例, 但还不保存到评论数据库.
            comment = form.save(commit=False)
            # 将评论和文章关联起来
            comment.post = post
            # 最终存进数据库, 调用模型实例的 save 方法.
            comment.save()
            # redirect() 可以接收两种参数
            # 1. url的name  直接重定向到 此url
            # 2. 模型实例 但是要求本模型必须实现了 get_absolute_url 方法.
            return redirect(post)
        else:
            # 反向获取该文章下的所有评论
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求, 说明用户没有提交数据, 重定向到文章详情页.
    return redirect(post)

