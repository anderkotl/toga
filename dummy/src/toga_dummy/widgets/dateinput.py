from datetime import date

from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class DateInput(Widget):
    def create(self):
        self._action("create DateInput")

    def get_value(self):
        return self._get_value("value", date.today())

    def set_value(self, value):
        self._set_value("value", value)
        self.interface.on_change(None)

    def get_min_date(self):
        return self._get_value("min date", None)

    def set_min_date(self, value):
        self._set_value("min date", value)

    def get_max_date(self):
        return self._get_value("max date", None)

    def set_max_date(self, value):
        self._set_value("max date", value)
