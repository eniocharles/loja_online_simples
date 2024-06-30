from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Cart, CartItem, Order, OrderItem

class ProductListView(ListView):
    # Define o modelo usado para esta view.
    model = Product
    # Especifica o template a ser usado para renderizar esta view.
    template_name = 'product_list.html'
    # Define o nome do contexto para ser usado no template.
    context_object_name = 'products'


class ProductDetailView(DetailView):
    # Define o modelo usado para esta view.
    model = Product
    # Especifica o template a ser usado para renderizar esta view.
    template_name = 'product_detail.html'
    # Define o nome do contexto para ser usado no template.
    context_object_name = 'product'


def add_to_cart(request, product_id):
    # Obtém ou cria um carrinho com base no 'cart_id' armazenado na sessão.
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    # Obtém o produto com base no 'product_id', ou retorna um erro 404 se não for encontrado.
    product = get_object_or_404(Product, id=product_id)
    # Obtém ou cria um item do carrinho com base no carrinho e produto.
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # Incrementa a quantidade do item do carrinho.
    cart_item.quantity += 1
    # Salva o item do carrinho atualizado.
    cart_item.save()
    # Armazena o 'cart_id' na sessão.
    request.session['cart_id'] = cart.id
    # Redireciona para a view do carrinho.
    return redirect('cart')


class CartView(TemplateView):
    # Especifica o template a ser usado para renderizar esta view.
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        # Obtém o contexto padrão fornecido pela classe base.
        context = super().get_context_data(**kwargs)
        # Obtém o carrinho com base no 'cart_id' armazenado na sessão.
        cart = Cart.objects.get(id=self.request.session.get('cart_id'))
        # Adiciona os itens do carrinho ao contexto.
        context['cart_items'] = cart.items.all()
        # Calcula o preço total dos itens no carrinho e adiciona ao contexto.
        context['total_price'] = sum(item.get_total_price() for item in cart.items.all())
        return context


def cancel_order(request):
    # Obtém o carrinho com base no 'cart_id' armazenado na sessão.
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    # Deleta todos os itens do carrinho.
    cart.items.all().delete()
    # Redireciona para a view do carrinho.
    return redirect('cart')


class CheckoutView(TemplateView):
    # Especifica o template a ser usado para renderizar esta view.
    template_name = 'order_confirmation.html'

    def post(self, request, *args, **kwargs):
        # Obtém o carrinho com base no 'cart_id' armazenado na sessão.
        cart = Cart.objects.get(id=request.session.get('cart_id'))
        # Cria um novo pedido com as informações fornecidas.
        order = Order.objects.create(
            customer=request.user,
            address=request.POST.get('address'),
            total_price=sum(item.get_total_price() for item in cart.items.all())
        )
        # Para cada item no carrinho, cria um item de pedido correspondente.
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        # Deleta todos os itens do carrinho após o pedido ser feito.
        cart.items.all().delete()
        # Renderiza a template de confirmação de pedido com o pedido criado.
        return render(request, 'order_confirmation.html', {'order': order})