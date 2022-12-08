from APIs.TalpiotAPIs.Tasks.task import Task
from APIs.TalpiotAPIs.Tasks.dummy_task import DummyTask
from web_framework.server_side.infastructure.constants import *

import datetime

from APIs.TalpiotAPIs import User

from web_framework.server_side.infastructure.components.grid_panel import GridPanel
from web_framework.server_side.infastructure.components.stack_panel import StackPanel
from web_framework.server_side.infastructure.components.label import Label
from web_framework.server_side.infastructure.components.combo_box import ComboBox
from web_framework.server_side.infastructure.page import Page
from web_framework.server_side.infastructure.constants import *
from APIs.TalpiotAPIs.mahzors_utils import *


class GuardingHistory(Page):
    @staticmethod
    def get_title() -> str:
        return "הצגת היסטוריית שמירה"

    @staticmethod
    def is_authorized(user):
        return MATLAM in user.role  # Only the people of the base

    def __init__(self, params):
        super().__init__()
        self.sp = None

    def draw_table(self, user_to_view):

        tasks = []
        for t in Task.objects(assignment__contains=user_to_view):
            tasks.append({'time': t.start_time, 'text': t.task_type.description, 'points': t.task_type.points})

        for t in DummyTask.objects(users__contains=user_to_view):
            tasks.append({'time': t.date, 'text': t.description, 'points': t.points})

        tasks.sort(key=lambda t: t['time'] if t['time'] is datetime else datetime.combine(t['time'],
                                                                                          datetime.min.time()))

        table = GridPanel(len(tasks), 3)
        self.layout_table.add_component(table, 1, 0)

        for i, t in enumerate(tasks):
            time_str = get_hebrew_time(t['time'])
            table.add_component(Label(time_str, size=SIZE_MEDIUM), i, 0)
            table.add_component(Label(t['text'], size=SIZE_MEDIUM), i, 1)
            table.add_component(Label(t['points'], size=SIZE_MEDIUM), i, 2)
        
    def select_mahzor(self, mahzor):
        user_options = {str(u.id): str(u.name) for u in User.objects(mahzor=mahzor)}
        combo = ComboBox(user_options, lambda u_id: self.draw_table(User.objects(id=u_id)[0]))
        self.options_table.add_component(combo, 0, 1)

        # Clear table
        self.layout_table.add_component(Label(""), 1, 0)

    def get_page_ui(self, user):
        self.sp = StackPanel([])

        self.sp.add_component(Label("היסטוריית שמירה", size=SIZE_EXTRA_LARGE))


        options_layout = GridPanel(2, 1)
        self.sp.add_component(options_layout)

        self.options_headers = GridPanel(1, 2, bg_color=COLOR_PRIMARY_DARK)
        options_layout.add_component(self.options_headers, 0, 0)
        self.options_headers.add_component(Label("מחזור", fg_color='White'), 0, 0)
        self.options_headers.add_component(Label("משתמש", fg_color='White'), 0, 1)

        self.options_table = GridPanel(1, 2)
        options_layout.add_component(self.options_table, 1, 0)
        mahzor_options = {m.mahzor_num: m.short_name for m in get_mahzors()}
        self.options_table.add_component(ComboBox(mahzor_options, lambda s: self.select_mahzor(int(s)),
                                                  str(user.mahzor)), row=0, column=0)

        user_options = {str(u.id): str(u.name) for u in User.objects(mahzor=user.mahzor)}
        combo = ComboBox(user_options, lambda u_id: self.draw_table(User.objects(id=u_id)[0]), str(user.id))
        self.options_table.add_component(combo, 0, 1)

        self.layout_table = GridPanel(2, 1)
        self.sp.add_component(self.layout_table)

        headers = GridPanel(1, 3, bg_color=COLOR_PRIMARY_DARK)
        self.layout_table.add_component(headers, 0, 0)
        headers.add_component(Label("תאריך", fg_color='White', size=SIZE_LARGE), 0, 0)
        headers.add_component(Label("תיאור", fg_color='White', size=SIZE_LARGE), 0, 1)
        headers.add_component(Label("נקודות", fg_color='White', size=SIZE_LARGE), 0, 2)

        self.draw_table(User.objects(id=user.id)[0])
        return self.sp

