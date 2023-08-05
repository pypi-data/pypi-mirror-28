#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import pyglet
import os

from swine import FPS_LIMIT


class Window(pyglet.window.Window):
    def __init__(self, resizable=False, vsync=False, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT):
        # type: (str) -> None
        pyglet.window.Window.__init__(self, resizable=resizable, vsync=vsync, style=style)
        self._resizeable = resizable
        self._vsync = vsync
        self._style = style

        self._title = ""
        self._icon = None
        self._fullscreen = False
        self._min_size = (0, 0)
        self._max_size = (0, 0)

        self._keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self._keys)

        self._loop = True
        
        self.scene_list = []
        self.active_scene = 0

        pyglet.clock.set_fps_limit(FPS_LIMIT)

        self.icon(pyglet.image.load(os.path.join(os.path.dirname(__file__), "swine.png")))

    def title(self, title):
        # type: (str) -> str
        """
        Set and return the title of the window.

        :param title:
        :return:
        """
        self._title = title
        self.set_caption(title)

        return self._title

    def icon(self, image):
        # type: (pyglet.image.AbstractImage) -> str
        """
        Sets and returns the icon of the window.

        :param image:
        :return:
        """
        self._icon = image
        self.set_icon(image)

        return self._icon

    def fullscreen(self, fullscreen):
        # type: (bool) -> bool
        """
        Set and return if the window is fullscreen.

        :param fullscreen:
        :return:
        """
        self._fullscreen = fullscreen
        self.set_fullscreen(fullscreen)

        return self._fullscreen

    def min_size(self, width, height):
        # type: (int, int) -> tuple[int, int]
        """
        Set and return the minimum size of the window.

        :param width:
        :param height:
        :return:
        """
        self._min_size = (width, height)
        self.set_minimum_size(width, height)

        return self._min_size

    def max_size(self, width, height):
        # type: (int, int) -> tuple[int, int]
        """
        Set and return the maximum size of the window.

        :param width:
        :param height:
        :return:
        """
        self._max_size = (width, height)
        self.set_maximum_size(width, height)

        return self._max_size

    def size(self, width, height):
        # type: (int, int) -> tuple[int, int]
        """
        Set and return the size of the window.

        :param width:
        :param height:
        :return:
        """
        self.set_size(width, height)

        return self.get_size()

    def location(self, x, y):
        # type: (int, int) -> tuple[int, int]
        """
        Set and return the location of the window.

        :param x:
        :param y:
        :return:
        """
        self.set_location(x, y)

        return self.get_location()

    def mainloop(self):
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

        while self._loop:
            pyglet.clock.tick()

            for window in pyglet.app.windows:
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()
                
    def on_draw(self):
        self.clear()

        self.scene_list[self.active_scene].batch.draw()

    def on_key_press(self, symbol, modifiers):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_key_release(symbol, modifiers)

    def on_text(self, text):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_text(text)

    def on_text_motion(self, motion):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_text_motion(motion)

    def on_mouse_motion(self, x, y, dx, dy):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_enter(self, x, y):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_enter(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for item in self.scene_list[self.active_scene].object_list:
            item.on_mouse_scroll(x, y, scroll_x, scroll_y)
