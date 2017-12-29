import random
import os
import json
from data_formatter import parse, check, get_data_list


class reader():
    def __init__(self, file_list):
        self.file_list = []
        self.use_list = []
        for a in range(0, len(file_list)):
            self.use_list.append(False)
        self.data_list = []
        self.temp_file = None
        self.rest = len(self.file_list)

    def gen_new_file(self, config):
        if self.rest == 0:
            return
        self.rest -= 1
        p = random.randint(0, len(self.file_list))
        while self.use_list[p]:
            p = random.randint(0, len(self.file_list))

        self.use_list[p] = True

        self.temp_file = open(os.path.join(config.get("data", "data_path"), str(self.file_list[p])), "r")

    def fetch_data(self, config):
        batch_size = config.getint("data", "batch_size")

        if batch_size > len(self.data_list):
            if self.temp_file is None:
                self.gen_new_file()

            while len(self.data_list) < 4 * batch_size:
                now_line = self.temp_file.readline()
                if now_line == '':
                    break
                data = json.loads(now_line)
                if check(data, config):
                    self.data_list.append(parse(data, config))

            if len(self.data_list) < batch_size:
                return None

        data = torch.stack(self.data[0:batch_size])
        self.data_list = self.data_list[batch_size:-1]

        return data


def create_dataset(file_list, config):
    return reader(file_list)


def init_train_dataset(config):
    return create_dataset(get_data_list(config.get("data", "train_data")), config)


def init_test_dataset(config):
    return create_dataset(get_data_list(config.get("data", "test_data")), config)


def init_dataset(config):
    train_dataset = init_train_dataset(config)
    test_dataset = init_test_dataset(config)

    return train_dataset, test_dataset