import logging
import sys

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("ETL-Process")


def main():
    logger.info("=== ROZPOCZYNAM PROCES INGESTII DANYCH (ETL) ===")

    try:
        # 1. Pobieramy instancję bazy (połączoną z Qdrant i OpenAI)
        import InitialConfig
        print("[Server] Konfiguracja ETL załadowana pomyślnie.", file=sys.stderr)
        logger.info("=== PROCES INGESTII ZAKOŃCZONY SUKCESEM ===")

    except Exception as e:
        logger.error(f"BŁĄD KRYTYCZNY PODCZAS INGESTII: {e}")
        print(f"[Server] Ostrzeżenie: Błąd podczas ładowania ETL: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()