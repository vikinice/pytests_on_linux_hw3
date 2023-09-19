import pytest

from checkers import checkout_negativ
import yaml

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):  # e извлекли из архива

        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z e arx2.{data["arc_type"]} -o{data["folder_ext"]} -y', "ERRORS")

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z t arx2.{data["arc_type"]}', "Is not")



if __name__ == '__main__':
    pytest.main(['-v'])