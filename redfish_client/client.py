import requests

from settings.config import *


class RedfishClient:

    def __init__(self, host, username, password, verify_tls=VERIFY_TLS):
        self.host = host.rstrip("/")
        self.verify_tls = verify_tls
        print(f"VVVVVVVVVVV:{verify_tls}")
        self.session = requests.Session()
        self.session.auth = (username, password)

    def get(self, endpoint=""):
        url = f"{self.host}{REDFISH_ROOT}/{endpoint.lstrip('/')}"

        response = self.session.get(
            url,
            verify=self.verify_tls,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        return response.json()

    def get_update_service(self):
        return self.get("UpdateService")

    def upload_firmware(self, firmware_path, uri):
        if not uri:
            raise ValueError("Firmware upload URI is not configured")

        if not uri.startswith("/"):
            raise ValueError("Upload URI must start with '/'")

        url = f"{self.host}{uri}"

        print(f"Uploading firmware to: {url}")

        with open(firmware_path, "rb") as firmware_file:
            response = self.session.post(
                url,
                data=firmware_file,
                headers={
                    "Content-Type": "application/octet-stream"
                },
                verify=self.verify_tls,
            )

        response.raise_for_status()

        print(f"Upload HTTP status: {response.status_code}")
        return response


if __name__ == "__main__":
    client_here=RedfishClient("https://127.0.0.1:2443","root","0penBmc" )
    print(client_here.get())