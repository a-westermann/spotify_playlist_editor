from tkinter import *
import api_calls
from tkinter import ttk
import webview
import sv_ttk
import threading
from redirect_handler import SpotifyRedirectHandler, start_local_server
from spotify_data import SpotifyData, Song


class Gui:
    def __init__(self):
        self.gui = Tk()
        self.gui.title('Spotify Liked Songs Editor')
        self.spotify_data = SpotifyData()
        self.auth_window = None
        self.user_access_token = None
        width, height = 1000, 800
        self.gui.geometry(f'{width}x{height}')
        canvas = Canvas(self.gui, width='100', height='100')
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        canvas.pack()
        self.screen_objects = {}
        login_label = ttk.Label(self.gui, text='Log in to start', font='arial')
        login_label.pack()
        self.screen_objects['login_label'] = login_label
        login_button = ttk.Button(self.gui, text='Log in', command=self.request_auth)
        button_width = 230
        login_button.place(x=width/2 - button_width / 2, y=200, width=button_width, height=50)
        self.screen_objects['login_button'] = login_button
        sv_ttk.set_theme("dark")
        self.gui.mainloop()
        exit()

    def request_auth(self):
        auth_url = api_calls.user_login()
        self.auth_window = webview.create_window('Authorization', auth_url)
        threading.Thread(target=self.wait_for_auth).start()
        webview.start()

    def wait_for_auth(self):
        auth_code, error = start_local_server()
        self.auth_window.destroy()
        self.screen_objects['login_label'].destroy()
        self.screen_objects['login_button'].destroy()
        if auth_code:
            self.user_access_token = api_calls.get_token(auth_code)
            self.playlist_editor_screen()
        else:
            label = ttk.Label(self.gui, text='Fail', font='arial')
            label.pack()


    def playlist_editor_screen(self):
        label = ttk.Label(self.gui, text='Hold on a sec... compiling your data. This may take a few minutes',
                          font='arial')
        label.pack()
        self.spotify_data.compile_data(self.user_access_token)
        label.destroy()
        columns = 'Artist', 'Name', 'ID', 'Delete'
        tree = ttk.Treeview(self.gui, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=50 if col == 'Delete' else 100, anchor='left')

        self.checkbox_states = {}

        for i, song in enumerate(self.spotify_data.get_songs_to_drop(0.1)):
            checkbox_var = BooleanVar(value=False)
            self.checkbox_states[song.id] = checkbox_var
            tree.insert('', 'end', values=('', song.artist, song.name, song.id))
            checkbox = ttk.Checkbutton(self.gui, variable=checkbox_var)
            tree_window = tree.bbox(i, column=0)
            tree.create_window(tree_window[0], tree_window[1], window=checkbox)

        scrollbar = ttk.Scrollbar(self.gui, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(expand=True, fill='both')
