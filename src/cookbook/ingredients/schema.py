import graphene

from graphene import relay

from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node, )

    name = graphene.String(description="The name of Category.")


class MutateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category = CategoryType(name=name)
        return MutateCategory(category=category)


class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateCategory(graphene.Mutation):
    class Arguments:
        category_data = CategoryInput(required=True)

    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, category_data=None):
        category = Category.objects.create(name=category_data.name)
        return CreateCategory(category=category)


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Mutations(object):
    mutate_category = MutateCategory.Field()
    create_category = CreateCategory.Field()


class Query(object):
    category = graphene.Field(
        CategoryType,
        id=graphene.Int(),
        name=graphene.String()
    )

    all_categories = graphene.List(CategoryType)

    ingredient = graphene.Field(
        IngredientType,
        id=graphene.Int(),
        name=graphene.String()
    )

    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None

