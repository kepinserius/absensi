from cryptography.fernet import Fernet

# Fungsi untuk membuat kunci enkripsi
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Fungsi untuk membaca kunci enkripsi
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# Fungsi untuk mengenkripsi data
def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

# Fungsi untuk mendekripsi data
def decrypt_data(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted
