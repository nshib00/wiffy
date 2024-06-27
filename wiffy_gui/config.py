class AppSettings:
    width = 400
    height = 400

    base_font_type = "Arial"
    base_font_size = 20

    header_color = "#fc6514"
    text_color = "#c0c0c0"

    @property
    def base_font(self):
        return (self.base_font_type, self.base_font_size)

    @property
    def base_font_small(self):
        return (self.base_font_type, self.base_font_size - 4)

    @property
    def base_font_big(self):
        return (self.base_font_type, self.base_font_size + 15)

    @property
    def base_font_header(self):
        return (self.base_font_type, self.base_font_size + 40)


app_settings = AppSettings()
