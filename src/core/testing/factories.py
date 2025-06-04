from functools import partial

import pytz
from faker import Faker
from mixer.backend.django import mixer


def register(method):
    name = method.__name__
    FixtureRegistry.METHODS[name] = method

    return method


class FixtureRegistry:
    METHODS: dict = {}

    def get(self, name):
        method = self.METHODS.get(name)

        if not method:
            message = f"Factory method “{name}” not found."
            raise AttributeError(message)

        return method


class CycleFixtureFactory:
    def __init__(self, factory, count):
        self.count = count
        self.factory = factory

    def __getattr__(self, name):
        if hasattr(self.factory, name):
            return lambda *args, **kwargs: [getattr(self.factory, name)(*args, **kwargs) for _ in range(self.count)]

        return None


class FixtureFactory:
    def __init__(self):
        self.mixer = mixer
        self.registry = FixtureRegistry()

    def __getattr__(self, name):
        method = self.registry.get(name)

        return partial(method, self)

    def cycle(self, count):
        return CycleFixtureFactory(self, count)

    def future_datetime(self, end_date="+30d", tzinfo=None):
        tzinfo = tzinfo or pytz.timezone("Europe/Moscow")

        return self.faker.future_datetime(end_date=end_date, tzinfo=tzinfo)

    def past_datetime(self, start_date="-30d", tzinfo=None):
        tzinfo = tzinfo or pytz.timezone("Europe/Moscow")

        return self.faker.past_datetime(start_date=start_date, tzinfo=tzinfo)

    @property
    def faker(self):
        return Faker()
