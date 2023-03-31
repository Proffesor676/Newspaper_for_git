# Создаём логгер
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

# функция отправки письма с логами ERRORS и выше
def send_email_for_errors_and_above(record):
    if record.levelno >= logging.ERROR and record.name in ['django.request', 'django.server']:
        send_logs_email()

# создаём консоль хэндлер
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# создаём фильтр и добавляем его в хэндлер
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# создаём файл с сообщениями general
file_handler = logging.FileHandler('general.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# создаём консоль хэндлер
if DEBUG == True:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
else:
    # создаём хэндлер с сообщениями логов INFO и выше
    file_handler = logging.FileHandler('general.log')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    # добавляем функцию отправки письма
    logger.addFilter(send_email_for_errors_and_above)

# создаём файл errors
error_handler = logging.FileHandler('errors.log')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s\n%(exc_info)s')
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

# создаём файл security
security_handler = logging.FileHandler('security.log')
security_handler.setLevel(logging.DEBUG)
security_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
security_handler.setFormatter(security_formatter)
security_handler.addFilter(logging.Filter('django.security'))
logger.addHandler(security_handler)


# создаём функцию для отправки сообщений
def send_logs_email():
    # устанавливаем параметры письма
    sender_email = 'sender@example.com'
    receiver_email = 'receiver@example.com'
    subject = 'Django Logs'

    # создаём объект сообщения
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Текст сообщения
    body = 'Сообщения из Djngo логи'
    message.attach(MIMEText(body, 'plain'))

    # прикрепляем лог файлы к сообщению
    for filename in ['errors.log', 'django.request.log', 'django.server.log']:
        with open(filename, 'rb') as file:
            attachment = MIMEApplication(file.read(), _subtype='txt')
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(attachment)

    # отправка сообщения
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, 'password')
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        logger.info('Email sent with logs.')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

# добавляем функцию в логгер как фильтр
logger.addFilter(send_email_for_errors_and_above)