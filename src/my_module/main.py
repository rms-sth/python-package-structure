"""
Package interface.
This is the main package interface.
"""
from my_module.libs.tasks.tasks import TaskProcessor


def main() -> None:
    print("Executing main function....")
    # TaskProcessor().import_to_redis()
    TaskProcessor().read_from_redis()


if __name__ == "__main__":
    main()
