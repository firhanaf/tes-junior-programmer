import requests
from .models import *
from decouple import config

def fetch_data_api():
    url = config('API_URL')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": config('API_USERNAME'),
        "password": config('API_PASS'),
    }

    # Kirim POST request dengan JSON body
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        try:
            # Parse the response as JSON
            response_json = response.json()

            # Assuming the 'data' key contains the list of products
            data_list = response_json.get('data', [])  # Safely get 'data' or an empty list if not found

            # Process the data (e.g., print or save to database)
            for product in data_list:
                print(f"Product Name: {product['nama_produk']}")
                print(f"Category: {product['kategori']}")
                print(f"Price: {product['harga']}")
                print(f"Status: {product['status']}")
                print("-" * 40)

            return data_list

        except ValueError:
            print("Error: Response is not in valid JSON format.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def insert_data_to_db(data):
    for item in data:
        # Retrieve or create Kategori
        kategori_name = item.get('kategori')
        kategori, created = Kategori.objects.get_or_create(nama=kategori_name)

        # Retrieve or create Status
        status_name = item.get('status')
        status, created = Status.objects.get_or_create(nama=status_name)

        # Create Produk
        Produk.objects.create(
            nama=item.get('nama_produk'),
            harga=item.get('harga'),
            kategori=kategori,  # ForeignKey to Kategori
            status=status,  # ForeignKey to Status
        )

    print("Data inserted successfully.")

def sync_data_api():
    data = fetch_data_api()
    if data:
        insert_data_to_db(data)