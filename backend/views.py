from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, authenticate  # <--- добавь это
from backend.models import CustomUser as User
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import *
from decimal import Decimal
import random
from django.core.mail import send_mail
from django_countries import countries
from plant_trees import settings
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json


def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

# Create your views here.
@login_required
def home(request):
    user = request.user
    balance = user.balance
    trees_count = Tree.objects.all().count()
    users = CustomUser.objects.all().count()
    countries = CustomUser.objects.values('country').distinct().count()
    trees = Tree.objects.all().order_by('-date_planted')[:8]
    users_with_tree_count = CustomUser.objects.annotate(tree_count=Count('trees')).order_by('-tree_count')

    # Если нужно — найти текущего пользователя в рейтинге
    current_user_position = None
    for index, user in enumerate(users_with_tree_count, start=1):
        if user == request.user:
            current_user_position = index
            break
    return render(request, 'index.html', {
        'balance': balance,
        'trees_count': trees_count,
        'users': users,
        'countries': countries,
        'trees': trees,
        'current_user_position': current_user_position,
    })

@login_required
def ranking(request):
    user = request.user
    balance = user.balance

    # Получаем пользователей с количеством деревьев
    users_with_tree_count = CustomUser.objects.annotate(tree_count=Count('trees')).order_by('-tree_count')

    # Топ-10 пользователей
    top_users = list(users_with_tree_count[:10])

    # Найти позицию текущего пользователя
    current_user_position = None
    for index, user_obj in enumerate(users_with_tree_count, start=1):
        if user_obj == user:
            current_user_position = index
            break

    # Сериализуем список пользователей в список словарей
    users_data = [
        {
            'id': u.id,
            'name': u.get_full_name() or u.full_name,
            'trees': u.tree_count
        }
        for u in users_with_tree_count
    ]

    return render(request, 'eco-ranking.html', {
        'balance': balance,
        'users_data_json': json.dumps(users_data, cls=DjangoJSONEncoder),
        'current_user_id': user.id,
        'current_user_position': current_user_position,
    })

@login_required
def about(request):
    user = request.user
    balance = user.balance
    return render(request, 'about.html', {
        'balance': balance,
    })

@login_required
def upload(request):
    user = request.user
    balance = user.balance
    tree_types = Tree_Type.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'upload.html', {
        'balance': balance,
        'tree_types': tree_types,
    })

@login_required
def profile(request):
    user = request.user
    
    user_trees = Tree.objects.filter(user=user)
    trees_count = user_trees.count()

    # Пересчёт баланса на всякий случай (опционально)
    balance = user.balance
    
    achievements = []
    if trees_count >= 1:
        achievements.append('first_tree')
    if trees_count >= 10:
        achievements.append('ten_trees')
    if trees_count >= 25:
        achievements.append('eco_hero')


    # Подсчёт кислорода и углекислого газа
    total_oxygen = Decimal('0.00')
    total_carbon = Decimal('0.00')

    for tree in user_trees.select_related('tree_type'):
        tree_type = tree.tree_type
        if tree_type.emit_oxygen:
            total_oxygen += tree_type.emit_oxygen
        if tree_type.utilize_carbon:
            total_carbon += tree_type.utilize_carbon

    # Пример: количество дней с момента регистрации
    days_in_app = (date.today() - user.date_joined.date()).days

    if request.method == 'POST' and request.FILES.get('avatar'):
        user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Аватар обновлён!')

    return render(request, 'profile.html', {
        'user': user,
        'trees_count': trees_count,
        'total_oxygen': total_oxygen,
        'total_carbon': total_carbon,
        'days_in_app': days_in_app,
        'balance': balance,
        'achievements': achievements,
    })

@login_required
def my_trees(request):
    trees = Tree.objects.filter(user=request.user).select_related('tree_type').order_by('-date_planted')
    user = request.user
    balance = user.balance
    return render(request, 'my_trees.html', {
        'user': user,
        'trees': trees,
        'balance': balance,
    })

@login_required
def tree_detail(request, tree_id):
    user = request.user
    balance = user.balance
    tree = get_object_or_404(Tree, id=tree_id, user=user)
    total_oxygen = tree.tree_type.emit_oxygen if tree.tree_type.emit_oxygen else Decimal('0.00')
    total_carbon = tree.tree_type.utilize_carbon if tree.tree_type.utilize_carbon else Decimal('0.00')
    return render(request, 'tree_detail.html', {
        'tree_id': tree_id,
        'user': user,
        'balance': balance,
        'tree': tree,
        'total_oxygen': total_oxygen,
        'total_carbon': total_carbon,
    })

