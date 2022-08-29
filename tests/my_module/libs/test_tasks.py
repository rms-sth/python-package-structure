import pytest

from my_module.libs.tasks.tasks import TaskProcessor, redis


def test_process_file() -> None:
    deals = TaskProcessor().process_file("deals.json")
    assert type(deals) is list


def test_process_invalid_file() -> None:
    with pytest.raises(Exception):
        TaskProcessor().process_file("invalid_deals.json")


@pytest.fixture
def mock_import_to_redis(monkeypatch) -> None:
    def import_to_redis(self) -> None:
        pass

    monkeypatch.setattr(TaskProcessor, "import_to_redis", import_to_redis)


def test_import_to_redis_using_monkeypatch(mock_import_to_redis) -> None:
    # TODO: monkey patch wont show up in coverage report
    assert TaskProcessor().import_to_redis() is None


class RedisMock:
    @staticmethod
    def set():
        return None

    @staticmethod
    def get():
        return {}


def test_import_to_redis(mocker) -> None:
    mocker.patch("my_module.libs.tasks.tasks.redis")
    redis.Redis.set = RedisMock.set()
    assert TaskProcessor().import_to_redis() is None


def test_read_from_redis(mocker) -> None:
    mocker.patch.object(redis.Redis, "json", return_value={})
    redis.Redis.json.get = RedisMock.get()
    data = TaskProcessor().read_from_redis()
    assert type(data) is dict
