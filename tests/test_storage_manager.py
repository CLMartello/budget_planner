from services.storage_manager import StorageManager
import pytest

def test_save_and_load(tmp_path):
    test_file = tmp_path / "accounts.json"
    storage = StorageManager(test_file)

    data = {
        "Personal": {
            "name": "Personal",
            "transactions": [],
            "logs": []
        }
    }

    storage.save(data)
    restored_data = storage.load()

    assert restored_data == data

def test_load_invalid_json(tmp_path):
    test_file = tmp_path / "accounts.json"
    test_file.write_text("{invalid json")

    storage = StorageManager(test_file)

    with pytest.raises(
        ValueError,
        match="Storage file contains invalid JSON"
    ):
        storage.load()

def test_load_requires_dictionary(tmp_path):
    test_file = tmp_path / "accounts.json"
    test_file.write_text("[]")

    storage = StorageManager(test_file)

    with pytest.raises(
        ValueError,
        match="Storage file must contain a JSON object."
    ):
        storage.load()


def test_load_missing_file_returns_empty_dictionary(tmp_path):
	test_file = tmp_path / "missing.json"
	storage = StorageManager(test_file)

	assert storage.load() == {}

def test_load_handles_os_error(tmp_path, monkeypatch):
	test_file = tmp_path / "accounts.json"
	test_file.write_text("{}")
	storage = StorageManager(test_file)

	def raise_os_error(*args, **kwargs):
		raise OSError("Permission denied")

	monkeypatch.setattr(
		"builtins.open",
		raise_os_error
	)

	with pytest.raises(
		OSError,
		match="Unable to read storage file"
	):
		storage.load()

def test_save_handles_os_error(tmp_path, monkeypatch):
	test_file = tmp_path / "accounts.json"
	storage = StorageManager(test_file)

	def raise_os_error(*args, **kwargs):
		raise OSError("Permission denied")

	monkeypatch.setattr(
		"builtins.open",
		raise_os_error
	)

	with pytest.raises(
		OSError,
		match="Unable to write storage file"
	):
		storage.save({})
