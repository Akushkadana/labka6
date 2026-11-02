
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductCRUDTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test product",
            description="Test description",
            price=Decimal("100.00")
        )

    # READ: проверяем открытие списка товаров
    def test_product_list_status_code(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)

    # READ: проверяем отображение товара
    def test_product_list_contains_product(self):
        response = self.client.get(reverse("product_list"))
        self.assertContains(response, "Test product")

    # CREATE: проверяем открытие страницы создания
    def test_product_create_page(self):
        response = self.client.get(reverse("product_create"))
        self.assertEqual(response.status_code, 200)

    # CREATE: проверяем создание нового товара
    def test_product_create(self):
        self.client.post(
            reverse("product_create"),
            {
                "name": "New product",
                "description": "New description",
                "price": "250.00",
            }
        )

        self.assertTrue(
            Product.objects.filter(name="New product").exists()
        )

    # UPDATE: проверяем открытие страницы редактирования
    def test_product_update_page(self):
        response = self.client.get(
            reverse(
                "product_update",
                kwargs={"pk": self.product.pk}
            )
        )
        self.assertEqual(response.status_code, 200)

    # UPDATE: проверяем изменение данных товара
    def test_product_update(self):
        self.client.post(
            reverse(
                "product_update",
                kwargs={"pk": self.product.pk}
            ),
            {
                "name": "Updated product",
                "description": "Updated description",
                "price": "150.00",
            }
        )

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, "Updated product")
        self.assertEqual(
            self.product.description,
            "Updated description"
        )
        self.assertEqual(
            self.product.price,
            Decimal("150.00")
        )

    # DELETE: проверяем открытие страницы удаления
    def test_product_delete_page(self):
        response = self.client.get(
            reverse(
                "product_delete",
                kwargs={"pk": self.product.pk}
            )
        )
        self.assertEqual(response.status_code, 200)

    # DELETE: проверяем удаление товара
    def test_product_delete(self):
        self.client.post(
            reverse(
                "product_delete",
                kwargs={"pk": self.product.pk}
            )
        )

        self.assertFalse(
            Product.objects.filter(pk=self.product.pk).exists()
        )
