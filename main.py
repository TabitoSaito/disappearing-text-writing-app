import tkinter as tk
from PIL import Image, ImageTk

HEADER = ("Arial", 20)
STANDARD = ("Arial", 14)


class Page(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

    def show(self):
        self.lift()


class StartPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        header_label = tk.Label(self, text="Disappearing Text writing App", font=HEADER)
        header_label.grid(row=0, column=1)

        image = Image.open("vanished_img.png")
        resize_img = image.resize((400, 400))
        self.img = ImageTk.PhotoImage(resize_img)

        img_label = tk.Label(self, image=self.img)
        img_label.grid(row=1, column=1, pady=20, padx=20)

        self.start_button = tk.Button(self, text="Start", font=STANDARD)
        self.start_button.config(padx=20, pady=20)
        self.start_button.grid(row=2, column=0, sticky="s", pady=20, padx=20)

        self.exit_button = tk.Button(self, text="Exit", font=STANDARD)
        self.exit_button.config(padx=20, pady=20)
        self.exit_button.grid(row=2, column=3, sticky="s", pady=20, padx=20)


class WritePage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.root = root
        self.id_1 = None
        self.id_2 = None
        self.id_5 = None
        self.id_delete = None
        self.id_reset_label = None

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        header_label = tk.Label(self, text="Start to write your story.", font=HEADER)
        header_label.grid(row=0, column=1, sticky="wne")

        self.text_input = tk.Text(self)
        self.text_input.grid(row=1, column=1)

        self.timer_label = tk.Label(self, text="", font=HEADER)
        self.timer_label.grid(row=2, column=1)

        self.startpage_button = tk.Button(self, text="Back to Startpage", font=STANDARD)
        self.startpage_button.config(padx=20, pady=20)
        self.startpage_button.grid(row=3, column=1, sticky="ws", pady=20, padx=20)

    def start_hotpotato(self):
        self.show()
        self.text_input.bind("<Key>", self.reset_timer)

    def end_hotpotato(self):
        self.text_input.unbind("<Key>")

    def start_timer(self):
        self.id_5 = self.after(5000, self.timer)

    def timer(self):
        self.timer_label.config(text="3")
        self.id_2 = self.after(1000, lambda: self.timer_label.config(text=2))
        self.id_1 = self.after(2000, lambda: self.timer_label.config(text=1))
        self.id_delete = self.after(3000, lambda: self.text_input.delete("1.0", tk.END))
        self.id_reset_label = self.after(3000, lambda: self.timer_label.config(text=""))

    def cancel_timer(self):
        try:
            try:
                self.after_cancel(self.id_5)
            except AttributeError:
                pass
            try:
                self.after_cancel(self.id_2)
            except AttributeError:
                pass
            try:
                self.after_cancel(self.id_1)
            except AttributeError:
                pass
            try:
                self.after_cancel(self.id_delete)
                self.after(self.id_reset_label)
            except AttributeError:
                pass
            self.timer_label.config(text="")
        except ValueError:
            pass

    def reset_timer(self, *args):
        self.cancel_timer()
        self.start_timer()


class PageController(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        p1 = StartPage(self)
        p2 = WritePage(self)

        p1.start_button.config(command=p2.start_hotpotato)
        p1.exit_button.config(command=root.destroy)

        def show_p1():
            p1.show()
            p2.end_hotpotato()

        p2.startpage_button.config(command=show_p1)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p1.show()


def main():
    root = tk.Tk()
    root.title("Disappearing Text writing App")
    controller = PageController(root)
    controller.pack(side="top", fill="both", expand=True)
    root.wm_geometry("700x700")
    root.mainloop()


if __name__ == "__main__":
    main()
