# -------------------------
# Текст форм аутентификации
# -------------------------

LOGIN_FORM_PLACEHOLDER = "Логин ВК (номер телефона или email)"
PWD_FORM_PLACEHOLDER = "Пароль ВК"
LOGIN_BUTTON_TEXT = "Войти"
SAVE_USER_DATA_BUTTON_TEXT = "Сохранить и продолжить"

# -------------------------
# Текст ошибок валидации логина/пароля при аутентификации
# -------------------------

DATA_NOT_SPECIFIED_ERROR_MESSAGE = "Ошибка: не введен логин или пароль. Пожайлуста, попробуйте снова."
INCORRECT_EMAIL_ERROR_MESSAGE = "Email введен некорректно. Пожайлуста, попробуйте снова."
INCORRECT_PHONE_NUMBER_ERROR_MESSAGE = "Номер телефона введен некорректно. Пожайлуста, попробуйте снова."

# -------------------------------------------------------------------------------------
# Сообщения, появляющиеся при загрузке данных об аудиозаписях из ВК
# -------------------------------------------------------------------------------------

SONGS_FOUND_TEXT = "Треков найдено:"
NO_TRACKS_MESSAGE = (
    "Не найдено сохраненных треков.\nПеред скачиванием нажмите на кнопку \"Найти треки из ВК\",\n"
    "чтобы сохранить данные о треках для их скачивания."
)

GETTING_TRACKS_DATA_MESSAGE = "Собираю данные о треках из ВК..."
NO_INTERNET_CONNECTION_MESSAGE = (
    "Нет подключения к интернету. Чтобы продолжить,\nвосстановите соединение и попробуйте снова."
)
GENERAL_PARSER_ERROR_MESSAGE = (
    "Ошибка скачивания. Проверьте интернет-соединение.\n"
    "Если профиль закрыт, сделайте его видимым.\nТакже сделайте аудиозаписи видимыми\n"
    "для всех пользователей."
)
GENERAL_ERROR_MESSAGE = "При работе программы возникла ошибка:"
FIND_SUCCESS_MESSAGE = (
    "Треки получены успешно.\nЧтобы увидеть загруженные треки, нажмите\n\"Список найденных треков\" в главном меню."
)
DOWNLOAD_SUCCESS_MESSAGE = "Треки скачаны успешно."


# ---------------------------------------------
# Сообщения, появляющиеся при скачивании треков
# ---------------------------------------------

DOWNLOADING_TRACKS_MESSAGE = "Скачиваю треки..."
NO_CHOSEN_TRACKS_FOR_DOWNLOAD_MESSAGE = (
    "Вы не выбрали треки для скачивания.\nЧтобы скачать, необходимо вернуться\nи выбрать количество треков больше 0."
)
INCORRECT_TRACKS_VALUE_MESSAGE = "Неверное значение. Количество треков должно быть\nв диапазоне от 1 до"

# --------------------------
# Текст элементов интерфейса
# --------------------------

# 1) Главное меню

FIND_TRACKS_BUTTON_LABEL = "Найти треки из ВК"
SHOW_TRACKS_BUTTON_LABEL = "Список найденных треков"
DOWNLOAD_TRACKS_BUTTON_LABEL = "Скачать треки"

# 2) Меню скачивания

TRACKS_TO_DOWNLOAD_LABEL = "Количество:"
CURRENT_DOWNLOAD_FOLDER_LABEL = "Текущая папка для скачивания:"
CHANGE_DIR_BUTTON_LABEL = "Изменить"
DOWNLOAD_BUTTON_LABEL = "Применить и скачать"

# 3) Прочие элементы

BASE_BACK_BUTTON_TEXT = "Назад"
SPINBOX_ALL_BUTTON_TEXT = "Все"
