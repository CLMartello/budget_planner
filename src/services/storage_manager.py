
import json
from pathlib import Path

class StorageManager:
	def __init__(self, filepath="data/accounts.json"):
		self.filepath = Path(filepath)

	def save(self, data: dict):
		try:
			self.filepath.parent.mkdir(
				parents=True,
				exist_ok=True
			)
		
			with open(self.filepath, "w") as f:
				json.dump(data, f, indent=4)

		except OSError as error:
			raise OSError(
				f"Unable to write storage file: {self.filepath}"
			) from error

	def load(self) -> dict:
		if not self.filepath.exists():
			return {}

		try:
			with open(self.filepath) as f:
				data = json.load(f)
		except json.JSONDecodeError as error:
			raise ValueError(
				"Storage file contains invalid JSON."
			) from error
		except OSError as error:
			raise OSError(
				f"Unable to read storage file: {self.filepath}"
			) from error

		if not isinstance(data, dict):
			raise ValueError(
				"Storage file must contain a JSON object."
			)

		return data