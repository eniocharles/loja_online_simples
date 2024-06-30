from django.db import models

class Product(models.Model):
    # O campo 'name' é um CharField com um limite máximo de 255 caracteres.
    name = models.CharField(max_length=255)
    
    # O campo 'short_description' é um CharField com um limite máximo de 255 caracteres.
    short_description = models.CharField(max_length=255)
    
    # O campo 'long_description' é um TextField para descrições mais longas.
    long_description = models.TextField()
    
    # O campo 'price' é um DecimalField com até 10 dígitos no total, e 2 casas decimais.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # O campo 'stock' é um PositiveIntegerField para armazenar a quantidade de produtos em estoque.
    stock = models.PositiveIntegerField()
    
    # O campo 'image' é um ImageField para armazenar imagens dos produtos, com upload para a pasta 'products/'.
    image = models.ImageField(upload_to='products/')

    # O método __str__ retorna uma representação legível do objeto Product.
    def __str__(self):
        return self.name


class Cart(models.Model):
    # O campo 'created_at' é um DateTimeField que armazena a data e hora em que o carrinho foi criado.
    # auto_now_add=True indica que o campo será preenchido automaticamente quando o objeto for criado.
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # O campo 'cart' é uma ForeignKey que se refere ao modelo Cart, com related_name='items' para acessar os itens do carrinho.
    # on_delete=models.CASCADE indica que se o carrinho for deletado, os itens do carrinho também serão deletados.
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    
    # O campo 'product' é uma ForeignKey que se refere ao modelo Product.
    # on_delete=models.CASCADE indica que se o produto for deletado, os itens do carrinho também serão deletados.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # O campo 'quantity' é um PositiveIntegerField que armazena a quantidade do produto no carrinho.
    quantity = models.PositiveIntegerField()

    # O método get_total_price calcula e retorna o preço total dos itens do carrinho.
    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    # O campo 'customer' é uma ForeignKey que se refere ao modelo de usuário padrão do Django ('auth.User').
    # on_delete=models.CASCADE indica que se o usuário for deletado, o pedido também será deletado.
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    # O campo 'address' é um CharField com um limite máximo de 255 caracteres.
    address = models.CharField(max_length=255)
    
    # O campo 'total_price' é um DecimalField com até 10 dígitos no total, e 2 casas decimais.
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # O campo 'created_at' é um DateTimeField que armazena a data e hora em que o pedido foi criado.
    # auto_now_add=True indica que o campo será preenchido automaticamente quando o objeto for criado.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # O campo 'updated_at' é um DateTimeField que armazena a data e hora da última atualização do pedido.
    # auto_now=True indica que o campo será atualizado automaticamente toda vez que o objeto for salvo.
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    # O campo 'order' é uma ForeignKey que se refere ao modelo Order, com related_name='items' para acessar os itens do pedido.
    # on_delete=models.CASCADE indica que se o pedido for deletado, os itens do pedido também serão deletados.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    # O campo 'product' é uma ForeignKey que se refere ao modelo Product.
    # on_delete=models.CASCADE indica que se o produto for deletado, os itens do pedido também serão deletados.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # O campo 'quantity' é um PositiveIntegerField que armazena a quantidade do produto no pedido.
    quantity = models.PositiveIntegerField()