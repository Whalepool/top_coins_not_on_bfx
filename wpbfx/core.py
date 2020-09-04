#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from pprint import pprint



class WpBFX():

	__name__ = 'WpBFX'
	_base_url = "https://api-pub.bitfinex.com/v2/"
	_debug = False 


	# Tickers
	def get_tickers(self):

		response = self._request('get_tickers', 'tickers?symbols=ALL')
		return response

	# Config
	def map_curr_sym(self):
		"""
		Maps symbols to their API symbols (e.g. BAB -> BCH)
		"""
		response = self._request('map_curr_sym', 'conf/pub:map:currency:sym')
		return response

	def map_sym_verbose(self):
		"""
		Maps symbols to their verbose friendly names (e.g. BNT -> Bancor)
		"""
		response = self._request('map_sym_verbose', 'conf/pub:map:currency:label')
		return response



	def __init__(self, debug=False):
		self._debug = debug


	def _log(self, out):
		if self._debug == True:
			if type(out) == str:
				print(out)
			else:
				pprint(out)


	def _request(self, funcname, endpoint, params={}):

		url = self._base_url+endpoint

		self._log('Requesting: {}'.format(url))

		response = requests.get(url, params=params).text
		data = json.loads(response)

		if 'error' in data: 
			self._handle_api_error( funcname, url, params, response )

		self._log(data)

		return data



	def _handle_api_error(self, funcname, url, params={}, response={} ):

		out = '\u001b[38;5;196m ---------------------------------------------------------- \033[0m \n'
		out += '\u001b[38;5;196m ----- {} ERROR ------------ {} ERROR ------- \033[0m \n'.format(self.__name__, self.__name__)
		out += '\u001b[38;5;109m  {} \033[0m \n'.format(eval("self."+funcname).__doc__)
		out += '\u001b[38;5;83m  Function name: {} \033[0m \n'.format(funcname)
		out += '\u001b[38;5;83m  URL: {} \033[0m \n'.format(url)
		out += '\u001b[38;5;83m  Params: {} \033[0m \n'.format(str(params))
		out += '\u001b[38;5;226m  Response: {} \033[0m \n'.format(str(response))
		out += '\u001b[38;5;196m ---------------------------------------------------------- \033[0m \n'

		print( out )

