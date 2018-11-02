from settings import PAGE_SIZE


class Pagination:
    def __init__(self, obj):
        self.obj = obj
        self._page_size = PAGE_SIZE

    @property
    def page_count(self):
        return len(self.obj) // self._page_size + 1

    def paginated(self, page):
        return self.obj[self._page_size * (page - 1):self._page_size * page]
