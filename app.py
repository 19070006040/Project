from flask import Flask
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

@app.route('/hello')
def hello():
    # Azure KeyVault'dan gizli bilgilere erişim
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url="https://your-key-vault-name.vault.azure.net/", credential=credential)
    postgres_password = secret_client.get_secret("PostgreSQLPassword").value
    postgres_user = secret_client.get_secret("PostgreSQLUsername").value
    postgres_host = secret_client.get_secret("PostgreSQLHost").value
    postgres_db = secret_client.get_secret("PostgreSQLDatabase").value

    # PostgreSQL veritabanına bağlanma
    conn = psycopg2.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello, PostgreSQL!'")
    result = cursor.fetchone()[0]
    conn.close()

    return result

if __name__ == '__main__':
    app.run()
