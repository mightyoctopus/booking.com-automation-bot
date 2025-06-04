import pandas as pd
from utilities.utilities import check_current_time
from prettytable import PrettyTable

class CsvProcessing:

    def __init__(self, name, price, stars):
        self.name = name
        self.price = price
        self.stars = stars

    def save_data_into_csv(self) -> None:
        data = {
            "Hotel Name": self.name,
            "Price": self.price,
            "Star-Rating": self.stars
        }
        df = pd.DataFrame(data)
        # print("PANDAS DF RESULT: ", df)

        df.to_csv(f"data/hotels_report -- {check_current_time()}.csv", index=False)
        print("CSV file generated successfully!")


    def display_result_data_in_console(self) -> None:
        table = PrettyTable(
            field_names= ["Hotel Name", "Price", "Star-Rating"]
        )
        table.add_column(
            "Hotel Name",
            self.name
        )
        table.add_column(
            "Price",
            self.price
        )
        table.add_column(
            "Star-Rating",
            self.stars
        )
        print(table)


