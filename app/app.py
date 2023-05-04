import os
import sys
import json
import time
import datetime
import requests

# Custom imports
import general_methods as gm

from print_tags import Tags
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
    json_data = None
    if args.update_key:
        print(f"\n{Tags.LightYellow}Updating main_data_json{Tags.ResetAll}")
        url = "https://www.myparts.ge/build/assets/appdata/en.json"
        response = requests.get(url)
        json_data = json.loads(response.text)

        if save_to_file:
            with open(file_path, "w") as f:
                f.write(json.dumps(json_data, indent=4))

    if json_data is None:
        if not os.path.exists(file_path):
            raise FileExistsError(f"File doesn't exist: {file_path}")
        else:
            with open(file_path, "r") as f:
                json_data = json.loads(f.read())

    return json_data


def get_orders_data(save_to_file=False, file_path="./main_data.json"):

    # json contains orders data
    url = "https://api2.myparts.ge/api/en/main"
    response = requests.get(url)
    json_data = json.dumps(json.loads(response.text), indent=4)

    if save_to_file:
        with open(file_path, "w") as f:
            f.write(json_data)

    return json_data


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

    return json_data


def decapsule_children(parent_dict: dict, children_key="children", parent_id_key=None):
    """
    parent_dict = {
        id_key: value,                      \n
        key: value,                         \n
        children_key: list,                 \n
    }

    return = [
        {
            id_key: value,                  \n
            parent_id_key: value,           \n
            key: value,                     \n
            children_key: list,             \n
        },
        {...}
    ]

    :param parent_dict: dict
    :param children_key: str
    :param parent_id_key: str
    :return:
    """
    if parent_id_key is None:
        parent_id_key = [*parent_dict.keys()][0]

    if parent_dict.get("parent_id") is None:
        parent_dict.update({"parent_id": 0})

    try:
        list_to_return = [parent_dict]
        for children_item in parent_dict[children_key]:
            children_dict = {
                "parent_id": parent_dict[parent_id_key],
            }
            if type(children_item) == dict:
                for key in children_item.keys():
                    children_dict.update({key: children_item[key]})
            else:
                children_dict.update(children_item)

            list_to_return.append(children_dict)

        del list_to_return[0][children_key]
        return list_to_return

    except KeyError:
        return [parent_dict]


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def get_manufacturers(main_data_json):
    """
        manufacturers_json = {<man_id:int>: <man_name:str>}
    """
    manufacturers_json = {}
    for raw_man in main_data_json["Mans"]:
        if raw_man["is_car"] is True:
            man_dict = {raw_man["man_id"]: raw_man["man_name"]}
            manufacturers_json.update(man_dict)

    return manufacturers_json


def get_categories(main_data_json):
    """
        return = [
            id: {
                parent_id,             \n
                text,                  \n
            },{...}
        ]

    :param main_data_json:
    :return: list[dicts]
    """

    # main_data_json["Cats"][19] < text: Auto parts
    parent_list = [main_data_json["Cats"]["19"]]
    loop_exit_key = False
    # Counter to exit infinity loop
    infinity_loop_counter = 0
    while not loop_exit_key:

        # Checking infinity loop
        if infinity_loop_counter > 10000:
            raise Exception("[ERROR] Getting categories > infinity loop")
        else:
            infinity_loop_counter += 1

        # Loop logic / decapsulation of children dicts
        loop_list = []
        start_len = len(parent_list)
        for parent in parent_list:
            loop_list.extend(decapsule_children(parent, parent_id_key="id"))
        parent_list = loop_list
        end_len = len(parent_list)

        # Leave loop if change of parent_list len is zero
        if start_len == end_len:
            loop_exit_key = True

    json_to_return = {}
    for category in parent_list:
        category_dict = {
            category["id"]: {
                "parent_id": category["parent_id"],
                "text": category["text"],
            }
        }
        json_to_return.update(category_dict)

    return json_to_return


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def start_app():
    # get_main_data(save_to_file=True)
    print(args)
    print(dan, end="\n\n")

    # Getting or updating main_data_json
    main_data_path = f"{dan.dirs['jsons']}main_data.json"
    main_data_json = get_main_data(save_to_file=True, file_path=main_data_path)

    # Getting Manufacturers list
    manufacturers_json = get_manufacturers(main_data_json)

    # Getting models of the manufacturers
    for raw_model in main_data_json["Models"]:
        if raw_model["man_id"] in [*manufacturers_json.keys()]:
            pass

    # years 1963 - this year = 60 last years
    today_year = datetime.date.today().year
    years_list = range(today_year - 60, today_year + 1)

    # Getting categories
    categories = get_categories(main_data_json)
    print(categories)

    # print(type(main_data_json["Cats"]["19"]["children"][0]))
    # print(type(main_data_json["Cats"]["19"]["children"][0]) == dict)
    # print(main_data_json["Cats"]["19"])

    # print(main_data_json["Mans"])
    # print(json.dumps(manufacturers_json, indent=2))


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()
