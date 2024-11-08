

class User:
    def __init__(self, first_name, last_name, username, password, email, birthday, is_active, figures):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.birthday = birthday
        self.is_active = is_active
        self.figures = figures



class Figure:
    def __init__(self, base, y_series, yy_series):
        self.base = base
        self.y_series = y_series
        self.yy_series = yy_series


class Base:
    def __init__(self, background, title_on, y_on, yy_on, x_on, title, label, x_range):
        self.background = background
        self.title_on = title_on
        self.y_on = y_on
        self.yy_on = yy_on
        self.x_on = x_on
        self.title = title
        self.label = label
        self.x_range = x_range


class Series:
    def __init__(self, show_data, show_ticks, show_label, show_tick_labels, show_ls, dashed, label, data_color, ls_color, range, data):
        self.show_data = show_data
        self.show_ticks = show_ticks
        self.show_label = show_label
        self.show_tick_labels = show_tick_labels
        self.show_ls = show_ls
        self.dashed = dashed
        self.label = label
        self.data_color = data_color
        self.ls_color = ls_color
        self.range = range
        self.data = data


class Data:
    def __init__(self, date, value):
        self.date = date
        self.value = value