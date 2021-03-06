#!/usr/bin/env python

import threading
import thread

import pygtk
pygtk.require('2.0')
import gtk
import gobject
gobject.threads_init()

import gzip
import os
import re
import shutil
import subprocess
import sys
import urllib
from urllib import FancyURLopener
from datetime import datetime
from datetime import time
from datetime import timedelta
import ConfigParser
from StringIO import StringIO
from time import sleep

class Bijin:
    version = '1.1.0.dev'
    source_urls = {
        0: {
            'title': 'ClockM - small',
            'url': 'http://www.clockm.com/tw/widget/img/clk/hour/%H%M.jpg',
            'http-referer': 'https://github.com/adhisimon/bijinclock/wiki',
        },
        1: {
            'title': 'ClockM - Big',
            'url': 'http://www.clockm.com/tw/img/clk/hour/%H%M.jpg',
            'http-referer': 'https://github.com/adhisimon/bijinclock/wiki',
        },
        2: {
            'title': 'Arthur',
            'url': 'http://www.arthur.com.tw/photo/images/400/%H%M.JPG',
            'http-referer': 'https://github.com/adhisimon/bijinclock/wiki',
        },
        3: {
            'title': 'Bijin Tokei - Japan - Small',
            'url': 'http://www.bijint.com/assets/pict/bijin/240x320/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/jp/',
        },
        4: {
            'title': 'Bijin Tokei - Japan - Big',
            'url': 'http://bijint.com/jp/tokei_images/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/jp/',
        },
        5: {
            'title': 'Bijin Tokei - Korea',
            'url': 'http://www.bijint.com/assets/pict/kr/240x320/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/kr/',
        },
        6: {
            'title': 'Bijin Tokei - Hong Kong',
            'url': 'http://www.bijint.com/assets/pict/hk/240x320/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/hk/',
        },
        7: {
            'title': 'Gal Tokei',
            'url': 'http://gal.bijint.com/assets/pict/gal/240x320/%H%M.jpg',
            'http-referer': 'http://gal.bijint.com/',
        },
        8: {
            'title': 'Circuit Tokei',
            'url': 'http://www.bijint.com/assets/pict/cc/590x450/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/cc/',
        },
        9: {
            'title': 'Binan Tokei',
            'url': 'http://www.bijint.com/assets/pict/jp/240x320/%H%M.jpg',
            'http-referer': 'http://www.bijint.com/binan/',
        },
        10: {
            'title': 'Lovely Time II',
            'url': 'http://gameflier.lovelytime.com.tw/photo/%H%M.JPG',
            'http-referer': 'https://github.com/adhisimon/bijinclock/wiki',
        },
    }

    source_selected = 0
    last_source_selected = source_selected
    cache_dir = os.path.expanduser("~/.bijinclock/caches")
    config_file = os.path.expanduser("~/.bijinclock/bijinclock.ini")
    config = None

    is_always_on_top = False
    is_fetch_next = True
    is_fullscreen = False
    window = None
    clock_image = None
    is_exit = False
    last_time = None
    popup = None
    message_label = None
    latest_version_label = None

    def __init__(self):
        if os.name == 'nt':
            gtk.rc_parse("gtkrc")

        self.init_cache_dir()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_title('loading...')
        self.window.set_resizable(False)

        self.init_icon()
        self.init_config()
        self.init_menu()

        vbox = gtk.VBox()
        self.window.add(vbox)

        event_box = gtk.EventBox()
        event_box.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        vbox.add(event_box)

        self.message_label = gtk.Label('  please wait while loading...  ')
        vbox.pack_start(self.message_label, False, False, 0)

        self.clock_image = gtk.Image()
        event_box.add(self.clock_image)

        self.window.show_all()

        event_box.connect("button-press-event", self.on_button_press_event)
        self.window.connect("delete_event", self.on_main_delete)
        self.window.connect("destroy", self.on_main_destroy)

    def init_icon(self):
        if os.path.isfile("/usr/share/icons/bijinclock.png"):
            try:
                self.window.set_icon_from_file("/usr/share/icons/bijinclock.png")
            except:
                pass
        elif os.path.isfile("/usr/local/share/icons/bijinclock.png"):
            try:
                self.window.set_icon_from_file("/usr/share/icons/bijinclock.png")
            except:
                pass

    def init_config(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.config_file)

        try:
            self.config.add_section("Main")
        except:
            pass

        try:
            self.source_selected = self.config.getint("Main", "selected_source")
        except:
            pass

        try:
            self.is_always_on_top = self.config.getboolean("Main", "always_on_top")
            self.window.set_keep_above(self.is_always_on_top)
        except:
            pass

    def init_menu(self):
        ui_source_selector = """<ui><popup name="Popup">"""

        for source_id in self.source_urls:
            ui_source_selector += """<menuitem name="source%s" action="source%s" />""" % (source_id, source_id)

        ui_source_selector += """</popup></ui>"""

        ui = """<ui>
            <popup name="Popup">
                <separator />
                <menuitem name="AlwaysOnTop" action="AlwaysOnTop" />
                <menuitem name="Fullscreen" action="Fullscreen" />
                <separator />
                <menuitem name="About" action="About" />
                <menuitem name="Homepage" action="Homepage" />
                <separator />
                <menuitem name="Quit" action="Quit" />
            </popup>
        </ui>"""

        self.ui_manager = gtk.UIManager()
        accel_group = self.ui_manager.get_accel_group()
        self.window.add_accel_group(accel_group)
        action_group = gtk.ActionGroup("Bijin Clock Action Group")
        action_group.add_actions(
            [
                ("Configure", None, "_Configure", None,
                    None, self.show_config_window
                ),
                ("About", None, "_About", None,
                    None, self.show_about_window
                ),
                ("Homepage", None, "Visit _Homepage", None,
                    None, self.open_homepage
                ),
                ("Quit", None, "_Quit", None,
                    None, lambda w: self.window.destroy()
                ),
            ]
        )
        action_group.add_toggle_actions(
            [
                (
                    # action name
                    'AlwaysOnTop',
                    # stock id
                    None,
                    # label
                    'Always on _top',
                    # accelerator
                    None,
                    # tooltip
                    None,
                    # callback
                    self.toggle_always_on_top,
                    # active flag
                    self.is_always_on_top
                ),
                (
                    # action name
                    'Fullscreen',
                    # stock id
                    None,
                    # label
                    '_Fullscreen',
                    # accelerator
                    None,
                    # tooltip
                    None,
                    # callback
                    self.on_toggle_fullscreen,
                    # active flag
                    self.is_fullscreen
                )
            ]
        )

        select_source_actions = []
        for source_id in self.source_urls:
             select_source_actions += [(
                "source%s" % source_id,
                None,
                self.source_urls[source_id]['title'],
                None,
                None,
                source_id
            )]

        action_group.add_radio_actions(select_source_actions, self.source_selected, self.on_select_source)

        self.ui_manager.insert_action_group(action_group, 0)
        self.ui_manager.add_ui_from_string(ui_source_selector)
        self.ui_manager.add_ui_from_string(ui)
        self.popup = self.ui_manager.get_widget("/Popup")

    def init_cache_dir(self):
        try:
            shutil.rmtree(self.cache_dir)
        except:
            pass

        os.makedirs(self.cache_dir)

    def main(self):
        interval_thread = IntervalThread(self)
        interval_thread.start()

        gtk.main()

    def on_button_press_event(self, widget, event):
        self.popup.popup(None, None, None, event.button, event.time)

    def on_toggle_fullscreen(self, action):
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.window.hide()
            self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
            self.window.set_resizable(True)
            self.window.show()
            self.window.fullscreen()
        else:
            self.window.hide()
            self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
            self.window.set_resizable(False)
            self.window.show()
            self.window.unfullscreen()

    def toggle_always_on_top(self, action):
        self.is_always_on_top = action.get_active()
        self.window.set_keep_above(action.get_active())
        self.config.set("Main", "always_on_top", str(action.get_active()))
        self.config_save()

    def config_save(self):
        with open(self.config_file, 'wb') as config_file:
            self.config.write(config_file)

    def on_select_source(self, current, data):
        self.source_selected = current.get_current_value()
        self.config.set("Main", "selected_source", str(self.source_selected))
        self.message_label.show()
        self.clock_image.hide()
        self.config_save()

    def show_about_window(self, data):

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        window.set_resizable(False)
        window.set_title('Bijin Clock')
        window.set_border_width(10)
        window.set_modal(True)
        window.set_property('skip-taskbar-hint', True)
        window.set_transient_for(self.window)
        window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#fff'))

        vbox = gtk.VBox()
        window.add(vbox)

        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textbuffer = textview.get_buffer()
        textbuffer.set_text(
"""Bijin Clock v%s
https://github.com/adhisimon/bijinclock/wiki
(c) gua@adhisimon.or.id 2011

Special thanks to:
* ClockM (http://www.clockm.com/)
* Arthur (http://www.arthur.com.tw/)
* Bijin Tokei (http://bijint.com/)
* Lovely Time (http://lovelytime.com.tw/)
        """ % self.version
        )

        vbox.add(textview)

        self.latest_version_label = gtk.Label("Loading latest version information from the web...")
        vbox.add(self.latest_version_label)

        fetch_latest_version_info = FetchLatestVersionInfo(self)
        fetch_latest_version_info.start()

        window.show_all()

    def open_homepage(self, data = None):
        try:
            os.startfile("https://github.com/adhisimon/bijinclock/wiki")
        except AttributeError:
            subprocess.call(['xdg-open', 'https://github.com/adhisimon/bijinclock/wiki'])

    def url_to_show(self, hour = None, minute = None):
        if not hour:
            time_to_show = datetime.now()
        else:
            time_to_show = time(hour = hour, minute = minute)

        return time_to_show.strftime(self.source_urls[self.source_selected]['url'])

    def url_to_show_next(self):
        now = datetime.now()
        next_minute = timedelta(minutes = 1) + now

        return self.url_to_show(next_minute.hour, next_minute.minute)

    def replace_image(self, filename):
        self.message_label.hide()
        self.clock_image.set_from_file(filename)
        self.last_source_selected = self.source_selected
        self.clock_image.show()
        os.remove(filename)

    def do_show(self):
        now = datetime.now()

        if (self.last_source_selected == self.source_selected) and self.last_time and (
            self.last_time.hour == now.hour
            and self.last_time.minute == now.minute
        ):
            return

        url = self.url_to_show()
        filename = self.do_fetch(url)
        if filename:
            self.last_time = now

            gobject.idle_add(self.window.set_title, 'Bijin Clock')
            gobject.idle_add(self.replace_image, filename)

            self.do_fetch_next()

    def sanitized_url(self, url):
        sanitized_url = re.sub(r'''\W''', '.', url)
        return sanitized_url

    def do_fetch(self, url):
        sanitized_url = self.sanitized_url(url)
        cache_file = self.cache_dir + '/' + sanitized_url

        if not os.path.exists(cache_file):
            #print datetime.now(), 'downloading %s' % url

            referer = self.source_urls[self.source_selected]['http-referer']
            myurlopener = MyUrlOpener()
            myurlopener.set_referer(referer)

            try:
                myurlopener.retrieve(url, cache_file)
            except:
                print "Error downloading %s" % url
                return False

            #print datetime.now(), '%s has been downloaded' % url

        return cache_file

    def do_fetch_next(self):
        url= self.url_to_show_next()
        self.do_fetch(url)

    def show_config_window(self, data = None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        window.set_resizable(False)
        window.set_title('Bijin Clock Configuration')
        window.set_border_width(10)
        window.set_modal(True)
        window.set_property('skip-taskbar-hint', True)
        window.set_transient_for(self.window)
        window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        vbox = gtk.VBox(False, 5)
        window.add(vbox)

        label = gtk.Label("Not implemented yet")
        vbox.add(label)

        window.show_all()

    def on_main_delete(self, widget, event, data = None):
        return False

    def on_main_destroy(self, widget, data = None):
        gtk.main_quit()
        print "Terminating..."
        self.is_exit = True

class IntervalThread(threading.Thread):
    caller = None

    def __init__(self, caller):
        super(IntervalThread, self).__init__()
        self.caller = caller

    def run(self):
        caller = self.caller

        while not caller.is_exit:
            caller.do_show()

            now = datetime.now()
            next_minute = timedelta(minutes = 1) + now
            next_minute = next_minute.replace(second = 0, microsecond = 0)
            sleep_time = next_minute - now

            sleep(min(2, sleep_time.seconds + 1))

class FetchLatestVersionInfo(threading.Thread):
    caller = None

    def __init__(self, caller):
        super(FetchLatestVersionInfo, self).__init__()
        self.caller = caller

    def run(self):
        caller = self.caller

        try:
            response = urllib.urlopen("http://adhisimon.github.com/bijinclock/LATEST_VERSION.txt")
        except:
            print 'failed to get information about latest version on the web'
            return

        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj = buf)
            response_text = f.read()
        else:
            response_text = response.read()

        m = re.search(r"===LATEST_VERSION=(.*)===", response_text)
        if m:
            latest_version = m.group(1)
            gobject.idle_add(
                caller.latest_version_label.set_text,
                "Your version is: %s, latest stable version is: %s" % (caller.version, latest_version)
            )

class MyUrlOpener(FancyURLopener):
    version = 'BijinClock http://adhisimon.or.id/bijinclock'

    def set_referer(self, referer):
        self.addheader('Referer', referer)


if __name__ == '__main__':
    bijin = Bijin()
    bijin.main()
