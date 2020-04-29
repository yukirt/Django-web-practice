from django.shortcuts import render
from datetime import datetime

def index(request, tvno = 0):
    tv_list = [
        {'name': '東森', 'tvcode': 'RaIJ767Bj_M'},
        {'name': '民視', 'tvcode': 'XxJKnDLYZz4'},
        {'name': '台視', 'tvcode': 'NbjI0cARzjQ'},
        {'name': '華視', 'tvcode': 'TL8mmew3jb8'},
    ]
    now = datetime.now()
    tvno = tvno
    tv = tv_list[tvno]
    return render(request, 'index.html',locals())