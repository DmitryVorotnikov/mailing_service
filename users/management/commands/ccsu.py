from getpass import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.validators import validate_email

from users.models import User


class Command(BaseCommand):
    """
    python manage.py ccsu - Custom Create SuperUser.
    """
    help = 'Create a superuser with a custom email and password'

    def add_arguments(self, parser):
        """
        Можно передать аргументы как флаги сразу с командой
        или ввести их потом.

        You can pass arguments as flags directly with the command
        or enter them later.
        """
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def validate_email(self, email):
        """
        Валидация email (такая же, как AbstractUser).

        Email validation (same as AbstractUser).
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def validate_password(self, password):
        """
        Валидация password (такая же, как у AbstractBaseUser).

        Password validation (same as AbstractBaseUser).
        """
        try:
            validate_password(password)
            return True
        except ValidationError:
            return False

    def handle(self, *args, **options):
        # По умолчанию запрещено создание пользователя.
        # User creation is not required by default.
        user_creation_required = False

        # Получение email через **options, либо его input. Проверка и валидация.
        # Get email from **options or through input. Check and validate.
        while True:
            email = options['email'] or input('Enter admin email or "exit":\n')
            if email.lower() == 'exit':
                print("User creation canceled!")
                user_creation_required = True
                break
            elif not self.validate_email(email):
                print("Email validation error!")
                continue
            else:
                break

        # Получение password через **options, либо его невидимый input (через getpass). Проверка и валидация.
        # Get password from **options or through a hidden input (using getpass). Check and validate.
        if not user_creation_required:
            while True:
                password = options['password'] or getpass('Enter admin password or "exit":\n')
                if password.lower() == 'exit':
                    user_creation_required = True
                    print("User creation canceled!")
                    break
                elif not self.validate_password(password):
                    print("Password validation error!")
                    continue
                else:
                    break

        # Повторный ввод пароля и проверка.
        # Re-enter the password and check for a match.
        if not user_creation_required:
            while True:
                confirm_password = getpass('Confirm admin password:\n')
                if password != confirm_password:
                    user_creation_required = True
                    print("Passwords do not match. Please try again.")
                    break
                else:
                    break

        # Создание супер-юзера.
        # Create a superuser.
        if not user_creation_required:
            user = User.objects.create(
                email=email,
                first_name='Admin',
                last_name='Admin',
                is_staff=True,
                is_active=True,
                is_superuser=True
            )

            user.set_password(password)
            user.save()
            print('A new superuser has been created!')
