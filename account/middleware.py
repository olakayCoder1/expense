from django.shortcuts import redirect

class LogoutRequiredMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):  
        if request.user.is_authenticated and( request.path == '/signin' or request.path == '/' ):
            return redirect('/dashboard')
        response = self.get_response(request)
        return response






