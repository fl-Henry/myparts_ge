import json
import sqlite3
import requests





def main():
    base_url = "https://api2.myparts.ge/api/en/products/detail/"
    for id_ in range(12046100, 12046352):
        url = f"{base_url}{id_}"
        response = requests.get(url)
        print("URL:", url, end=" ")
        json_data = json.loads(response.text)
        if len(json_data["data"]) > 0:
            print(json_data["data"]["pr_type_id"])
        else:
            print(" --/-- ")


if __name__ == '__main__':
    main()