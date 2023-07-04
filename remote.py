import requests


class Remote():
	def get_pihole(host, key):
		try:
			response = requests.get(f"http://{host}/admin/api.php", {
				'auth': key,
				'summary': ''
			})
			response.raise_for_status()
		except requests.HTTPError:
			return None
		except Exception:
			return None

		return response.json()

	def get_linode(instance, token):
		# https://www.linode.com/docs/api/linode-instances/#linode-statistics-view
		try:
			response = requests.get(f"https://api.linode.com/v4/linode/instances/{instance}/stats", headers={
				"Authorization": f"Bearer {token}",
				"Content-Type": "application/json"
			})
			response.raise_for_status()
		except requests.HTTPError:
			return None
		except Exception:
			return None

		return response.json()

	def get_synology_nas(server, user, password):
		try:
			auth_response = requests.get(f"http://{server}/webapi/auth.cgi", {
				'api': 'SYNO.API.Auth',
				'version': 2,
				'method': 'login',
				'account': user,
				'passwd': password,
				'format': 'sid'
			})
			auth_response.raise_for_status()
			auth = auth_response.json()['data']['sid']

			data_response = requests.get(f"http://{server}/webapi/entry.cgi", {
				'api': 'SYNO.Storage.CGI.Storage',
				'version': 1,
				'method': 'load_info',
				'_sid': auth
			})
			data_response.raise_for_status()
		except requests.HTTPError:
			return None
		except Exception:
			return None

		return data_response.json()
