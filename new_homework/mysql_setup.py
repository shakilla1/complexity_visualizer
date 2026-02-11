from fabric import Connection
import subprocess

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = None

if HOST == '127.0.0.1':
    def run_command(command):
        subprocess.run(command, shell=True, check=True)
else:
    connection = Connection(
        host=HOST,
        user=USER,
        connect_kwargs={'password': PASSWORD} if PASSWORD else {}
    )
    def run_command(command):
        connection.run(command, warn=True)


def install_mysql():
    print("Updating packages...")
    run_command("apt update -y")
    print("Installing MySQL Server...")
    run_command("apt install mysql-server -y")
    print("MySQL installation completed.\n")


def create_database():
    db_name = "fabric_database"
    print(f"Creating database '{db_name}'...")
    run_command(f'mysql -e "CREATE DATABASE IF NOT EXISTS {db_name};"')
    print("Database created successfully.\n")


if __name__ == "__main__":
    install_mysql()
    create_database()
