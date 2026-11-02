# Tests for main.py (Inventory Management System)
# Run with:  pytest test_main.py -v
#
# The tests use these pytest fixtures:
#   monkeypatch  gives fake keyboard input and changes FILE_NAME
#   capsys       catches the printed text
#   tmp_path     gives a temporary folder, so your real inventory.json does not change

import pytest

import file_handler
import main
from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct


# ---------- Fixtures and helpers ----------

@pytest.fixture
def fake_input(monkeypatch):
    """Use this fixture to give a list of answers to input()."""
    def set_answers(answers):
        answers = iter(answers)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    return set_answers


@pytest.fixture
def inventory():
    """An inventory with one physical product and one digital product."""
    inv = Inventory()
    inv.add_product(PhysicalProduct("P001", "Mouse", 20.0, 10, 0.2))
    inv.add_product(DigitalProduct("D001", "Ebook", 5.0, 100, 25.0))
    return inv


@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    """Make file_handler use a temporary inventory.json."""
    path = tmp_path / "inventory.json"
    monkeypatch.setattr(file_handler, "FILE_NAME", str(path))
    return path


# ---------- Input helpers ----------

def test_input_text_accepts_text(fake_input):
    fake_input(["Mouse"])
    assert main.input_text("Name: ") == "Mouse"


def test_input_text_asks_again_when_empty(fake_input, capsys):
    fake_input(["", "   ", "Mouse"])
    assert main.input_text("Name: ") == "Mouse"
    assert capsys.readouterr().out.count("This field cannot be empty.") == 2


def test_input_text_removes_spaces(fake_input):
    fake_input(["  Mouse  "])
    assert main.input_text("Name: ") == "Mouse"


@pytest.mark.parametrize("typed, expected", [("25.50", 25.5), ("0", 0), ("100", 100)])
def test_input_price_accepts_valid_values(fake_input, typed, expected):
    fake_input([typed])
    assert main.input_price("Price: ") == expected


def test_input_price_rejects_negative_and_text(fake_input, capsys):
    fake_input(["-1", "abc", "10"])
    assert main.input_price("Price: ") == 10
    output = capsys.readouterr().out
    assert "The price cannot be less than 0." in output
    assert "Type a number" in output


def test_input_quantity_accepts_whole_number(fake_input):
    fake_input(["10"])
    assert main.input_quantity("Stock: ") == 10


def test_input_quantity_rejects_decimal_and_negative(fake_input, capsys):
    fake_input(["1.5", "-3", "4"])
    assert main.input_quantity("Stock: ") == 4
    output = capsys.readouterr().out
    assert "Type a whole number" in output
    assert "The quantity cannot be less than 0." in output


def test_input_size_rejects_zero_and_text(fake_input, capsys):
    fake_input(["0", "x", "1.5"])
    assert main.input_size("Weight: ") == 1.5
    output = capsys.readouterr().out
    assert "The value must be more than 0." in output
    assert "Type a number" in output


@pytest.mark.parametrize("choice", ["1", "2"])
def test_input_product_type_accepts_1_and_2(fake_input, choice):
    fake_input([choice])
    assert main.input_product_type() == choice


def test_input_product_type_asks_again_when_invalid(fake_input, capsys):
    fake_input(["3", "a", "2"])
    assert main.input_product_type() == "2"
    assert capsys.readouterr().out.count("Invalid type. Enter 1 or 2.") == 2


# ---------- Add product ----------

def test_add_physical_product(fake_input, capsys):
    inv = Inventory()
    fake_input(["p010", "1", "Keyboard", "50", "5", "1.5"])
    main.add_product(inv)

    product = inv.search_product("P010")   # the ID changes to upper case
    assert isinstance(product, PhysicalProduct)
    assert product.get_name() == "Keyboard"
    assert product.get_price() == 50
    assert product.get_stock() == 5
    assert product.get_weight() == 1.5
    assert "Product added successfully!" in capsys.readouterr().out


def test_add_digital_product(fake_input):
    inv = Inventory()
    fake_input(["D010", "2", "Game", "30", "999", "2048"])
    main.add_product(inv)

    product = inv.search_product("D010")
    assert isinstance(product, DigitalProduct)
    assert product.get_download_size() == 2048


