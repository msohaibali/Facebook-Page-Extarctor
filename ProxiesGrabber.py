import requests


class ProxiesGrabber:
    @staticmethod
    def build_proxies_list(proxies_list: list) -> list:
        parsed_proxies_list = list()
        for single_item in proxies_list:
            proxy_dict = {
                "http": "http://{USERNAME}:{PASSWORD}@{IP}:{PORT}/".format(
                    USERNAME=single_item.get("username"),
                    PASSWORD=single_item.get("password"),
                    IP=single_item.get("proxy_address"),
                    PORT=single_item.get("port"),
                )
            }
            parsed_proxies_list.append(proxy_dict)

        return parsed_proxies_list

    @staticmethod
    def get_proxies_list(
        token: str,
        proxies_url: str,
    ) -> list:
        headers = {"Authorization": "Token " + token}

        proxies_response = requests.get(
            proxies_url,
            headers=headers,
        )

        if proxies_response.ok:
            proxies_response = proxies_response.json()
            results = proxies_response.get("results")
            proxies_list = ProxiesGrabber.build_proxies_list(results)
            return proxies_list

        else:
            print("[-]  Issue in Proxies Request")
            return []
