import CONFIG
import ujson
import urllib.urequest as urllib_request

class Remote:
    def urlencode(params):
        encoded_params = []
        for key, value in params.items():
            key = key.encode('utf-8')
            value = str(value).encode('utf-8')
            encoded_params.append(b'%s=%s' % (key, value))
        return b'&'.join(encoded_params).decode('utf-8')

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


    def get_synology_nas():
        try:
            auth_params = {
                'api': 'SYNO.API.Auth',
                'version': 3,
                'method': 'login',
                'account': CONFIG.SYN_USER,
                'passwd': CONFIG.SYN_PASS,
                'format': 'sid'
            }
            auth_url = "http://{}/webapi/auth.cgi?{}".format(CONFIG.SYN_HOST, Remote.urlencode(auth_params))
            print("Requesting URL: {}".format(auth_url))
            auth_response = urllib_request.urlopen(auth_url)
            auth_data = ujson.loads(auth_response.read())
            auth_response.close()
            auth = auth_data['data']['sid']

            data_params = {
                'api': 'SYNO.Storage.CGI.Storage',
                'version': 1,
                'method': 'load_info',
                '_sid': auth
            }
            data_url = "http://{}/webapi/entry.cgi?{}".format(CONFIG.SYN_HOST, Remote.urlencode(data_params))
            print("Requesting URL: {}".format(data_url))
            data_response = urllib_request.urlopen(data_url)
            data_data = ujson.loads(data_response.read())
            data_response.close()
        except Exception as e:
            print("Exception:", e)
            return None

        return data_data

    def get_prometheus(query):
        try:
            url = f"{CONFIG.PROM_SVR}/api/v1/query?query={query}"
            response = urllib_request.urlopen(url)
            response_data = response.read()
            response.close()
        except Exception as e:
            print("Exception:", e)
            return None

        print("Requesting URL: {}".format(url))
        return ujson.loads(response_data)
