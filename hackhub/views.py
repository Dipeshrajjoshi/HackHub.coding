from django.shortcuts import render

# custom view for 404 Page Not Found error
def error_404(request, exception):
    return render(request, '404.html', status=404)

# custom view for 500 Internal Server Error (server crash)
def error_500(request):
    return render(request, '500.html', status=500)

# custom view for 403 Permission Denied error
def error_403(request, exception):
    return render(request, '403.html', status=403)
