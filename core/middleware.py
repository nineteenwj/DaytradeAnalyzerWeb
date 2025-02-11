from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 定义不需要登录就能访问的URL列表
        exempt_urls = [
            '/login/',
            '/register/',
            '/reset-password/',
            '/simulate/',
            '/opening_buy_strategy/',
        ]

        # 检查当前路径是否在豁免列表中
        current_path = request.path_info
        if not request.user.is_authenticated:
            for exempt_url in exempt_urls:
                if current_path.startswith(exempt_url):
                    return self.get_response(request)
            # 如果用户未登录且访问的不是豁免URL，重定向到登录页面
            return redirect('login')

        return self.get_response(request)