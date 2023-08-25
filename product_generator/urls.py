from django.urls import path
from product_generator.views import GenerateProductView

app_name = "product_generator"

urlpatterns = [
    path("generate-product/", GenerateProductView.as_view(), name="generate_product"),
]
