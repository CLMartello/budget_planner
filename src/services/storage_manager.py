
import json
from pathlib import Path

class StorageManager:
	def __init__(self, filepath="data/accounts.json"):
		self.filepath = Path(filepath)

	def save(self, data: dict):
		self.filepath.parent.mkdir(parents=True, exist_ok=True)
		with open(self.filepath, "w") as f:
			json.dump(data, f, indent=4)

	def load(self) -> dict:
		if not self.filepath.exists():
			return {}
		with open(self.filepath) as f:
			return json.load(f)

