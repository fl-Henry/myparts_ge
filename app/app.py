import os
import sys
import json
import time
import datetime
import requests
import pandas as pd

# Custom imports
import general_methods as gm

from print_tags import Tags


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


def get_json_data(url, file_path=None, save_to_file=False, method="GET", request_data=None, update_key=None):
    if file_path is None and save_to_file is True:
        raise ValueError("[ERROR] get_json_data > save_to_file is True, but file_path is not specified")
    if update_key is None:
        update_key = args.update_key

    # API request to get json
    json_data = None
    if update_key:
        print(f"\n{Tags.LightYellow}Getting data from {url}{Tags.ResetAll}")
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=request_data)
        else:
            response = requests.get(url)
        json_data = json.loads(response.text)

        if save_to_file:
            with open(file_path, "w") as f:
                f.write(json.dumps(json_data, indent=4))
                print(f"Data saved to {file_path}")

    if json_data is None:
        if not os.path.exists(file_path):
            raise FileExistsError(f"File doesn't exist: {file_path}")
        else:
            with open(file_path, "r") as f:
                json_data = json.loads(f.read())

    return json_data


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def get_main_data(save_to_file=False, file_path=None):

    # URL with json main data -> manufacturer / model / part categories
    url = "https://www.myparts.ge/build/assets/appdata/en.json"

    # File path for main_data_json
    if file_path is not None:
        dan.files.update({"main_data": file_path})
    else:
        dan.files.update({"main_data": f"{dan.dirs['jsons']}main_data.json"})

    json_data = get_json_data(url, file_path=dan.files["main_data"], save_to_file=save_to_file)
    return json_data


def get_orders_data(request_data):
    """
        request_data = {
            "page": "1",                           \n
            "man_id": "41",                        \n
            "model_id": "1089",                    \n
            "year_from": "2018",                   \n
            "cat_id": "1241",                      \n
            "pr_type_id": 1,            | It seems that it is the main category (Auto parts or Vehicles)           \n
            "limit": 15                 | Number of ads shown on the page           \n
        }

    :param request_data: dict
    :param save_to_file:
    :param file_path:
    :return:
    """
    # URL with json containing orders data
    url = "https://api2.myparts.ge/api/en/products/get"
    request_data.update({"pr_type_id": 1})
    if request_data.get("limit") is None:
        request_data.update({"limit": 100})

    # Getting all products' ads. There is a pagination, so I use a while loop
    ...
    # Pagination
    # ["data"]["pagination"]["currentPage"] <int>
    # ["data"]["pagination"]["nextPage"] <int> or None
    # ["data"]["pagination"]["totalPages"] <int> or? None  # I don't use this
    json_data = {"data": {"pagination": {"nextPage": 1}}}
    raw_products_list = []
    while json_data["data"]["pagination"]["nextPage"] is not None:
        request_data.update({"page": json_data["data"]["pagination"]["nextPage"]})
        json_data = get_json_data(
            url,
            request_data=request_data,
            method="POST",
            update_key=True
        )
        raw_products_list.extend(json_data["data"]["products"])

    # Parsing raw_products_list
    ...
    # Product details
    # ["product_id"] <int>
    # ["cat_id"] <int>
    # ["currency_id"] <int> -> 3 is GEL
    # ["price"] <str> GEL -> float
    # ["views"] <int>
    # ["cond_type_id"] <int>
    # ["order_date"] <datetime>?
    products_list = []
    for product in raw_products_list:
        product_dict = {
            "product_id": product["product_id"],
            "cond_type_id": product["cond_type_id"],
            "man_id": request_data["man_id"],
            "model_id": request_data["model_id"],
            "year": request_data["year_from"],
            "cat_id": product["cat_id"],
            "price": product["price"],
            "currency_id": product["currency_id"],
            "views": product["views"],
            "order_date": product["order_date"],
        }
        products_list.append(product_dict)

    return products_list

#
# def get_product_detail_data(product_id, save_to_file=False, file_path=None):
#
#     # URL with json containing product detail data
#     url = f"https://api2.myparts.ge/api/en/products/detail/{product_id}"
#
#     # File path for *_detail_data_json
#     if file_path is not None:
#         dan.files.update({f"product_{product_id}": file_path})
#     else:
#         dan.files.update({f"product_{product_id}": f"{dan.dirs['jsons']}{product_id}_detail_data.json"})
#
#     json_data = get_json_data(url, file_path=dan.files[f"product_{product_id}"], save_to_file=save_to_file)
#     return json_data

