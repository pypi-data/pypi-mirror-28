from .exceptions import InvalidInput


class Page:

    def __init__(self, start=None, length=None):
        if start and start < 1:
            raise InvalidInput("Start index cannot be less than 1")
        if length and length < 1:
            raise InvalidInput("Page length cannot be less than 1")
        self._start = start or 0
        self._length = length or 10

    def get_start(self):
        return self._start

    def get_length(self):
        return self._length

    def get_end(self):
        return self._start + self.get_length()

    def to_dict(self):
        return {
            "start": self.get_start(),
            "end": self.get_end()
        }


class Pagination:

    def __init__(self, current_page=None):
        if current_page:
            self._current_page = current_page
        else:
            self._current_page = Page()
        self._updated_current_page = None
        self._total_count = 0

    def get_current_page(self):
        return self._current_page

    def update_page_properties(self, current_page_count, total_count):
        self._updated_current_page = Page(self.get_current_page().get_start(), current_page_count)
        self._total_count = total_count

    def get_next_page(self):
        curr_end = self.get_current_page().get_end()
        curr_len = self.get_current_page().get_length()
        if curr_end < self._total_count:
            next_total = self._total_count - curr_end
            next_len = next_total if next_total < curr_len else curr_len
            return Page(curr_end+1, next_len)
        return None

    def get_previous_page(self):
        curr_start = self.get_current_page().get_end()
        if curr_start != 0:
            curr_len = self.get_current_page().get_length()
            prev_len = curr_start if curr_start < curr_len else curr_len
            return Page(curr_start - prev_len, prev_len)
        return None

    def to_dict(self):
        next_page = self.get_next_page()
        if next_page:
            next_page = next_page.to_dict()
        previous_page = self.get_previous_page()
        if previous_page:
            previous_page = previous_page.to_dict()
        return {
            "previous": previous_page,
            "current": self.get_current_page().to_dict(),
            "next": next_page
        }


class Meta:

    def __init__(self, current_page=None, order_by=None):
        self._pagination = Pagination(current_page)
        self._order_by = order_by

    def get_pagination(self):
        return self._pagination

    def get_order_by(self):
        return self._order_by

    def set_order_by(self, *order_by):
        self._order_by = order_by

    def to_dict(self):
        return {
            "page": self.get_pagination().to_dict()
        }
