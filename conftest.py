import random
import string
import yaml
import pytest as pytest
from checkers import checkout, return_stdout
from datetime import datetime

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture()
def make_folder():
    return checkout(
        f'mkdir -p {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} {data["folder_ext3"]} {data["folder_bad"]} {data["stat_file_dir"]}',
        "")


@pytest.fixture()
def clear_folder():
    return checkout(
        f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* {data["folder_ext3"]}/* {data["folder_bad"]}/*',
        "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        checkout(f'cd {data["folder_in"]}; dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                 '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not checkout(f'cd {data["folder_in"]}; mkdir {subfolder_name}', ''):
        return None, None
    if not checkout(f'cd {data["folder_in"]}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', ''):
        return subfolder_name, None

    return subfolder_name, subfile_name


@pytest.fixture()
def create_bad_archive():
    checkout(f'cd {data["folder_in"]}; 7z a -t{data["arc_type"]} {data["folder_out"]}/arx2', "Everything is Ok")
    checkout(f'cp {data["folder_out"]}/arx2.{data["arc_type"]} {data["folder_bad"]}', '')
    checkout(f'truncate -s 1 {data["folder_bad"]}/arx2.{data["arc_type"]}', '')  # сделали битым


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print(f'Finish: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture(autouse=True)
def stat_fixture():
    pass
    yield
    time_stamp = datetime.now().strftime("%H:%M:%S.%f")
    files_count = data["count"]
    file_size = data["bs"]
    cpu_stat = return_stdout("cat /proc/loadavg")
    checkout(f'cd {data["stat_file_dir"]}; echo "time = {time_stamp}, files_count = {files_count}, file_size = {file_size}, cpu_stat = {cpu_stat}" >> stat.txt','')