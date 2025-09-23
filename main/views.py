from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.db.models import Q

from .models import Category, Product, Size


# IndexView — це клас-представлення (view), який відповідає за головну сторінку сайту.
# Ми успадковуємо його від TemplateView, бо нам потрібно відображати шаблон з контекстом.
class IndexView(TemplateView):
    # Основний шаблон, який використовується для рендерингу сторінки.
    template_name = 'main/base.html'

    # Метод формує дані (контекст), які ми передаємо у шаблон.
    def get_context_data(self, **kwargs):
        # Викликаємо базову реалізацію, щоб отримати стандартний контекст.
        context = super().get_context_data(**kwargs)

        # Додаємо до контексту список усіх категорій (для меню або фільтрів).
        context['categories'] = Category.objects.all()

        # Додаємо поточну категорію. За замовчуванням — None (нічого не вибрано).
        context['current_category'] = None

        return context

    # Перевизначаємо метод GET, який викликається при завантаженні сторінки.
    def get(self, request: HttpRequest, *args, **kwargs):
        # Отримуємо контекст через метод get_context_data.
        context = self.get_context_data(**kwargs)

        # Якщо запит прийшов через HTMX (тобто це AJAX-запит),
        # тоді повертаємо тільки частину сторінки (динамічний контент),
        # щоб не перезавантажувати всю сторінку.
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/home_content.html', context)

        # Якщо це звичайний запит (користувач просто відкрив сторінку),
        # тоді повертаємо повний шаблон.
        return TemplateResponse(request, self.template_name, context)


class CatalogView(TemplateView):
    template_name = 'main/base.html'

    # флажки пошука
    # Словник з правилами фільтрації.
# Ключ — це назва параметра з GET-запиту (?color=red, ?min_price=100 і т.д.).
# Значення — лямбда-функція, яка приймає queryset та значення параметра,
#            і повертає відфільтрований queryset.
    FILTER_MAPPING = {
        'color': lambda queryset, value: queryset.filter(color__iexact=value),
        'min_price': lambda queryset, value: queryset.filter(price__gte=value),
        'max_price': lambda queryset, value: queryset.filter(price__lte=value),
        'size': lambda queryset, value: queryset.filter(product_sizes__size__name=value),
    }

    def get_context_data(self, **kwargs):
        # Отримуємо базовий контекст з батьківського класу
        context = super().get_context_data(**kwargs)

    # Дістаємо slug категорії з параметрів
        category_slug = kwargs.get('category_slug')

    # Отримуємо список усіх категорій
        categories = Category.objects.all()

    # Базовий список продуктів, відсортованих за датою створення
        products = Product.objects.all().order_by('-created_at')

    # Поточна категорія (якщо не вибрана — залишаємо None).
        current_category = None

    # Якщо slug категорії переданий у URL — отримуємо категорію з бази.
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
        # Фільтруємо список продуктів, щоб залишилися тільки ті, що належать цій категорії.
            products = products.filter(category=current_category)

    # Отримуємо пошуковий запит з параметра `q` (?q=сорочка).
        query = self.request.GET.get('q')
        if query:
            # Фільтруємо товари: залишаємо ті, що містять пошуковий текст у назві або описі.
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

    # Словник, куди збережемо обрані параметри фільтрів (щоб передати назад у шаблон).
        filter_params = {}

    # Перебираємо всі доступні фільтри (з FILTER_MAPPING).
        for param, filter_func in self.FILTER_MAPPING.items():
            # Дістаємо значення параметра з URL.
            value = self.request.GET.get(param)
            if value:
                # Якщо параметр переданий — застосовуємо відповідну функцію-фільтр.
                products = filter_func(products, value)
                filter_params[param] = value  # зберігаємо значення для шаблону
            else:
                # Якщо параметр не переданий — кладемо порожній рядок.
                filter_params[param] = ''

    # Додаємо пошуковий запит теж у filter_params (для відображення у формі пошуку).
        filter_params['q'] = query or ''

    # Оновлюємо контекст, щоб передати дані у шаблон.
        context.update({
            'categories': categories,
            'products': products,
            'current_category': current_category,
            'filter_params': filter_params,
            'sizes': Size.objects.all(),
            'search_query': query or '',
        })

    # Логіка відображення пошукової форми (наприклад, щоб відкривати/закривати панель пошуку).
    # якщо параметр show_search=true
        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = False

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # дінамічний контент якшо був запрос, якшо ні вертаємо дефолт
        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                return TemplateResponse(request, 'main/search_input.html', context)
            elif context.get('reset_search'):
                return TemplateResponse(request, 'main/search_button.html', {})
            template = 'main/filter_modal.html' if request.GET.get(
                'show_filters') == 'true' else 'main/catalog.html'
            return TemplateResponse(request, template, context)
        return TemplateResponse(request, self.template, context)


class ProductDetailView(DetailView):
    # Використовуємо готовий generic-клас DetailView для відображення одного об’єкта
    # модель, з якою працюємо (Product)
    model = Product
    template_name = 'main/base.html'         # шаблон за замовчуванням
    slug_field = 'slug'                      # поле, по якому шукаємо продукт
    # ключ у URL (наприклад: /product/<slug>/)
    slug_url_kwarg = 'slug'

    # Додаємо додаткові дані у контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # отримуємо поточний продукт по slug
        # Всі категорії, щоб можна було вивести меню/фільтр
        context['categories'] = Category.objects.all()
        # Схожі продукти (тієї ж категорії, але виключаємо поточний товар)
        context['related_products'] = Product.objects.filter(
            category=product.category,
        ).exclude(id=product.id)[:4]  # обмежуємо 4 штуками
        # Зберігаємо slug категорії для підсвітки/навігації
        context['current_product'] = product.category.slug
        return context

    # Перевизначаємо метод GET
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()                # дістаємо сам продукт
        context = self.get_context_data(**kwargs)      # формуємо контекст
        # Якщо запит зроблений через HTMX (динамічний)
        if request.headers.get('HX-Request'):
            # Віддаємо тільки частковий шаблон з деталями продукту
            return TemplateResponse(request, 'main/product_detail.html', context)
        # Якщо це звичайний запит — повертаємо повну сторінку
        return TemplateResponse(request, self.template_name, context)
