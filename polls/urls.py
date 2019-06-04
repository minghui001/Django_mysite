from django.urls import path
from .import views

app_name = 'polls'
urlpatterns=[
    # /polls/
    path(r'',views.index,name='index'),
    # /polls/hello.html
    path('hello.html',views.hello,name='hello'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]