import json
import requests


# Custom imports
import general_methods as gm

from sqlite3_handler.db_handler import SQLiteHandler


# # ===== General Variables =================================================================== General Variables =====
...
# # ===== General Variables =================================================================== General Variables =====

...
# Parsing the arguments
args = gm.ArgParser()

# Directories and names of files class
dan = gm.DaNHandler()


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


def get_main_data(save_to_file=False, file_path="./main_data.json"):

    # json main data -> manufacturer / model / part categories
    url = "https://api2.myparts.ge/api/en/main"
    response = requests.get(url)
    json_data = json.dumps(json.loads(response.text), indent=4)

    if save_to_file:
        with open(file_path, "w") as f:
            f.write(json_data)


def get_product_detail_data(product_id, save_to_file=False, file_path="./product_{product_id}_detail_data.json"):
    if file_path == "./product_{product_id}_detail_data.json":
        file_path = f"./product_{product_id}_detail_data.json"

    # json product detail data
    url = f"https://api2.myparts.ge/api/en/products/detail/{product_id}"
    response = requests.get(url)
    json_data = json.dumps(json.loads(response.text), indent=4)

    if save_to_file:
        with open(file_path, "w") as f:
            f.write(json_data)


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def start_app():
    # get_main_data(save_to_file=True)
    print(args)
    print(dan)
    print("Hi")

if __name__ == '__main__':
    start_app()
