from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductType, Product, Transaction
from .forms import TransactionForm, ProductAddForm, ProductUpdateForm


def item_list(request):
    user_profile = request.user.profile
    sell_products = Product.objects.filter(owner=user_profile)
    buy_products = Product.objects.exclude(owner=user_profile)
    sell_product_types = ProductType.objects.filter(products__owner=user_profile)
    buy_product_types = ProductType.objects.exclude(products__owner=user_profile)
    return render(request, "item_list.html", {'buy_products': buy_products, 'buy_product_types': buy_product_types, 'sell_products': sell_products, 'sell_product_types': sell_product_types})


def item_entry(request, num=1):

    product = Product.objects.get(id=num)
    product_type = product.product_type
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            existing_transaction = Transaction.objects.filter(buyer=request.user.profile, product=product, status='CAR').first()

            if existing_transaction:
                form.add_error(None, "This product is already in your cart.")
            else:
                amount = form.cleaned_data['amount']

                if amount > product.stock:
                    form.add_error('quantity', f"Only {product.stock} items in stock.")
                else:
                    transaction = form.save(commit=False)
                    transaction.buyer = request.user.profile
                    transaction.product = product
                    transaction.status = 'CAR'
                    transaction.save()

                    product.stock -= amount
                    product.save()

                    return redirect("item_cart")
    
    return render(request, "item_entry.html", {'product': product, 'product_type': product_type, 'transaction_form': form})

@login_required
def item_add(request):
    form = ProductAddForm()
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect('item_list')
    return render(request, "item_add.html", {'add_form': form})

@login_required
def item_edit(request, num=1):
    product = Product.objects.get(id=num)
    form = ProductUpdateForm(instance=product)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('item_entry', num)
    return render(request, 'item_edit.html', {'edit_form': form, 'product': product})

@login_required
def item_cart(request):
    # buyer transactions
    transactions = Transaction.objects.filter(buyer=request.user.profile)
    return render(request, "item_cart.html", {'transactions': transactions})
    

@login_required
def item_transactions(request):
    # seller transactions
    transactions = Transaction.objects.filter(product__owner=request.user.profile)
    return render(request, "item_transactions.html", {'transactions': transactions})
