from django.shortcuts import render
from django.http import HttpResponseRedirect
from mysite import models, forms

def index(request, pid=None, del_pass=None):
    posts = models.Post.objects.filter(enabled=True).order_by('pub_time')[:30]
    print(posts)
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['user_mood']
    except:
        user_id = None
        message = "如果要張貼訊息，則每一個欄位都要填..."
    
    if del_pass and pid:
        try:
            post = models.objects.get(id=pid)
        except:
            post = None
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = "資料刪除成功"
            else:
                message = "密碼錯誤"
    elif user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id,del_pass=user_pass, message=user_post, enabled=True)
        post.save()
        message = "成功儲存！請記得你的邏輯密碼[{}]！訊息需經審查後才會顯示。".format(user_pass)

    return render(request, 'index.html', locals())

def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())

def posting(request):
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['user_mood']
    except:
        user_id = None
        message = "如果要張貼訊息，則每一個欄位都要填..."
    
    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id,del_pass=user_pass, message=user_post, enabled=True)
        post.save()
        message = "成功儲存！請記得你的邏輯密碼[{}]！訊息需經審查後才會顯示。".format(user_pass)

    return render(request, 'posting.html', locals())

def contact(request):
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信"
        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())

def post2db(request):
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            messgae = '您的訊息已儲存，要等管理員啟用後才看得到。'
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如要張貼訊息，則每一個欄位都要填.....'
    else:
        post_form = forms.PostForm()
        # moods = models.Mood.objects.all()
        message = '如要張貼訊息，則每一個欄位都要填.....'
    return render(request, 'post2db.html', locals())
