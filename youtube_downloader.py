"""  tkinter """
import re
from string import punctuation, whitespace
import tkinter as tk
import tkinter.filedialog as tk_filedialog
from pytube import YouTube

def is_youtube_url(text_line :str) -> bool:
    """ check if text_line is an url and contains 'youtu' """
    def is_correct_url(text_line :str) -> bool:
        """ check if text_line is an url """
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, text_line) is not None
    return is_correct_url(text_line) and ('youtu.' in text_line or 'youtube.' in text_line)

def file_name_normalize(file_name: str) -> str:
    """ remove all chars except letters and digits """
    inadmissible_chars = punctuation + whitespace
    table = str.maketrans(inadmissible_chars, '_' * len(inadmissible_chars))
    file_name = file_name.translate(table)
    return file_name

class LinkDialog(tk.Tk):
    """ Main Dialog """
    def __init__(self) -> None:
        super().__init__()
        self.title('Youtube Downloader')
        self._width = 600
        self._height = 120
        self.geometry(f'{self._width}x{self._height}+100+100')

        self.default_link = 'https://youtu.be/Hu8bkennWUk' #'https://youtu.be/nLYroLhY3Jg'
        self.link = self.default_link

        self.canvas = tk.Canvas(master=self, bg="green", width=self._width, height=self._height)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.add_status_line()
        self.add_input_link_dialog()

    def add_status_line(self):
        """" add status line """
        x_pos = self._width // 2
        y_pos = 90
        self.status_line = self.canvas.create_text(x_pos, y_pos,
                                                   text='input youtube link in the field above',
                                                   fill='white')

    def add_input_link_dialog(self):
        """ get address of video """

        def update_link():
            nonlocal self
            link = self.link_field.get()
            if is_youtube_url(link):
                self.link_field.configure(foreground='green')
                self.link = link
                video = YouTube(self.link)
                highest_video_stream = video.streams.get_highest_resolution()
                file_extension = getattr(highest_video_stream, 'subtype', 'mp4')
                self.canvas.itemconfig(self.status_line, text='Choose name and destination for videofile')
                file_name = self.save_file('video_' +
                                           file_name_normalize(video.title) +
                                           '.' +
                                           file_extension)
                self.canvas.itemconfig(self.status_line, text='Please wait, video is dowloading.....')
                path_to_saved_video = highest_video_stream.download(filename=file_name)
                self.canvas.itemconfig(self.status_line, text='video is saved to: ' + path_to_saved_video)
                self.link_field.configure(foreground='black')
            else:
                self.link_field.configure(foreground='red')
                self.link = None

        x_pos = self._width // 2
        y_pos = 50
        self.frame = tk.Frame(master=self.canvas, borderwidth=1)
        self.canvas.create_window(x_pos, y_pos, window=self.frame)

        self.link_label = tk.Label(master=self.frame, text='Link:')
        self.link_label.grid(column=0, row=0)

        # check = (self.register(self.check_url), "%P")
        self.link_field = tk.Entry(master=self.frame, width=30) # validatecommand=
        self.link_field.insert(0, self.default_link)
        self.link_field.grid(column=2, row=0)
        self.ok_btn = tk.Button(master=self.frame,
                                text='Download',
                                borderwidth=3,
                                command=update_link)
        self.ok_btn.grid(column=4, row=0)

    def save_file(self, default_name = 'video_file_name'):
        """ save file dialog """
        filename = tk_filedialog.asksaveasfilename(initialfile=default_name)
        return filename

def main():
    """ main function """
    dialog = LinkDialog()
    dialog.mainloop()


if __name__ == "__main__":
    import sys
    import os
    os.system('cls')
    print('-----------------------------------------------------------')
    main()


    sys.exit()