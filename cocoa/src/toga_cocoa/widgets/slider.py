from travertino.size import at_least

import toga
from toga_cocoa.libs import (
    SEL,
    NSEventType,
    NSSlider,
    objc_method,
    objc_property,
)

from .base import Widget


class TogaSlider(NSSlider):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onSlide_(self, sender) -> None:
        event_type = sender.window.currentEvent().type
        if event_type == NSEventType.LeftMouseDown:
            if self.interface.on_press:
                self.interface.on_press(self.interface)
        elif event_type == NSEventType.LeftMouseUp:
            if self.interface.on_release:
                self.interface.on_release(self.interface)

        if self.interface.on_change:
            self.interface.on_change(self.interface)


class Slider(Widget, toga.widgets.slider.SliderImpl):
    def create(self):
        self.native = TogaSlider.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.target = self.native
        self.native.action = SEL("onSlide:")

        self.add_constraints()

    def get_tick_count(self):
        return (
            self.native.numberOfTickMarks
            if self.native.allowsTickMarkValuesOnly
            else None
        )

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self.native.allowsTickMarkValuesOnly = False
            self.native.numberOfTickMarks = 0
        else:
            self.native.allowsTickMarkValuesOnly = True
            self.native.numberOfTickMarks = tick_count

    def get_value(self):
        return self.native.doubleValue

    def set_value(self, value):
        self.native.doubleValue = value

    def get_range(self):
        return (self.native.minValue, self.native.maxValue)

    def set_range(self, range):
        self.native.minValue = range[0]
        self.native.maxValue = range[1]

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
