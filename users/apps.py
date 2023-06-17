from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # ? To Create a data tuple in Profile table when a new user is created
    def ready(self) -> None:
        import users.signals
        