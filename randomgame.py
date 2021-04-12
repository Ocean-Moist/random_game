from yet_another_http_client import ConnectionManager, TLSConnectionManager # import my home grown rust http client (why use it? bc its cool and i need an escuse to show it off)
from abc import ABC, abstractmethod
from urllib.parse import urlparse

class http_stuff(ABC):
	@property
	@abstractmethod
	def payloads(self):
		"""Get payloads to send"""
		pass
	def __init__(
		self,
		api_base: str = "https://api.random.com",
	):
		self.api_base = api_base
		parsed = urlparse(self.api_base)
		self.api_host = parsed.hostname or "api.random.com"
		self.api_port = parsed.port or {"https": 443, "http": 80}[parsed.scheme]
		self.api_ssl = parsed.scheme == "https"

	def setup(
		self
	):	
		conns = (
			TLSConnectionManager(self.api_host, self.api_port, self.api_host)
			if self.api_ssl
			else ConnectionManager(self.api_host, self.api_port)
		)
		conns.connect(1)
		conns.send(self.payloads)

class random_1_100(http_stuff):
	@property
	def payloads(self):
		return [
			"\r\n".join(
				(
					"POST /json-rpc/4/invoke HTTP/1.1",
					"Host: api.random.org",
					"Content-Type: application/json",
					"Content-Length: ..."
					"Accept: */*",
					"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
					"",
					"""
{
	"jsonrpc": "2.0",
	"method": "generateIntegers",
	"params": {
		"apiKey": "dc256660-782e-4006-a15b-8b7767fa063f",
		"n": 1,
		"min": 1,
		"max": 100,
		"replacement": true,
		"base": 10,
		"pregeneratedRandomization": null
	},
	"id": 21246
}
					"""
				)
			).encode()
	]
random = random_1_100()
random.setup()											