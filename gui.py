from tkinter import ttk as ttk
import tkinter as tk
from watchlist_comparer import WatchlistComparer
from webull_helper import WebullHelper
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread


class GUI:

    wb = None
    watchlist_comp = None
    current_chart = None
    setting_chart = False
    root = None
    login_frame = None
    tab_root = None
    compare_tab = None
    algo_trader_tab = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Webull Toolkit')
        self.root.geometry('800x600')
        self.root.configure(background='white')
        self.create_login_screen()
        self.root.mainloop()

    # Creates the main watchlist comparer gui.
    def create_gui(self):

        self.watchlist_comp = WatchlistComparer(self.wb)

        style = ttk.Style()
        style.configure("tabs.TFrame", foreground="white", background="white")

        # Set up tabs
        self.tab_root = ttk.Notebook(self.root)
        self.compare_tab = ttk.Frame(self.tab_root, style='tabs.TFrame')
        self.algo_trader_tab = ttk.Frame(self.tab_root, style='tabs.TFrame')

        self.tab_root.add(self.compare_tab, text='Watchlist Comparer')
        self.tab_root.add(self.algo_trader_tab, text='Algo Trader')
        self.tab_root.pack(expand=1, fill="both")

        watchlists = self.watchlist_comp.get_watchlists()
        var = tk.StringVar(self.compare_tab)
        var.set(watchlists[0])
        options = tk.OptionMenu(self.compare_tab, var, *watchlists)
        options.pack()

        button = tk.Button(self.compare_tab, text="OK", command=lambda: self.replace_chart(var.get().__str__()))
        button.pack()

        self.add_chart(watchlists[0])

    # Creates the login screen and doesnt change until login is successful.
    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.configure(background='white')
        tk.Label(self.login_frame, text='Username: ').pack()
        username = tk.Entry(self.login_frame)
        username.pack()
        tk.Label(self.login_frame, text='Password: ').pack()
        password = tk.Entry(self.login_frame)
        password.pack()
        tk.Label(self.login_frame, text='Multi-factor authentication (only enter if you haven\'t logged in here before.): ').pack()
        mfa = tk.Entry(self.login_frame)
        mfa.pack()
        tk.Label(self.login_frame,
                 text='Get Multi-factor authentication code (If you click this, you must enter the new code upon login.): ').pack()
        tk.Label(self.login_frame,
                 text='MFA username: ').pack()
        mfa_username = tk.Entry(self.login_frame)
        mfa_username.pack()
        wbh = WebullHelper()
        tk.Button(self.login_frame, text='Get Multi-factor authentication', command=lambda: wbh.get_new_mfa(str(mfa_username.get()))).pack()

        tk.Button(self.login_frame, text='Login', command=lambda: self.attempt_login(str(username.get()), str(password.get()), str(mfa.get()))).pack()

        self.login_frame.pack()

    def attempt_login(self, username, password, mfa):
        wbh = WebullHelper()
        success = wbh.login(username, password, mfa)

        if success:
            self.wb = wbh.get_webull_object()
            self.login_frame.pack_forget()
            self.create_gui()

    def add_chart(self, watchlist_name):
        fig = self.watchlist_comp.get_tkinter_chart_figure(watchlist_name)
        if self.current_chart is not None:
            self.current_chart.get_tk_widget().pack_forget()
        self.current_chart = FigureCanvasTkAgg(fig, self.compare_tab)
        self.current_chart.get_tk_widget().pack()

    def replace_chart(self, watchlist_name):
        if not self.setting_chart:
            self.setting_chart = True
            Thread(target=self.replace_chart_thread_func, kwargs=dict(watchlist_name=watchlist_name)).start()

    def replace_chart_thread_func(self, watchlist_name):
        self.add_chart(watchlist_name)
        self.setting_chart = False