#
# def get_products_data(orders_data_json):
#     # https://api2.myparts.ge/api/en/products/detail/11923084
#     # ["lang_data"]["title"] <str>
#     # ["cat_id"] <int>
#     # ["currency_id"] <int> -> 3 is GEL
#     # ["price"] <str> GEL -> float
#     # ["views"] <int>
#     # ["cond_type_id"] <int>
#     # ["order_date"] <datetime>?
#     products_data_json = []
#     product_id_list = [x["product_id"] for x in orders_data_json]
#     for product_id in product_id_list:
#         product_detail_data = get_product_detail_data(product_id, save_to_file=True)
#         product_details_dict = {
#             "product_id": product_detail_data["data"]["product_id"],
#             "title": product_detail_data["data"]["lang_data"]["title"],
#             "cond_type_id": product_detail_data["data"]["cond_type_id"],
#             "cat_id": product_detail_data["data"]["cat_id"],
#             "price": product_detail_data["data"]["price"],
#             "currency_id": product_detail_data["data"]["currency_id"],
#             "views": product_detail_data["data"]["views"],
#             "order_date": product_detail_data["data"]["order_date"],
#         }
#         products_data_json.append(product_details_dict)
#     return products_data_json


def get_manufacturers(main_data_json):
    """
        manufacturers_json = {
            "man_id": int,                     \n
            "man_name": str,                   \n
        }
    :param main_data_json:
    :return:
    """
    manufacturers_json = []
    for raw_man in main_data_json["Mans"]:
        if raw_man["is_car"] is True:
            man_dict = {
                "man_id": int(raw_man["man_id"]),
                "man_name": str(raw_man["man_name"]),
            }
            manufacturers_json.append(man_dict)

    return manufacturers_json


def get_models(main_data_json):
    """
        model_dict = {
            "model_id": int,                   \n
            "man_id": int,                     \n
            "model_name": str,                 \n
        }

    :param main_data_json:
    :return:
    """
    models_json = []
    for item in main_data_json["Models"]:
        model_dict = {
            "model_id": int(item["model_id"]),
            "man_id": int(item["man_id"]),
            "model_name": item["model_name"],
        }
        models_json.append(model_dict)

    return models_json


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

    json_to_return = []
    for category in parent_list:
        category_dict = {
            "id": int(category["id"]),
            "parent_id": int(category["parent_id"]),
            "text": str(category["text"]),

        }
        json_to_return.append(category_dict)

    return json_to_return


def replace_manufacturer(orders_data_df, manufacturers_df):
    df_to_return = pd.DataFrame()
    for index, row in orders_data_df.iterrows():
        man_name = manufacturers_df[(manufacturers_df["man_id"]) == int(row["man_id"])].reset_index(drop=True)
        row = row.to_frame().T.reset_index(drop=True)
        row = pd.concat([row, man_name], axis=1)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)
    df_to_return = df_to_return.drop(columns=["man_id", "man_id"])
    return df_to_return


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def start_app():

    # STDOUT input parameters
    print(args)
    print(dan, end="\n\n")

    # Getting or updating main_data_json
    main_data_json = get_main_data(save_to_file=True)

    # Getting Manufacturers list
    manufacturers_json = get_manufacturers(main_data_json)
    manufacturers_df = pd.DataFrame(
        manufacturers_json,
        columns=["man_id", "man_name"]
    )

    # Getting models of the manufacturers
    models_json = get_models(main_data_json)
    models_df = pd.DataFrame(
        models_json,
        columns=["model_id", "man_id", "model_name"]
    )

    # years 1963 - this year = 60 last years // List to check if the selected year is in this list
    today_year = datetime.date.today().year
    years_list = range(today_year - 60, today_year + 1)

    # Getting categories
    categories_json = get_categories(main_data_json)
    categories_df = pd.DataFrame(
        categories_json,
        columns=["id", "parent_id", "text"]
    )

    # Getting condition types
    condition_types_json = []
    cond_type_id_count = len(main_data_json["Languages"]["CondTypes"])
    for condition_type_name, cond_type_id in zip(main_data_json["Languages"]["CondTypes"], range(cond_type_id_count)):
        condition_type_dict = {
            "cond_type_id": cond_type_id,
            "cond_type_name": condition_type_name,
        }
        condition_types_json.append(condition_type_dict)
    condition_types_df = pd.DataFrame(
        condition_types_json,
        columns=["cond_type_id", "cond_type_name"]
    )

    # Getting orders_data
    request_data = {
        "man_id": "41",
        "model_id": "1089",
        "year_from": "2018",
        "cat_id": "1261",
    }
    orders_data_json = get_orders_data(request_data)
    orders_data_df = pd.DataFrame(
        orders_data_json,
    )

    # # Getting products' products_data
    # products_data_json = get_products_data(orders_data_json)
    # products_data_df = pd.DataFrame(
    #     products_data_json,
    # )
    # pd.set_option("display.max_rows", None)
    # print(products_data_df)
    ...
    # Creating table to save as CSV
    df = replace_manufacturer(orders_data_df, manufacturers_df)
    print(df)


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()