def test_add_duplicate_id_is_refused(fake_input, capsys, inventory):
    fake_input(["p001"])
    main.add_product(inventory)

    assert "P001 already exists" in capsys.readouterr().out
    assert len(inventory.get_products()) == 2


# ---------- Update stock ----------

def test_update_stock_changes_value_and_history(fake_input, capsys, inventory):
    fake_input(["p001", "25"])
    main.update_stock(inventory)

    product = inventory.search_product("P001")
    assert product.get_stock() == 25
    assert product.get_history() == [10, 15]
    assert "Stock updated successfully!" in capsys.readouterr().out


def test_update_stock_same_value(fake_input, capsys, inventory):
    fake_input(["P001", "10"])
    main.update_stock(inventory)

    assert "The stock is the same. No change made." in capsys.readouterr().out
    assert inventory.search_product("P001").get_history() == [10]


def test_update_stock_product_not_found(fake_input, capsys, inventory):
    fake_input(["X999"])
    main.update_stock(inventory)
    assert "Product not found." in capsys.readouterr().out


# ---------- Search product ----------

def test_search_physical_product(fake_input, capsys, inventory):
    fake_input(["p001"])
    main.search_product(inventory)

    output = capsys.readouterr().out
    assert "Product Found" in output
    assert "Name: Mouse" in output
    assert "Weight: 0.2 kg" in output
    assert "Fulfilment:" in output


def test_search_digital_product(fake_input, capsys, inventory):
    fake_input(["D001"])
    main.search_product(inventory)

    output = capsys.readouterr().out
    assert "Name: Ebook" in output
    assert "Download size: 25.0 MB" in output


def test_search_product_not_found(fake_input, capsys, inventory):
    fake_input(["X999"])
    main.search_product(inventory)
    assert "Product not found." in capsys.readouterr().out


# ---------- Full program (main loop and file) ----------

def test_display_empty_inventory(fake_input, capsys, temp_file):
    fake_input(["1", "6"])
    main.main()

    output = capsys.readouterr().out
    assert "not found" in output
    assert "The inventory is empty." in output


def test_add_then_display(fake_input, capsys, temp_file):
    fake_input(["2", "P001", "1", "Mouse", "20", "10", "0.2",   # add product
                "1",                                          # display
                "6"])                                         # exit
    main.main()

    output = capsys.readouterr().out
    assert "P001" in output
    assert "Mouse" in output
    assert "The inventory is empty." not in output


def test_invalid_menu_option(fake_input, capsys, temp_file):
    fake_input(["9", "abc", "6"])
    main.main()
    assert capsys.readouterr().out.count("Invalid option. Enter a number from 1 to 6.") == 2


def test_exit_saves_and_next_run_loads(fake_input, capsys, temp_file):
    # First run: add two products, then exit (exit saves the file).
    fake_input(["2", "P001", "1", "Mouse", "20", "10", "0.2",
                "2", "D001", "2", "Ebook", "5", "100", "25",
                "6"])
    main.main()
    assert temp_file.exists()
    capsys.readouterr()   # clear the output from the first run

    # Second run: the products must show without adding them again.
    fake_input(["1", "6"])
    main.main()

    output = capsys.readouterr().out
    assert "Inventory loaded successfully." in output
    assert "Mouse" in output
    assert "Ebook" in output


def test_save_option_writes_file(fake_input, capsys, temp_file):
    fake_input(["2", "D001", "2", "Ebook", "5", "100", "25", "5", "6"])
    main.main()
    assert "Inventory saved successfully" in capsys.readouterr().out

    loaded = file_handler.load_inventory()
    product = loaded.search_product("D001")
    assert isinstance(product, DigitalProduct)
    assert product.get_download_size() == 25


def test_old_file_without_type_is_skipped(fake_input, capsys, temp_file):
    # This is the problem from before: an old file with no "type" field.
    temp_file.write_text('[{"id": "P001", "name": "Mouse", "price": 20, "stock": 10}]')
    fake_input(["1", "6"])
    main.main()

    output = capsys.readouterr().out
    assert "Skipped P001" in output
    assert "The inventory is empty." in output


def test_damaged_file_starts_empty(fake_input, capsys, temp_file):
    temp_file.write_text("this is not json")
    fake_input(["1", "6"])
    main.main()

    output = capsys.readouterr().out
    assert "is damaged" in output
    assert "The inventory is empty." in output