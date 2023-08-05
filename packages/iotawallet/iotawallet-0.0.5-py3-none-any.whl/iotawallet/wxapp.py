import queue
import traceback
import threading

import wx
from iota.adapter import resolve_adapter
from iota.commands.core import GetNodeInfoCommand

from .wallet import Wallet

DEFAULT_URI = 'https://iotanode.us:443'


class WalletWindow(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title='Iota Wallet',
            size=(1000, 600),
        )

        self.worker = WorkerThread()

        self.panel = wx.Panel(self)
        self.create_status_bar()
        self.add_login_ui()

    def add_login_ui(self):

        # TODO: Change this to an icon
        text = wx.StaticText(self.panel, label='Iota Wallet')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(text, flag=wx.CENTER)

        self.seed_input = wx.TextCtrl(self.panel)
        self.login_button = wx.Button(self.panel, label='Login')
        login_vbox = wx.BoxSizer(wx.VERTICAL)
        login_vbox.Add(self.seed_input, proportion=1, flag=wx.EXPAND)
        login_vbox.Add(self.login_button, proportion=1, flag=wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=2, flag=(wx.CENTER | wx.ALL), border=20)
        vbox.Add(login_vbox, proportion=1, flag=(wx.EXPAND | wx.ALL), border=20)

        self.panel.SetSizer(vbox)
        self.panel.Layout()

        self.Bind(wx.EVT_BUTTON, self.on_login_clicked, self.login_button)

    def create_status_bar(self):
        self.status_bar = self.CreateStatusBar()

        # Get the milestone status the first time then set up a timer to
        # periodically check it
        self._update_milestone()

        self._update_milestone_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._update_milestone, self._update_milestone_timer)
        self._update_milestone_timer.Start(3 * 1000)

    def _update_milestone(self, event=None):
        response = GetNodeInfoCommand(resolve_adapter(DEFAULT_URI))()
        current_milestone = response['latestSolidSubtangleMilestoneIndex']
        latest_milestone = response['latestMilestoneIndex']

        if current_milestone == latest_milestone:
            status = f'Synced: {current_milestone}'
        else:
            status = f'Unsynced: {current_milestone}/{latest_milestone}'

        self.status_bar.PushStatusText(status)

    def on_login_clicked(self, event):
        seed = self.seed_input.GetLineText(0)

        # Check seed
        error = ''
        if len(seed) != 81:
            error = 'Error: Seed must be 81 characters'
        else:
            valid_chars = '9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if not all(char in valid_chars for char in seed):
                error = 'Error: Seed must contain only A-Z or 9'

        if error:
            print(error)
            self.disable_login_button(error)
            wx.CallLater(3 * 1000, self.reenable_login_button)
        else:
            self.wallet = Wallet(
                uri=DEFAULT_URI,
                seed=seed,
            )

            self.worker.send(self.wallet.refresh_account, callback=self.after_account)
            self.disable_login_button('Logging in...')

    def disable_login_button(self, label):
        self.login_button.SetLabel(label)
        self.login_button.Disable()

    def reenable_login_button(self):
        self.login_button.Enable()
        self.login_button.SetLabel('Login')

    def after_account(self, result):
        self.transition_to_main_ui()

    def transition_to_main_ui(self):
        self.panel.DestroyChildren()
        self.create_main_ui()

    def create_main_ui(self):
        notebook = wx.Notebook(self.panel)

        overview_tab = OverviewTab(notebook, self.wallet)
        send_tab = SendTab(notebook, self.wallet)
        receive_tab = ReceiveTab(notebook, self.wallet)
        history_tab = HistoryTab(notebook, self.wallet)

        notebook.AddPage(overview_tab, 'Overview')
        notebook.AddPage(send_tab, 'Send')
        notebook.AddPage(receive_tab, 'Receive')
        notebook.AddPage(history_tab, 'History')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(notebook, flag=(wx.EXPAND | wx.ALL), proportion=1)

        self.panel.SetSizer(sizer)
        self.panel.Layout()


class OverviewTab(wx.Panel):
    def __init__(self, parent, wallet):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label=f'Balance: {wallet.balance}')
        sizer.Add(text, flag=wx.ALL)
        self.SetSizer(sizer)


class SendTab(wx.Panel):
    def __init__(self, parent, wallet):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label='Send')
        sizer.Add(text, flag=wx.ALL)
        self.SetSizer(sizer)


class ReceiveTab(wx.Panel):
    def __init__(self, parent, wallet):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label='Receive')
        sizer.Add(text, flag=wx.ALL)
        self.SetSizer(sizer)


class HistoryTab(wx.Panel):
    def __init__(self, parent, wallet):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label='History')
        sizer.Add(text, flag=wx.ALL)
        self.SetSizer(sizer)


class WorkerThread:
    def __init__(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.queue = queue.Queue()
        self.thread.start()

    def _run(self):
        while True:
            command, args, callback = self.queue.get()
            try:
                result = command(*args)
                if callback:
                    wx.CallAfter(callback, result)
            except Exception as e:
                traceback.print_exc()

    def send(self, command, args=(), callback=None):
        self.queue.put((command, args, callback))


def main():
    app = wx.App()
    wallet = WalletWindow()
    wallet.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
