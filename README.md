# Order Manager

techStack :
Python, Django(v3.2.9), HTML5, CSS3, fetch API, JavaScript , sqlite3

dependent Library :
django_weasyprint(v2.1.0), djangorestframework(v3.12.4),

To run ths application locally follow below steps.

Run following command in cmd

Step 1 : Clone this Repository

```bash
git clone https://github.com/ShivChevli/IngredientManager.git
```

Step 2 : Navigate to Project Directory

```bash
cd IngredientManager
```

Step 3 : Create python Virtual Environment 

for windows 
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

For Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Step 4 : Install dependency

```bash
pip install -r requirements.txt
```

Step 5 : Create database and it seed with Inital data

```bash
python manage.py migrate
python manage.py loaddata ./seedData/orderInventory.json
```

Step 6: Start Server

```bash
python manage.py runserver
```

Step 7 :
Now open "http://127.0.0.1:8000/orderInventory/" url in your browser to navigate home page of web-application

## Notes

linux setup is recommanded setup, We are using one python library which require additional Package. In linux we can install it by following command.

```bash
sudo apt-get install libpangocairo-1.0-0
```

- Totake Backup we need to run following command. 
    ```bash
    python manage.py dumpdata orderInventory > ./seedData/orderInventory
    ```