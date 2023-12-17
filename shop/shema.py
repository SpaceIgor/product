import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, Shop, Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    cheapest_products = graphene.List(ProductType)

    def resolve_cheapest_products(self, info):
        cheapest_products = []
        categories = ()

        for i in Category.allowed_categories.values():
            categories += i

        shops = Shop.objects.all()

        for shop in shops:
            for category in categories:
                cheapest_product = Product.objects.filter(
                    shop=shop,
                    categories=category
                ).order_by('price').first()

                if cheapest_product:
                    cheapest_products.append(cheapest_product)

        return cheapest_products


schema = graphene.Schema(query=Query)