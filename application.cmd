cd e:
e: 
cd \Projects\InventoryManagement\ 
start cmd.exe @cmd /k "conda activate Practical & python manage.py runserver"
timeout 5
start msedge.exe http://127.0.0.1:8000/orderInventory/
