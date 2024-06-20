import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self.page = page
        self.page.title = "Template application using MVC and DAO"
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.dd_anno = None
        self.btn_grafo = None
        self.dd_nazione = None
        self.btn_volumi = None
        self.btn_rappresentativi = None
        self.txt_lunghezza = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Hello World", color="blue", size=24)
        self.page.controls.append(self._title)

        self.dd_anno = ft.Dropdown(label="Anno")
        self.btn_grafo = ft.ElevatedButton(text="Crea grafo", on_click=self.controller.handle_crea_grafo)
        row1 = ft.Row([self.dd_anno, self.btn_grafo], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row1)

        self.dd_nazione = ft.Dropdown(label="Nazione")
        self.btn_volumi = ft.ElevatedButton(text="Calcola volumi",
                                            disabled=True,
                                            on_click=self.controller.handle_volumi)
        self.controller.fill_dds()
        row2 = ft.Row([self.dd_nazione, self.btn_volumi], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row2)

        self.btn_rappresentativi = ft.ElevatedButton(text="Retailer rappresentativi",
                                                     disabled=True,
                                                     on_click=self.controller.handle_percorso)
        self.txt_lunghezza = ft.TextField(label="Lunghezza percorso", disabled=True)
        row3 = ft.Row([self.txt_lunghezza, self.btn_rappresentativi], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.page.controls.append(self.txt_result)
        self.page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()
