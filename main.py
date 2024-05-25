import flet as ft
from memegenerator import MemeGenerator

class MemeApp:
    def __init__(self):
        self.generator = MemeGenerator()

    def main(self, page: ft.Page):
        page.title = "МемоГенератор"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.AUTO

        self.image_path = ""
        self.path_display = ft.TextField(label='Путь к изображению', width=400, disabled=True)
        self.top_text_input = ft.TextField(label='Текст сверху', width=400)
        self.bottom_text_input = ft.TextField(label='Текст снизу', width=400)
        self.font_size_slider = ft.Slider(min=10, max=100, value=30, divisions=90, label="{value}", width=400)
        self.image_display = ft.Image(src="", width=400, height=400)

        select_image_button = ft.ElevatedButton(text='Выбрать изображение', on_click=self.on_select_image_click)
        preview_button = ft.ElevatedButton(text='Предварительный просмотр', on_click=self.on_preview_click)
        save_button = ft.ElevatedButton(text='Сохранить мем', on_click=self.on_save_click)

        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)

        page.overlay.append(self.file_picker)
        page.add(select_image_button, self.path_display, self.top_text_input, self.bottom_text_input, self.font_size_slider, preview_button, save_button, self.image_display)

    def on_select_image_click(self, e):
        self.file_picker.pick_files(allow_multiple=False)

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.image_path = e.files[0].path
            self.path_display.value = self.image_path
            e.page.update()

    def on_preview_click(self, e):
        if self.image_path:
            top_text = self.top_text_input.value
            bottom_text = self.bottom_text_input.value
            font_size = self.font_size_slider.value
            base64_data = self.generator.preview_image(self.image_path, top_text, bottom_text, font_size)
            if base64_data:
                self.image_display.src_base64 = base64_data
                e.page.update()
            else:
                print("Не удалось загрузить изображение для предварительного просмотра.")
        else:
            print("Путь к изображению не указан.")

    def on_save_click(self, e):
        if self.image_path:
            top_text = self.top_text_input.value
            bottom_text = self.bottom_text_input.value
            font_size = self.font_size_slider.value
            if top_text and bottom_text:
                filename = self.generator.create_meme(self.image_path, top_text, bottom_text, font_size)
                dialog = ft.AlertDialog(
                    title=ft.Text("Мем сохранен!"),
                    content=ft.Text(f"Мем сохранен как {filename}"),
                    actions=[
                        ft.TextButton("OK", on_click=self.close_dialog)
                    ]
                )
                e.page.dialog = dialog
                dialog.open = True
                e.page.update()
            else:
                print("Текст для мема не указан.")
        else:
            print("Путь к изображению не указан.")

    def close_dialog(self, e):
        e.page.dialog.open = False
        e.page.update()

if __name__ == "__main__":
    app = MemeApp()
    ft.app(target=app.main)