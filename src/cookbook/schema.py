import graphene

from cookbook.ingredients import schema


class Mutations(schema.Mutations, graphene.ObjectType):
    pass


class Query(schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)

