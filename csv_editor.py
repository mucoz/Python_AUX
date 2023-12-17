import os.path
import csv
from dataclasses import is_dataclass, asdict


class CSVEditor:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def get_path(self):
        return self.file_path

    def get_name(self):
        return os.path.basename(self.file_path)

    def create_new(self, file_path, header_list=None):
        csv_path = file_path if file_path[-3:].lower() == "csv" else file_path + ".csv"
        with open(csv_path, "w", newline='') as file:
            if header_list:
                csv_writer = csv.writer(file)
                csv_writer.writerow(header_list)
            file.close()
        self.file_path = csv_path

    def add_headers(self, header_list):
        if self.file_path:
            with open(self.file_path, "w", newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(header_list)
                file.close()

    def add_rows(self, data):
        if self.file_path is None:
            raise FileNotFoundError("File path is not set.")
        headers = self.get_headers()
        if not headers:
            raise KeyError("Keys not found.")
        if is_dataclass(data):
            data = asdict(data)
        if type(data) == list:
            contains_sublist = any(isinstance(item, list) for item in data)
            contains_subdict = any(isinstance(item, dict) for item in data)
            contains_dataclass = any(is_dataclass(item) for item in data)
            with open(self.file_path, "a", newline='') as file:
                if contains_sublist:
                    csv_writer = csv.writer(file)
                    for each_list in data:
                        csv_writer.writerow(each_list)
                elif contains_subdict:
                    csv_writer = csv.DictWriter(file, headers)
                    for each_dict in data:
                        csv_writer.writerow(each_dict)
                elif contains_dataclass:
                    csv_writer = csv.DictWriter(file, headers)
                    for each_dataclass in data:
                        csv_writer.writerow(asdict(each_dataclass))
                else:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(data)
                file.close()
        elif type(data) == dict:
            verified_data = {}
            for key in data.keys():
                if key not in headers:
                    raise KeyError("Keys are not compatible.")
            for header in headers:
                try:
                    verified_data[header] = data[header]
                except KeyError:
                    verified_data[header] = ""
            # if Counter(list(data.keys())) != Counter(self.get_headers()):
            #     raise KeyError("Keys are not compatible.")
            with open(self.file_path, "a", newline='') as file:
                # fieldnames = data.keys()
                csv_writer = csv.DictWriter(file, headers)
                csv_writer.writerow(data)
                file.close()



    def get_headers(self):
        """Needs to return list"""
        data = []
        with open(self.file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:
                    for col in row:
                        data.append(col)
                    break
            file.close()
        return data

    def read_all(self, include_headers=True):
        """Needs to return list"""
        data = []
        line = 0
        with open(self.file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:
                    if include_headers==False:
                        if line > 0:
                            data.append(row)
                        line += 1
                    else:
                        data.append(row)
            file.close()
        return data

    def read_rows(self, column_name_or_index, value):
        data = self.read_all()
        new_rows = []
        index = -1
        if isinstance(column_name_or_index, int):
            index = column_name_or_index
        else:
            for i, val in enumerate(data[0]):
                if val == column_name_or_index:
                    index = i
        if index == -1:
            raise KeyError(f"Column name or index not found : {column_name_or_index}")
        for row in data:
            if row and len(row) > index and row[index] == str(value):
                new_rows.append(row)
        return new_rows

    def read_single(self, column_name_or_index, value):
        return self.read_rows(column_name_or_index, value)[0]

    def get_data_count(self, include_headers=False):
        if include_headers:
            return len(self.read_all())
        else:
            return len(self.read_all())-1

    def update_rows(self, find_column_name_or_index, find_value, change_column_name_or_index, new_value):
        # first read everything
        data = self.read_all()
        # data to be kept
        new_rows = []
        # find indexes of the columns
        find_index = -1
        change_index = -1
        if isinstance(find_column_name_or_index, int):
            find_index = find_column_name_or_index
        else:
            for i, val in enumerate(data[0]):
                if val == find_column_name_or_index:
                    find_index = i
        if isinstance(change_column_name_or_index, int):
            change_index = change_column_name_or_index
        else:
            for i, val in enumerate(data[0]):
                if val == change_column_name_or_index:
                    change_index = i
        if find_index == -1 or len(data[0]) <= find_index:
            raise KeyError(f"Column name or index not found : {find_column_name_or_index}")
        if change_index == -1 or len(data[0]) <= change_index:
            raise KeyError(f"Column name or index not found : {change_column_name_or_index}")
        for row in data:
            if row and len(row) > find_index and len(row) > change_index:
                if row[find_index] == find_value:
                    row[change_index] = new_value
                new_rows.append(row)
            else:
                return
        # Write back rows to the file
        with open(self.file_path, "w", newline='') as file:
            csv_writer = csv.writer(file)
            # Write rows to keep
            csv_writer.writerows(new_rows)
            file.close()

    def delete_rows(self, column_name_or_index, value):
        # first read everything
        data = self.read_all()
        # data to be kept
        new_rows = []
        # find the index of the column
        index = -1
        if isinstance(column_name_or_index, int):
            index = column_name_or_index
        else:
            for i, val in enumerate(data[0]):
                if val == column_name_or_index:
                    index = i
        if index == -1 or len(data[0]) <= index:
            raise KeyError(f"Column name or index not found : {column_name_or_index}")
        for row in data:
            # Delete by index
            if row and len(row) > index and row[index] != str(value):
                new_rows.append(row)
        # Write back rows to the file
        with open(self.file_path, "w", newline='') as file:
            csv_writer = csv.writer(file)
            # Write rows to keep
            csv_writer.writerows(new_rows)
            file.close()
        
