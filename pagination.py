from settings import PAGE_SIZE


class Pagination:
    position = 0

    def __init__(self, obj):
        self.obj = obj
        self._page_size = PAGE_SIZE

    @property
    def page_count(self):
        return len(self.obj) // self._page_size + 1

    def paginated(self):
        paginated = {}
        for page in range(0, (len(self.obj) // self._page_size) + 1):
            prev_pos = self.position
            paginated[page + 1] = self.obj[self.position:self._page_size + self.position]
            self.position += self._page_size if self._page_size < (len(self.obj) - self.position) else 0
            if prev_pos == self.position:
                break
        return paginated
