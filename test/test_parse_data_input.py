import os

import pytest

from tmatch.item import Item, retrieve_last_n_items


@pytest.mark.parametrize("line, expected_ip, expected_epoc", [
    ("[Time: 03/Feb/2017 11:47:35][UTC_time: 1486118855.550373][source_ip: 172.17.0.3][pkt: 15][len: 533] Tweet(1)",
     "172.17.0.3",
     1486118855),
    ("[Time: 03/Feb/2017 11:47:36][UTC_time: 1486118856.542422][source_ip: 172.17.0.2][pkt: 65][len: 548] Tweet(17)",
     "172.17.0.2",
     1486118856),
    ("[Time: 03/Feb/2017 11:47:37][UTC_time: 1486118857.572891][source_ip: 172.17.0.5][pkt: 90][len: 552] Tweet(17)",
     "172.17.0.5",
     1486118857),
])
def test_parse_etend_line(line, expected_ip, expected_epoc):
    item = Item.from_extend_output_line(line)
    assert item.ip == expected_ip
    assert item.epoch == expected_epoc


@pytest.fixture()
def complete_data():
    return open(os.path.join("resources", "extend_out.txt")).read()


def test_retrieve_last_n_ip_should_return_empty_list_if_no_ip(complete_data):
    assert [] == retrieve_last_n_items(complete_data, "1.2.3.4", 10)


def test_retrieve_last_n_ip_should_return_last_n_elements(complete_data):
    assert [Item("172.17.0.3", 1486120493),
            Item("172.17.0.3", 1486120554),
            Item("172.17.0.3", 1486120617)] == retrieve_last_n_items(complete_data, "172.17.0.3", 3)


def test_retrieve_last_n_ip_should_return_just_available_lines():
    trunked = """[Time: 03/Feb/2017 12:15:47][UTC_time: 1486120547.509251][source_ip: 172.17.0.4][pkt: 4747][len: 516] Tweet(1)
[Time: 03/Feb/2017 12:15:48][UTC_time: 1486120548.320838][source_ip: 172.17.0.6][pkt: 4771][len: 485] Tweet(1)
[Time: 03/Feb/2017 12:15:54][UTC_time: 1486120554.997427][source_ip: 172.17.0.3][pkt: 4819][len: 539] Tweet(1)
[Time: 03/Feb/2017 12:16:49][UTC_time: 1486120609.327368][source_ip: 172.17.0.4][pkt: 4919][len: 484] Tweet(1)
[Time: 03/Feb/2017 12:16:51][UTC_time: 1486120611.456094][source_ip: 172.17.0.2][pkt: 4967][len: 524] Tweet(1)
[Time: 03/Feb/2017 12:16:57][UTC_time: 1486120617.627161][source_ip: 172.17.0.3][pkt: 4992][len: 552] Tweet(17)
[Time: 03/Feb/2017 12:17:10][UTC_time: 1486120630.243241][source_ip: 172.17.0.5][pkt: 5067][len: 521] Tweet(1)"""
    assert [Item("172.17.0.3", 1486120554),
            Item("172.17.0.3", 1486120617)] == retrieve_last_n_items(trunked, "172.17.0.3", 3)


def test_retrieve_last_n_ip_should_ignore_empty_lines():
    some_empty_lines = """

[Time: 03/Feb/2017 12:15:54][UTC_time: 1486120554.997427][source_ip: 172.17.0.3][pkt: 4819][len: 539] Tweet(1)

[Time: 03/Feb/2017 12:16:57][UTC_time: 1486120617.627161][source_ip: 172.17.0.3][pkt: 4992][len: 552] Tweet(17)
    """
    assert [Item("172.17.0.3", 1486120554),
            Item("172.17.0.3", 1486120617)] == retrieve_last_n_items(some_empty_lines, "172.17.0.3", 3)
