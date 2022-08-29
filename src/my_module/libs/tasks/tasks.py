import datetime
import json
import os
import time

import redis
from redis.commands.json.path import Path

resource_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources"
)


def create_tasks(some_parameter: str | None = None) -> bool:  # noqa: D103
    return True


class TaskProcessor:
    def __init__(self, filename: str = "deals.json", index: str = "deals") -> None:
        self.filename = filename
        self.index = index
        self.client = redis.Redis(host="localhost", port=5439, password="")

    def format_timestamp(self, datum: dict, time_type: str = "created_at") -> str:
        formatted_time = (
            datetime.datetime.fromisoformat(datum["_source"][time_type])
            if time_type in datum["_source"]
            else None
        )
        formatted_time = (
            datetime.datetime.timestamp(formatted_time) if formatted_time else time.time()
        )
        return formatted_time

    def format_data(self, data: str) -> dict:
        datum: dict = json.loads(data)

        created_at = self.format_timestamp(datum, "created_at")
        updated_at = self.format_timestamp(datum, "updated_at")
        formatted_data: dict = {
            "id": datum["_id"],
            "created_at_timestamp": created_at,
            "updated_at_timestamp": updated_at,
            **datum["_source"],
        }
        return formatted_data

    def process_file(self, file_name: str = "") -> list[dict]:
        """reads all the data from the given file name, process to valid format"""
        try:
            file_path: str = resource_path + "/data/" + file_name
            merged_data: list = []
            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    formatted_data = self.format_data(line)
                    merged_data.append(formatted_data)
            return merged_data
        except Exception as e:
            raise e

    def import_to_redis(self) -> None:
        data = self.process_file(self.filename)
        self.client.json().set(self.index, Path.root_path(), data)

    def read_from_redis(self):
        result = self.client.json().get(self.index)
        print(result)
