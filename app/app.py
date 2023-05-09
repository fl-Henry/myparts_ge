import os
import csv
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


def clear_screen():
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # Else Operating System is Windows (os.name = nt)
        _ = os.system('cls')


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
        print(f"\n{Tags.LightYellow}Getting data from {file_path}{Tags.ResetAll}")
        if not os.path.exists(file_path):
            raise FileExistsError(f"File doesn't exist: {file_path}")
        else:
            with open(file_path, "r") as f:
                json_data = json.loads(f.read())

    return json_data


def save_to_csv(to_csv_df, file_path=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if file_path is not None:
        dan.files.update({"main_data": file_path})
    else:
        file_path = f"{dan.dirs['csvs']}{timestamp}_orders_data.csv"
        dan.files.update({f"{timestamp}_orders_data.csv": file_path})

    to_csv_df.to_csv(file_path, sep=';', encoding='utf-8')
    print(f"\n{Tags.LightYellow}Saved to: {file_path}{Tags.ResetAll}")


def df_select_one(df: pd.DataFrame, column, value):
    return df[df[column] == value].reset_index(drop=True).iloc[0].to_frame().T


def df_select_all(df: pd.DataFrame, column, value):
    return df[df[column] == value].reset_index(drop=True)


def compact_df(main_df, columns_num=4):
    df_len = len(main_df) // columns_num
    df_1 = main_df.iloc[:df_len]
    len_counter = 1
    while df_len * len_counter < len(main_df):
        df_2 = main_df.iloc[len_counter * df_len:(len_counter + 1) * df_len].reset_index(drop=True)
        df_1 = pd.concat([df_1, df_2], axis=1).reset_index(drop=True)
        len_counter += 1
    return df_1


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def get_main_data(save_to_file=False, file_path=None):

    # URL with json main data -> manufacturer / model / part categories
    # url = "https://www.myparts.ge/build/assets/appdata/en.json"
    url = "https://www.myparts.ge/build/assets/appdata/ka.json"

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
    # ["price"] <str> -> float  # In a pair with currency_id
    # ["price_value"] <str> -> float  # GEL
    # ["views"] <int>
    # ["cond_type_id"] <int>
    # ["order_date"] <datetime>?
    products_list = []
    for product in raw_products_list:
        product_dict = {
            "product_id": product["product_id"],
            "title": product["lang_data"]["title"],
            "cond_type_id": product["cond_type_id"],
            "man_id": request_data["man_id"],
            "model_id": request_data["model_id"],
            "year": request_data["year_from"],
            "year_from": product["product_models"][0]["year_from"],
            "year_to": product["product_models"][0]["year_to"],
            "cat_id": product["cat_id"],
            "price_value": float(product["price_value"]),
            # "price": float(product["price"]),
            # "currency_id": product["currency_id"],
            "views": product["views"],
            "order_date": product["order_date"],
        }
        products_list.append(product_dict)

    return products_list


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


def get_currencies(main_data_json):
    """
        currencies_json = {
            "currency_id": int,            \n
            "currency_name": str,          \n
        }
    :param main_data_json:
    :return:
    """
    currencies_json = []
    for raw_currency in main_data_json["Currencies"]:
        currency_dict = {
            "currency_id": int(raw_currency["currencyID"]),
            "currency_name": str(raw_currency["title"]),
        }
        currencies_json.append(currency_dict)

    return currencies_json


def get_categories(main_data_json):
    """
        return = [
            {
                id: int,                    \n
                parent_id: int,             \n
                text: str,                  \n
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
            raise Exception("[ERROR] get_categories > infinity loop")
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


def get_parent_categories(categories_df, sub_category_id: int):

    # Creating start list with categories DataFrames (from child to parent)
    last_category = categories_df[categories_df["id"] == sub_category_id].reset_index(drop=True)
    categories_df_list = [last_category]

    # Finding all parent categories
    infinity_loop_counter = 0
    while categories_df_list[-1]["parent_id"][0] != 0:

        # Checking infinity loop
        if infinity_loop_counter > 10000:
            raise Exception("[ERROR] get_parent_categories > infinity loop")
        else:
            infinity_loop_counter += 1

        # parent_id for current sub_category
        parent_id = categories_df_list[-1]["parent_id"][0]

        # Finding parent category and append to list
        parent_category_df = categories_df[categories_df["id"] == parent_id].reset_index(drop=True)
        categories_df_list.append(parent_category_df)

    # Removing last category ("Auto parts")
    categories_df_list.pop()

    # Cleaning list of categories
    categories_df_list = [x["text"][0] for x in reversed(categories_df_list)]

    # Creating DataFrame
    categories_list_df = pd.DataFrame(
        [[sub_category_id, categories_df_list[0], [666], categories_df_list[-1]]],
        columns=["cat_id", "main_category", "sub_categories", "product_name"]
    )
    categories_list_df.at[0, "sub_categories"] = categories_df_list[1:-1]

    return categories_list_df


def replace_df_column(main_df, column_data_df, joint_column_name, columns_to_join: list[str] = None):

    # Drop every column that not in not_drop_list
    if columns_to_join is not None:
        not_drop_list = [joint_column_name, *columns_to_join]
        for column_name in column_data_df.columns:
            if column_name not in not_drop_list:
                column_data_df = column_data_df.drop(columns=column_name)

    # Join DataFrames and drop joint column
    df_to_return = pd.DataFrame()
    for index, row in main_df.iterrows():
        column_data = column_data_df[(column_data_df[joint_column_name]) == int(row[joint_column_name])].reset_index(drop=True)
        row = row.to_frame().T.reset_index(drop=True)
        row = pd.concat([row, column_data], axis=1)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)
    df_to_return = df_to_return.drop(columns=[joint_column_name, joint_column_name])
    return df_to_return


def replace_manufacturer(orders_data_df, manufacturers_df):
    df_to_return = pd.DataFrame()
    for index, row in orders_data_df.iterrows():
        man_name = manufacturers_df[(manufacturers_df["man_id"]) == int(row["man_id"])].reset_index(drop=True)
        row = row.to_frame().T.reset_index(drop=True)
        row = pd.concat([row, man_name], axis=1)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)
    df_to_return = df_to_return.drop(columns=["man_id", "man_id"])
    return df_to_return


def choosing_request_data(manufacturers_df, models_df, years_list, categories_df):
    clear_screen()

    # Selecting manufacturer
    pd.set_option("display.max_rows", None)
    print(f"{Tags.LightYellow}{Tags.Reverse}Manufacturers table{Tags.ResetAll}")
    print(compact_df(manufacturers_df, columns_num=4).fillna(0).astype({"man_id": "int32"}).to_string(index=False))
    print("Select manufacturer's ID (Ex: 41): ", end="")
    man_id = int(input())
    man_name = df_select_one(manufacturers_df, "man_id", man_id)["man_name"][0]
    clear_screen()

    # Selecting model
    models_df = df_select_all(models_df, "man_id", man_id)
    compact_models_df = compact_df(models_df, columns_num=4).fillna(0).astype({"model_id": "int32"})
    compact_models_df = compact_models_df.drop(columns=["man_id"]).to_string(index=False)
    print(f"{Tags.LightYellow}{Tags.Reverse}Models table{Tags.ResetAll}")
    print(compact_models_df)
    print(f"Manufacturer: {man_name}; Select models's ID (Ex: 1139): ", end="")
    model_id = int(input())
    model_name = df_select_one(models_df, "model_id", model_id)["model_name"][0]
    clear_screen()

    # Selecting year
    print(f"\nAvailable years: {years_list[0]} - {years_list[-1]}")
    print(f"Manufacturer: {man_name}; Model: {model_name}; Select year (Ex: 1998): ", end="")
    year = int(input())
    clear_screen()

    # Selecting category
    cat_id = 19
    current_categories_df = df_select_all(categories_df, "parent_id", cat_id)
    categories_list = []
    while len(current_categories_df) != 0:
        print(f"{Tags.LightYellow}{Tags.Reverse}Categories table{Tags.ResetAll}")
        print(current_categories_df.to_string(index=False, columns=["id", "text"]))
        print(f"Manufacturer: {man_name}; Model: {model_name}; Year: {year}")
        print("Categories:", " > ".join(categories_list), "Select category's ID (Ex: 457): ", end="")
        cat_id = int(input())
        cat_name = df_select_one(categories_df, "id", cat_id)["text"][0]
        categories_list.append(cat_name)
        current_categories_df = df_select_all(categories_df, "parent_id", cat_id)
        clear_screen()

    print(f"Manufacturer: {man_name}; Model: {model_name}; Year: {year}")
    print("\nCategories:", " > ".join(categories_list))

    # Setting request_data dict
    request_data = {
        "man_id": man_id,
        "model_id": model_id,
        "year_from": year,
        "cat_id": cat_id,
    }
    return request_data


# # ===== Start app =================================================================================== Start app =====
...
# # ===== Start app =================================================================================== Start app =====


def start_app():

    # STDOUT input parameters
    print(args)
    print(dan, end="\n\n")

    args.update_key = True

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

    # Getting Currencies
    currencies_json = get_currencies(main_data_json)
    currencies_df = pd.DataFrame(
        currencies_json,
        columns=["currency_id", "currency_name"]
    )

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

    request_data = choosing_request_data(manufacturers_df, models_df, years_list, categories_df)

    # Getting orders_data
    # request_data = {
    #     "man_id": "41",
    #     "model_id": "1089",
    #     "year_from": "2018",
    #     "cat_id": "1261",
    # }
    orders_data_json = get_orders_data(request_data)
    orders_data_df = pd.DataFrame(
        orders_data_json,
    )

    if len(orders_data_df) > 0:
        # Creating table to save as CSV // replace Manufacturer
        to_csv_df = replace_df_column(orders_data_df, manufacturers_df, "man_id")

        # # Replace Currency
        # to_csv_df = replace_df_column(to_csv_df, currencies_df, "currency_id")

        # Replace Condition type
        to_csv_df = replace_df_column(to_csv_df, condition_types_df, "cond_type_id")

        # Replace Model
        to_csv_df = replace_df_column(to_csv_df, models_df, "model_id", columns_to_join=["model_name"])

        # Get parent categories by children
        categories_list_df = get_parent_categories(categories_df, int(request_data["cat_id"]))

        # Replace Categories
        to_csv_df = replace_df_column(to_csv_df, categories_list_df, "cat_id")

        columns_order = ["product_id", "man_name", "model_name", "year", "main_category", "sub_categories", "product_name",
                         "title", "year_from", "year_to", "cond_type_name", "price_value", "views", "order_date"]

        to_csv_df = to_csv_df[columns_order]
        # print(to_csv_df)
        save_to_csv(to_csv_df)
        print(f"The details of the orders have been {Tags.LightYellow}{Tags.Reverse}successfully saved{Tags.ResetAll}")
    else:
        print(f"{Tags.LightYellow}{Tags.Reverse}There are no any orders!!!{Tags.ResetAll}")


def anchor_for_navigate():
    pass


if __name__ == '__main__':
    start_app()
