from django.db.models import TextChoices
from asgiref.sync import sync_to_async
from viewflow.fsm import State


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""
    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'


class UserFlow:
    """Отвечает за механизм работы состояний пользователя.

    Принимает объект пользователя и взаимодействует с ORM
    в асинхронном режиме.
    """
    state = State(UserStates, default=UserStates.START)

    def __init__(self, user):
        self.user = user

    @state.getter()
    def _get_user_state(self):
        return self.user.state

    @state.setter()
    def _set_user_state(self, value):
        self.user.state = value

    @state.transition(source=State.ANY, target=UserStates.SCHEDULE)
    def _schedule(self):
        pass

    @state.transition(source=state.ANY, target=UserStates.START)
    def _start(self):
        pass

    @state.transition(source=state.ANY, target=UserStates.HELP)
    def _help(self):
        pass

    def _sync_save(self):
        self.user.save()

    async def schedule(self):
        self._schedule()
        await sync_to_async(self._sync_save)()

    async def start(self):
        self._start()
        await sync_to_async(self._sync_save)()

    async def help(self):
        self._help()
        await sync_to_async(self._sync_save)()