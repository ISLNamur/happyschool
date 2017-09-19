from django.shortcuts import render


def myapp(request):
    return render(request, template_name="myapp/index.html")