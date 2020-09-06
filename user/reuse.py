from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def login_check(view_func):
    @wraps(view_func)
    def check_session(request):
            #从session里面取取username字段的值，若取不到则表明没有用户登录，取得到说明有
        username=request.session.get('username')
        if not username:
            return redirect(reverse('user:login'))
        else:
            return view_func(request)
    return check_session

