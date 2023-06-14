from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.views import View
from django.http import HttpResponse
from .models import Product, OrderItem
from .forms import OrderCreatForm
from .utils import get_choices, filter_orders
import mimetypes


# Class based view to display the main page
class MainPageView(View):
    # Function to handle HTTP GET requests. It fetches all the products and renders the main page.
    def get(self, request):
        # Fetch all product objects from the database
        products = Product.objects.all()

        # Define context variables that are passed to the template.
        context = {"products": products}

        # Render the 'main.html' template, passing in the context
        return render(request, "market/main.html", context)


# Class based view to display all orders. It uses the LoginRequiredMixin to ensure that only logged in users can access this view.
class GetOrdersView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It fetches all the order items and renders the order list page.
    def get(self, request):
        # Fetch all OrderItem objects from the database
        data = OrderItem.objects.all()

        # Filter the orders based on the current request
        orders = filter_orders(request, data)

        # Define context variables that are passed to the template.
        context = {"orders": orders}

        # Render the 'order_list.html' template, passing in the context.
        return render(request, "market/order_list.html", context)


# Class based view to create a user order. It also uses the LoginRequiredMixin.
class CreateUserOrderView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It renders the order creation form.
    def get(self, request, pk):
        # Fetch the product with the provided primary key (pk)
        item = Product.objects.get(id=pk)

        # Initialize the order creation form
        form = OrderCreatForm()

        # Define context variables that are passed to the template.
        context = {"form": form}

        # Render the 'order_form.html' template, passing in the context
        return render(request, "market/order_form.html", context)

    # Function to handle HTTP POST requests. It performs the order creation operation.
    def post(self, request, pk):
        # Fetch the product with the provided primary key (pk)
        item = Product.objects.get(id=pk)

        # Initialize the order creation form with the data received from the user
        form = OrderCreatForm(request.POST)

        # Check if the form data is valid
        if form.is_valid():
            # If the form data is valid, create a new order instance but don't save it to the database yet.
            order = form.save(commit=False)

            # Assign the product and customer to the order
            order.product = item
            order.customer = request.user

            # Now save the order instance into the database.
            order.save()

            # Redirect to the 'showorders' page.
            return redirect("showorders")

        context = {"form": form}
        # If the form data was not valid, re-render the order form with the form errors.
        return render(request, "market/order_form.html", context)


# Class based view to mark an order item as paid. It also uses the LoginRequiredMixin.
class MarkOrderItemAsPaidView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It marks the order item as paid and redirects to the orders page.
    def get(self, request, pk):
        # Fetch the OrderItem with the provided primary key (pk) or return 404 if it doesn't exist
        order_item = get_object_or_404(OrderItem, id=pk)

        # Mark the order item as paid
        order_item.paid()

        # Redirect to the 'showorders' page.
        return redirect("showorders")


# Class based view to change the status of an order. It also uses the LoginRequiredMixin.
class ChangeOrderStatusView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It displays the form to change the status of an order.
    def get(self, request, pk):
        # Fetch the OrderItem with the provided primary key (pk) or return 404 if it doesn't exist
        order = get_object_or_404(OrderItem, id=pk)

        # Get the status choices for the current order
        choices = get_choices(request, order)

        # Define context variables that are passed to the template.
        context = {"order": order, "page": "edit", "choices": choices}

        # Render the 'order_form.html' template, passing in the context.
        return render(request, "market/order_form.html", context)

    # Function to handle HTTP POST requests. It performs the operation of changing the status of an order.
    def post(self, request, pk):
        # Fetch the OrderItem with the provided primary key (pk) or return 404 if it doesn't exist
        order = get_object_or_404(OrderItem, id=pk)

        # Get the status choices for the current order
        choices = get_choices(request, order)

        # Get the status from the POST data
        status = request.POST.get("status")

        # Check if the status is a valid choice
        if status in dict(OrderItem.STATUS_CHOICES):
            # If it's a valid status, change the status of the order and save it
            order.status = status
            order.save()

            # Redirect to the 'showorders' page.
            return redirect("showorders")
        else:
            # If it's not a valid status, return an error message
            return HttpResponse("Wrong value")


# Class based view to generate a payment HTML file. It also uses the LoginRequiredMixin.
class GeneratePaymentHtmlView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It generates a payment HTML file and redirects to the orders page.
    def get(self, request, pk):
        # Fetch the OrderItem with the provided primary key (pk)
        order_item = OrderItem.objects.get(id=pk)

        # The filename for the payment HTML file
        file_name = "payment.html"

        # Define context variables that are passed to the template.
        context = {"order_item": order_item}

        # Render the payment template as a string
        html_content = render_to_string("market/payment_template.html", context)

        # Save the generated HTML content as a file in the order item
        order_item.file.save(file_name, ContentFile(html_content), save=True)

        # Redirect to the 'showorders' page.
        return redirect("showorders")


# Class based view to download a file. It also uses the LoginRequiredMixin.
class DownloadFileView(LoginRequiredMixin, View):
    # Function to handle HTTP GET requests. It returns the requested file for download.
    def get(self, request, pk):
        # Fetch the OrderItem with the provided primary key (pk)
        order_item = OrderItem.objects.get(id=pk)

        # Get the file extension of the order item's file
        file_extension = order_item.file.name.split(".")[-1]

        # Guess the content type of the file based on its extension
        content_type, _ = mimetypes.guess_type(file_extension)

        # Create a HttpResponse with the order item's file and the guessed content type
        response = HttpResponse(order_item.file, content_type=content_type)

        # Set the 'Content-Disposition' header to suggest a filename to the browser
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{order_item.file.name}"'

        # Return the response
        return response
