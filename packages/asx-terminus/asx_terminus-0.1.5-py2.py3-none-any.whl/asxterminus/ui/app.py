import urwid

from asxterminus.config import config

from .portfolio import ShareTable
from .news import AnnouncementTable, GoogleFinanceNews


class TerminalApp(object):

    def __init__(self, config, portfolio):
        self.config = config
        self.portfolio = portfolio
        self.quote_table = ShareTable(
            portfolio=portfolio
        )
        self.announcements_table = AnnouncementTable(portfolio=self.portfolio)
        self.rss_table = GoogleFinanceNews(portfolio=self.portfolio)
        self.main_loop = urwid.MainLoop(
            self.get_layout(),
            self.palette,
            unhandled_input=self.handle_input
        )

    def run(self):
        self.main_loop.run()

    def exit(self):
        raise urwid.ExitMainLoop()

    @property
    def palette(self):
        return [
            ('titlebar', 'dark blue,bold', ''),
            ('refresh', 'dark green,bold', ''),
            ('quit', 'dark red,bold', ''),
            ('headers', 'dark blue,bold', ''),
            ('cell', 'white', ''),
            ('gain', 'dark green,bold', ''),
            ('loss', 'dark red,bold', '')
        ]

    def handle_input(self, key):
        if key == 'R' or key == 'r':
            self.refresh(None, None)

        if key == 'Q' or key == 'q':
            self.exit()

    def refresh(self, a, b):
        self.quote_table.refresh()
        self.announcements_table.refresh()
        self.rss_table.refresh()

        self.main_loop.draw_screen()
        self.quote_box.base_widget.set_text(
            self.quote_table.render()
        )
        self.news_box.base_widget.set_text(
            self.announcements_table.render()
        )
        self.rss_box.base_widget.set_text(
            self.rss_table.render()
        )
        self.main_loop.set_alarm_in(
            int(self.config.refresh_interval), self.refresh
        )

    def get_header(self):
        header_text = urwid.Text(
            '\n%s\n' % self.config.title_bar
        )
        header = urwid.AttrMap(header_text, 'titlebar')
        return header

    def get_quote_table(self):
        quote_text = urwid.Text(self.quote_table.render())
        self.quote_box = urwid.Padding(quote_text, left=2, right=0)
        return self.quote_box

    def get_announcements_table(self):
        text = urwid.Text(self.announcements_table.render())
        self.news_box = urwid.Padding(text, left=2, right=0)
        return self.news_box

    def get_rss_table(self):
        text = urwid.Text(self.rss_table.render())
        self.rss_box = urwid.Padding(text, left=2, right=0)
        return self.rss_box

    def get_body(self):
        divider = urwid.Divider(
            div_char=self.config.divider_char, top=1, bottom=1
        )
        quote_table = self.get_quote_table()
        announcements_table = self.get_announcements_table()
        rss_table = self.get_rss_table()
        lw = urwid.SimpleFocusListWalker([
            quote_table, divider,
            announcements_table, divider,
            rss_table
        ])
        return urwid.ListBox(lw)

    def get_footer(self):
        menu = urwid.Text([
            'Press (', ('refresh', 'R'), ') to manually refresh. ',
            'Press (', ('quit', 'Q'), ') to quit.'
        ])
        return menu

    def get_layout(self):
        return urwid.Frame(
            header=self.get_header(),
            body=self.get_body(),
            footer=self.get_footer()
        )
