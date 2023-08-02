"""  tkinter """
import tkinter as tk

class Person:
    """ person info """
    def __repr__(self) -> str:
        return str(vars(self))

# def class_decorator(parameter = None):
#     """ add some modification to class """
#     def decorator(cls):
#         orig_init = cls.__init__
#         def new_init(self,  *args, **kwargs):
#             orig_init(self, *args, **kwargs)
#             print('run modified init')
#             print(f'decorator with {parameter = }')
#             self.title('Modified Dialog')
#         cls.__init__ = new_init
#         return cls
#     return decorator

def input_field(column, row,
                attr_name='name',
                prompt_text='Your name:',
                default_value='Guido van Rossum'):
    """ decorator function which adds input field to tkinter widget """
    def decorator(cls):
        orig_init = cls.__init__
        def new_init(self,  *args, **kwargs):
            orig_init(self, *args, **kwargs)
            self.title('input_field is added')
            self.name_label = tk.Label(master=self, text=prompt_text)
            self.name_label.grid(column=column, row=row)
            self.name_field = tk.Entry(master=self)
            self.name_field.insert(0, default_value)
            self.name_field.grid(column=column+1, row=row)
            self.person_info_methods[attr_name] = self.name_field.get
        cls.__init__ = new_init
        return cls
    return decorator

def btn_close(cls):
    """ decorator function which adds CLOSE button to tkinter widget class """
    orig_init = cls.__init__
    def new_init(self,  *args, **kwargs):
        orig_init(self, *args, **kwargs)
        self.title('close button is added')
        self.quit_btn = tk.Button(master=self, text='Quit', command=self.close)
        self.quit_btn.grid(column=1, row=300)
    cls.__init__ = new_init
    return cls

def btn_submit(cls):
    """ decorator function which adds submit button to tkinter widget class """
    def submit(self):
        """ submit function """
        person = Person()
        for method_name, method in self.person_info_methods.items():
            # print(method_name, method())
            attribute_name = method_name
            attribute_value = method()
            setattr(person, attribute_name, attribute_value)
            # person.method_name = method()
        print(person)
        self.close()
    cls.submit = submit
    orig_init = cls.__init__

    def new_init(self,  *args, **kwargs):
        orig_init(self, *args, **kwargs)
        self.title('submit button is added')
        self.quit_btn = tk.Button(master=self, text='Submit', command=self.submit)
        self.quit_btn.grid(column=0, row=300)
    cls.__init__ = new_init
    return cls

def radio_buttons(column, row, attr_name='gender', items=('male', 'female')):
    """ decorator function which adds radio buttons to tkinter widget """
    def decorator(cls):
        orig_init = cls.__init__

        def new_init(self,  *args, **kwargs):
            orig_init(self, *args, **kwargs)

            self.title('state radio buttons are added')
            self.selected_button_id = tk.IntVar()

            for i, item in enumerate(items):
                self.button = tk.Radiobutton(master=self,
                                             text=item,
                                             value=i,
                                             variable=self.selected_button_id)
                self.button.grid(column=column, row=row+i)

            self.selected_button_id.set(0)
            # self.person_info_methods[attr_name] = self.get_selected_button
            self.person_info_methods[attr_name] = lambda: items[self.selected_button_id.get()]

        cls.__init__ = new_init
        return cls
    return decorator

def listbox_slider(column, row, attr_name='number', items=range(10)):
    """ decorator function which adds list with slider to tkinter widget """
    def decorator(cls):
        orig_init = cls.__init__

        def get_item(self, event=None):
            """Get current selection from listbox"""
            # print(self.listbox.get(0,'end'))
            selected_item_index = self.listbox.curselection()
            selected_item = self.listbox.get(selected_item_index)
            return selected_item
        
        cls.get_item = get_item

        def new_init(self,  *args, **kwargs):
            orig_init(self, *args, **kwargs)
            self.title('listbox_slider is added')

            self.listbox = tk.Listbox(master=self, height=4)

            for i, item in enumerate(items):
                self.listbox.insert(i, item)
            self.listbox.select_set(0)

            # self.listbox.bind("<<ListboxSelect>>", self.get_city)
            self.listbox.grid(column=column, row=row)

            self.scrollbar = tk.Scrollbar(master=self, orient='vertical')
            self.scrollbar.grid(column=column+1, row=row, sticky='ns')

            self.listbox.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.listbox.yview)

            self.person_info_methods[attr_name] = self.get_item

        cls.__init__ = new_init
        return cls
    return decorator


@listbox_slider(1, 5, attr_name='city',
                items=('New York', 'London', 'Paris', 'Tokyo', 'Seul',
                       'Vienna', 'Zhovti Vody', 'Rio de Janeiro', 'Kyiv',
                       'Beijing', 'Havana', 'Buenos Aires', 'Toronto',))


# @radio_buttons(0, 2, attr_name='animal', items=('fox', 'rat', 'cat', 'dog', 'pigg', 'cow'))
# @input_field(0, 0, attr_name='field1', prompt_text='field1', default_value='value1')
# @input_field(0, 1, attr_name='field2', prompt_text='field2', default_value='value2')
# @input_field(0, 2, attr_name='field3', prompt_text='field3', default_value='value3')
@btn_submit
@btn_close
# @class_decorator('Some parameter')
class BaseDialog(tk.Tk):
    """ dialog class """
    def __init__(self, title='Base Dialog', geometry_settings=None) -> None:
        super().__init__()
        self.title(title)
        self.initial_geometry_settings = geometry_settings
        self.set_geometry()
        self.person_info_methods = {} # set of methods which get info from dialog
        # self.mainloop()

    def set_geometry(self):
        """ set dialog position on screen """
        if self.initial_geometry_settings is None:
            width, _ = self.get_screen_resolution()
            x_position = width // 2
            self.geometry(f'500x600+{x_position}+100')
        else:
            self.geometry(self.initial_geometry_settings)

    @staticmethod
    def get_screen_resolution():
        """ return screen resolution """
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        root.quit()
        return width, height

    def close(self):
        """ close tkinter widget """
        self.quit()
        self.destroy()
        # self.quit()


def main():
    """ main function """
    dialog = BaseDialog('Empty Dialog')
    dialog.mainloop()


if __name__ == "__main__":
    import sys
    import os
    os.system('cls')
    print('-----------------------------------------------------------')
    main()
    sys.exit()

# def decorator_factory(argument):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             funny_stuff()
#             something_with_argument(argument)
#             result = function(*args, **kwargs)
#             more_funny_stuff()
#             return result
#         return wrapper
#     return decorator