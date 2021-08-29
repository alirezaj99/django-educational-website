from django.shortcuts import render

# ERRORS

def view_404(request, exception):
    context = {

    }
    return render(request, "errors/404.html", context)


def view_403(request, exception):
    context = {

    }
    return render(request, "errors/403.html", context)


def view_400(request, exception):
    context = {

    }
    return render(request, "errors/400.html", context)


def view_500(request):
    context = {

    }
    return render(request, "errors/500.html", context)
