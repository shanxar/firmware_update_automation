import argparse
from pathlib import Path
import requests

from redfish_client.client import RedfishClient
from settings.logger_config import setup_logger

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="OpenBMC Redfish firmware update automation"
    )

    parser.add_argument("--host", required=True, help="BMC base URL")
    parser.add_argument("--username", required=True, help="BMC username")
    parser.add_argument("--password", required=True, help="BMC password")
    parser.add_argument("--firmware", required=True, help="Firmware image path")

    return parser.parse_args()


def main():
    args = parse_arguments()
    logger=setup_logger()
    firmware_path = Path(args.firmware)

    # Step 1: Validate firmware file
    if not firmware_path.is_file():
        raise SystemExit(f"ERROR: Firmware file not found: {firmware_path}")

    if firmware_path.stat().st_size == 0:
        raise SystemExit(f"ERROR: Firmware file is empty: {firmware_path}")

    print(f"Firmware file validated: {firmware_path}")
    print(f"File size: {firmware_path.stat().st_size} bytes")

    # Step 2: Create Redfish client
    client = RedfishClient(
        host=args.host,
        username=args.username,
        password=args.password,
        verify_tls=False,  # Isolated QEMU lab only
    )

    try:
        # Step 3: Check Redfish connectivity
        service_root = client.get("")
        logger.debug(service_root)
        logger.info(" Redfish connection successful.")
    
    except requests.RequestException as exc:
        raise SystemExit(f"ERROR: Redfish request failed: {exc}") from exc
        """print(
            "Redfish version:",
            service_root.get("RedfishVersion", "Unknown"),
            )

        # Step 4: Inspect UpdateService
        update_service = client.get_update_service()

        print("\nUpdateService retrieved successfully.")

        for key, value in update_service.items():
            print(f"{key}: {value}")

        # Step 5: Upload firmware
        print("\nStarting firmware upload...")

        response = client.upload_firmware(
            firmware_path=firmware_path,
            uri=FIRMWARE_UPDATE_URI,
        )

        print("Firmware upload request completed.")
        print("HTTP status:", response.status_code)
        print("Response:", response.text)

    except requests.RequestException as exc:
        raise SystemExit(f"ERROR: Redfish request failed: {exc}") from exc

    finally:
        client.session.close()"""

if __name__ == "__main__":
    main()