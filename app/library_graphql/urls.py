from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from . import views

app_name = 'library_graphql'

urlpatterns = [
    path('', views.index, name='index'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
    path('reset-data/', views.reset_data, name='reset_data'),
] 