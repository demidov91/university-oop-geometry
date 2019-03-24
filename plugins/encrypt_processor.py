import base64
import logging
import os
import tkinter as tk
from io import BytesIO

logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends.openssl.backend import backend as openssl_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    is_initialized = False
    logger.error('Missing cryptography package. Run `pip install cryptography` to install.')
else:
    is_initialized = True

from geometry.file_processor import FileProcessor
from geometry.gui.gui import GUI


def get_fernet(password: bytes, salt: bytes) -> 'Fernet':
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=openssl_backend
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password)))


class EncryptProcessor(FileProcessor):
    password_input = None
    dialog = None
    SALT_LENGTH = 16

    def __init__(self):
        super().__init__()
        if not is_initialized:
            raise Exception('Module was not initialized.')

    def write(self, data: bytes):
        password = self.password_input.get().encode()
        salt = os.urandom(self.SALT_LENGTH)

        data = get_fernet(password, salt).encrypt(data)

        return b'Salt' + bytes([self.SALT_LENGTH]) + salt + data

    def read(self, file: BytesIO) -> BytesIO:
        password = self.password_input.get().encode()
        prefix = file.read(4)
        if prefix != b'Salt':
            logger.warning('This is not an encrypted file.')
            file.seek(0)
            return file

        salt_length = file.read(1)
        salt = file.read(ord(salt_length))

        return BytesIO(get_fernet(password, salt).decrypt(file.read()))

    def _get_password(self, gui: GUI):
        self.dialog = tk.Toplevel(gui.master)
        self.dialog.grab_set()

        self.password_input = tk.StringVar()
        line = tk.Frame(self.dialog)
        label = tk.Label(line, text='password')
        entry = tk.Entry(line, textvariable=self.password_input)
        submit = tk.Button(self.dialog, text='ok', command=self.dialog.destroy)

        line.pack(side=tk.TOP)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.LEFT)
        submit.pack(side=tk.TOP)

        gui.wait_window(self.dialog)
        return bool(self.password_input.get())


    def pre_save(self, gui: GUI):
        return self._get_password(gui)

    def post_open(self, gui: GUI):
        return self._get_password(gui)
