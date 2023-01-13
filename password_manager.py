from cryptography.fernet import Fernet
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class PasswordManager:
    key: str = None
    password_file : str = None
    password_dict : Dict[str,str] = field(default_factory=dict)


    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
            print(self.key)

    def create_password(self, path, initial_values=None):
        self.password_file = path
        if initial_values:
            for key, value in initial_values.items():
                self.add_password(key, value)

    
    def load_passowrd_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode())


    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + '\n')


    def get_password(self, site):
        return self.password_dict[site]


def main():
    pm = PasswordManager()
    password = {
        'email':'123456',
        'facebook':'my_account',
        'youtube':'helloworld123',
        'something':'myfavouritepassword',

    }
    done = False
    
    while not done:
        choice = input('Enter your choice: ')
        match choice:
            case "1":
                path = input('Enter path: ')
                pm.create_key(path)
            case "2":
                path = input('Enter path: ')
                pm.load_key(path)
            case "3":
                path = input('Enter path: ')
                pm.create_password(path, password)
            case "4":
                path = input('Enter path: ')
                pm.load_passowrd_file(path)
            case "5":
                site = input('Enter the site: ')
                password = input('Enter the password: ')
                pm.add_password(site, password)
            case "6":
                site = input('What site do you want: ')
                print(f'Password for {site} is {pm.get_password(site)}')
            case "q":
                done = True
                print('Leaving password!!! ')
            case other:
                print('Invalid choice!!')









if __name__ == '__main__':
    main() 