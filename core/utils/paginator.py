import math
from typing import List, Tuple


class Paginator:
    def __init__(self, array: List | Tuple, page: int = 1, per_page: int = 1):
        self.array = array
        self.page = page
        self.per_page = per_page
        self.len = len(self.array)

        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self) -> List | Tuple:
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self) -> List | Tuple:
        page_items = self.__get_slice()
        return page_items

    def has_next(self) -> int | bool:
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self) -> int | bool:
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self) -> List | Tuple:
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(
            "Следующая страница не существует. Используйте has_next(), чтобы проверить, существует ли следующая страница."
        )

    def get_previous(self) -> List | Tuple:
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(
            "Предыдущая страница не существует. Используйте has_previous(), чтобы проверить, существует ли предыдущая страница."
        )