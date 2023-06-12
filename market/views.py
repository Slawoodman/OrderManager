from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, OrderItem
from .forms import OrderCreatForm
from .utils import get_choices, filter_orders
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
import mimetypes


def mainpage(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "market/main.html", context)


def get_orders(request):
    data = OrderItem.objects.all()
    orders = filter_orders(request, data)

    context = {"orders": orders}
    return render(request, "market/order_list.html", context)


@login_required(login_url="login")
def createUserOrder(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = OrderCreatForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = item
            order.customer = request.user
            order.save()
            return redirect("showorders")
    else:
        form = OrderCreatForm()
    context = {"form": form}
    return render(request, "market/order_form.html", context)


def mark_order_item_as_paid(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    order_item.paid()
    return redirect("showorders")


def change_order_status(request, pk):
    order = get_object_or_404(OrderItem, id=pk)
    choices = get_choices(request, order)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(OrderItem.STATUS_CHOICES):
            order.status = status
            order.save()
            return redirect("showorders")
        else:
            return HttpResponse("Wrong value")

    context = {"order": order, "page": "edit", "choices": choices}
    return render(request, "market/order_form.html", context)


def generate_payment_html(request, pk):
    order_item = OrderItem.objects.get(id=pk)
    file_name = "payment.html"
    context = {
        "order_item": order_item,
    }
    html_content = render_to_string("market/payment_template.html", context)

    # Save the HTML content to the OrderItem instance
    order_item.file.save(file_name, ContentFile(html_content), save=True)

    return redirect("showorders")
    # return render(request, 'market/payment_template.html', context)


def download_file(request, pk):
    # Retrieve the order item from the database
    order_item = OrderItem.objects.get(id=pk)

    # Determine the content type based on the file extension
    file_extension = order_item.file.name.split(".")[-1]
    content_type, _ = mimetypes.guess_type(file_extension)

    # Create a response with the file content
    response = HttpResponse(order_item.file, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{order_item.file.name}"'

    return response
