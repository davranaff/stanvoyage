

class Pagination:
    __slots__ = ('model', 'per_page')

    def __init__(self, model, per_page=4):
        self.model = model
        self.per_page = per_page

    def next_page(self, page):
        self.model.objects.filter()

    def previous_page(self):
        ...
