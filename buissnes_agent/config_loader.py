import os
import sys
import yaml
import logging
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ConfigLoader")

class Config:
    """Singleton przechowujący konfigurację aplikacji."""
    _instance = None
    _data: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Ładuje konfigurację: default.yaml + {profile}.yaml + ENV overrides."""

        # 1. Określenie ścieżek
        base_dir = os.path.dirname(os.path.abspath(__file__))  # buissnes_agent/
        project_root = os.path.dirname(base_dir)  # root projektu
        config_dir = os.path.join(project_root, "config")

        profile = os.getenv("APP_PROFILE", "default")
        logger.info(f"Ładowanie konfiguracji dla profilu: {profile}")

        # 2. Ładowanie DEFAULT
        default_path = os.path.join(config_dir, "default.yaml")
        self._data = self._load_yaml(default_path)

        # 3. Ładowanie PROFILE specific (nadpisanie)
        if profile != "default":
            profile_path = os.path.join(config_dir, f"{profile}.yaml")
            profile_data = self._load_yaml(profile_path)
            self._merge_dicts(self._data, profile_data)

        # 4. Nadpisanie ze zmiennych środowiskowych (opcjonalne, dla Docker/K8s)
        # Przykład: APP_VECTOR_DB__COLLECTION_NAME nadpisuje vector_db.collection_name
        self._apply_env_overrides()

        logger.info("Konfiguracja załadowana pomyślnie.")

    def _load_yaml(self, path: str) -> Dict:
        if not os.path.exists(path):
            logger.warning(f"Plik konfiguracyjny nie istnieje: {path}")
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Błąd parsowania YAML {path}: {e}")
            return {}

    def _merge_dicts(self, base: Dict, override: Dict):
        """Rekurencyjne łączenie słowników."""
        for k, v in override.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                self._merge_dicts(base[k], v)
            else:
                base[k] = v

    def _apply_env_overrides(self):
        """
        Umożliwia nadpisywanie dowolnego klucza przez ENV.
        Konwencja: APP__SECTION__KEY (podwójne podkreślenie to separator)
        """
        prefix = "APP__"
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                # Usuwamy prefix i dzielimy po __
                keys = env_key[len(prefix):].lower().split("__")

                # Nawigujemy w głąb słownika
                target = self._data
                for k in keys[:-1]:
                    if k not in target:
                        target[k] = {}
                    target = target[k]

                # Ustawiamy wartość
                target[keys[-1]] = env_val
                logger.debug(f"Nadpisano z ENV: {keys} = {env_val}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Pobiera wartość z konfiguracji używając notacji kropkowej.
        Np. config.get("vector_db.collection_name")
        """
        keys = key_path.split(".")
        val = self._data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val


# Globalna instancja
settings = Config()