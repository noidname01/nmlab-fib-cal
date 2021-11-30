from django.urls import path, re_path

from .views import FibView,LogsView

urlpatterns = [
    re_path(r'^fibonacci/?$', FibView.as_view()),
    re_path(r'^logs/?$', LogsView.as_view())
]