@login_required
def upload_tree_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image') or request.FILES.get('photo_initial')
        coordinates = request.POST.get('coordinates')
        tree_type_name = request.POST.get('tree_type')

        if not all([image, coordinates, tree_type_name]):
            messages.error(request, "Пожалуйста, заполните все поля и добавьте фото.")
            return redirect('upload_tree')

        try:
            lat_str, lon_str = coordinates.split(',')
            latitude = Decimal(lat_str.strip())
            longitude = Decimal(lon_str.strip())
        except:
            messages.error(request, "Неверный формат координат.")
            return redirect('upload_tree')

        try:
            tree_type = Tree_Type.objects.get(name=tree_type_name)
        except Tree_Type.DoesNotExist:
            messages.error(request, "Неверный тип дерева.")
            return redirect('upload_tree')

        Tree.objects.create(
            user=request.user,
            tree_type=tree_type,
            photo_initial=image,
            latitude=latitude,
            longitude=longitude,
        )

        messages.success(request, "Дерево успешно загружено! Вы получили монетки :)")
        return redirect('profile')  # или куда хочешь

    tree_types = Tree_Type.objects.all()
    return render(request, 'upload.html', {
        'tree_types': tree_types
    })

@login_required
def rules(request):
    user = request.user
    balance = user.balance
    return render(request, 'rules.html', {
        'balance': balance,
    })

User = get_user_model()

def page_not_found_handler(request, exception):
    return render(request, '404.html', status=404)

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Замените на вашу главную страницу
        else:
            messages.error(request, 'Неверный email или пароль')

    return render(request, 'login.html')

def reset_password_view(request):
    # Не пускаем залогиненных пользователей
    if request.user.is_authenticated:
        return redirect('home')

    step = request.session.get('reset_step', 1)

    if request.method == 'POST':
        if 'step' in request.POST:
            step = int(request.POST['step'])

        # === Шаг 1: Ввод email ===
        if step == 1:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                code = ''.join(random.choices('0123456789', k=4))

                request.session['reset_email'] = email
                request.session['reset_code'] = code
                request.session['reset_step'] = 2

                send_mail(
                    'Код подтверждения',
                    f'Ваш код подтверждения: {code}',
                    settings.DEFAULT_FROM_EMAIL,  # ← это правильно
                    [email],
                    fail_silently = False, 
                )
                return redirect('reset_password')

            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден.')

        # === Шаг 2: Ввод кода ===
        elif step == 2:
            code_input = ''.join([
                request.POST.get('code1', ''),
                request.POST.get('code2', ''),
                request.POST.get('code3', ''),
                request.POST.get('code4', '')
            ])
            if code_input == request.session.get('reset_code'):
                request.session['reset_step'] = 3
                return redirect('reset_password')
            else:
                messages.error(request, 'Неверный код подтверждения.')

        # === Шаг 3: Ввод нового пароля ===
        elif step == 3:
            password1 = request.POST.get('newPassword')
            password2 = request.POST.get('confirmNewPassword')

            if password1 != password2:
                messages.error(request, 'Пароли не совпадают.')
            else:
                email = request.session.get('reset_email')
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()

                request.session.flush()
                return redirect('login')  # ✅ гарантированно сработает

    # Рендер шаблона по умолчанию
    context = {
        'step': request.session.get('reset_step', 1),
        'email': request.session.get('reset_email', ''),
    }
    return render(request, 'forgot_password.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    country_list = list(countries)

    if request.method == 'POST':
        step = int(request.POST.get('step', 1))

        if step == 1:
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone = request.POST.get('phone_number')
            country = request.POST.get('country')
            password = request.POST.get('password')
            confirm = request.POST.get('confirmPassword')

            if password != confirm:
                messages.error(request, 'Пароли не совпадают')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email уже используется')
                return redirect('register')

            code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            request.session['register_data'] = {
                'email': email,
                'name': name,
                'phone': phone,
                'country': country,
                'password': password,
                'code': code,
            }

            # Отправка кода по email
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code}',
                settings.DEFAULT_FROM_EMAIL,  # ← это правильно
                [email],
            )

            return render(request, 'register.html', {
                'step': 2,
                'email': email
            })

        elif step == 2:
            entered_code = ''.join([
                request.POST.get('code1', ''),
                request.POST.get('code2', ''),
                request.POST.get('code3', ''),
                request.POST.get('code4', '')
            ])
            saved_data = request.session.get('register_data')

            if saved_data and entered_code == saved_data['code']:
                user = User.objects.create_user(
                    email=saved_data['email'],
                    full_name=saved_data['name'],
                    phone_number=saved_data['phone'],
                    country=saved_data['country'],
                    password=saved_data['password'],
                    is_active=True
                )
                login(request, user)
                del request.session['register_data']
                messages.success(request, 'Аккаунт успешно создан!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный код')
                return render(request, 'register.html', {
                    'step': 2,
                    'email': saved_data.get('email') if saved_data else '',
                })

    return render(request, 'register.html', {'step': 1, 'country_list': country_list})