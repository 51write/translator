from .page import Page

class File:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)