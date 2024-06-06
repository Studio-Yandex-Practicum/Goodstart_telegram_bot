from django.db.models import TextChoices
from viewflow.fsm import State


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'


class UserFlow:
    """
    Finite State Machine базе Postgres.

    Определяет механику переходов
    из состояния в состояние и обеспечивает
    асинхонное взаимодействие с Django ORM.
    """

    state = State(UserStates, default=UserStates.START)

    def __init__(self, user):
        """Принимает объект пользователя."""
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

    async def schedule(self):
        """Переход в положение 'Расписание'. Асинхронный метод."""
        self._schedule()
        await self.user.asave()

    async def start(self):
        """Переход в положение 'Старт'. Асинхронный метод."""
        self._start()
        await self.user.asave()

    async def help(self):
        """Переход в положение 'Помощь'. Асинхронный метод."""
        self._help()
        await self.user.asave()
