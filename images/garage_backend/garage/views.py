from django.shortcuts import render


def home(request, *args, **kwargs):
    return render(request, 'home.html')


def about(request, *args, **kwargs):
    my_context = {
        "About": {
            "Name": ['Titus'],
            "email": ['kiptootitus75@gmail.com'],
            "phone_number": +254705830228
        },
        "Education": 'Karatina University'
    }
    return render(request, 'about.html', my_context)


def contact(request, *args, **kwargs):
    return render(request, 'contact.html')
