import CONFIG
import ujson
import urllib.urequest as urllib_request

class Remote:
    def get_pihole():
        try:
            url = f"http://{CONFIG.PIHOLE_URL}/admin/api.php?auth={CONFIG.PIHOLE_KEY}&summary="
            response = urllib_request.urlopen(url)
            response_data = response.read()
            response.close()
        except Exception as e:
            print("Exception:", e)
            return None

        print("Requesting URL: {}".format(url))
        return ujson.loads(response_data)
