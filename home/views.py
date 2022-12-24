from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime, timedelta
from django.db.models import Count, Q, Max
from products.models import Product, Brand
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        product_discount = Product.objects.filter(available=True, discount__isnull=False)
        product_newest = Product.objects.filter(discount__isnull=True).order_by('-created')[:10]

        last_ten_days = datetime.today() - timedelta(days=10)
        product_popular = Product.objects.filter(discount__isnull=True).annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_ten_days))
        ).order_by('-count', '-created')[:10]

        content_type_id = ContentType.objects.get(app_label='products', model='brand').id
        brand_hot = Brand.objects.annotate(
            max=Max('ratings__average', filter=Q(ratings__content_type_id=content_type_id))
        ).order_by('-max', '-name')[:6]

        return render(request, 'home/home.html',
                      {'product_discount': product_discount, 'product_newest': product_newest,
                       'product_popular': product_popular, 'brand_hot': brand_hot})


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'home/contact.html', {'form': form})
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            email = cd['email']
            subject = cd['subject']
            msg = cd['message']
            body = 'نام کاربر: ' + name + '\n' + 'ایمیل کاربر: ' + email + '\n' + 'موضوع: ' + subject + '\n' + '\n\n'\
                   + msg
            form = EmailMessage(
                'فرم ارتباط با ما',
                body,
                '',
                ('email@email.com',),
            )
            form.send(fail_silently=True)
            messages.success(request, 'پیام شما با موفقیت به پشتیبانی سایت ارسال شد', 'success')
    return redirect('home:contact')


def about_view(request):
    return render(request, 'home/about.html')


def faq_view(request):
    return render(request, 'home/faq.html')


def term_view(request):
    return render(request, 'home/term.html')


def custom_page_not_found_view(request, exception):
    return render(request, "home/404.html", status=404)


def custom_server_error_view(request, exception=None):
    return render(request, "home/500.html", status=500)

