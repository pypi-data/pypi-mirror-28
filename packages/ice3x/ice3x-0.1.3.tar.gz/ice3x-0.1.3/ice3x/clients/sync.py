import json
import hmac
import urllib
import requests
import datetime
import hashlib

from typing import List, Dict
from ice3x.clients.abc import IceCubedClientABC
from ice3x.decorators import add_nonce, requires_authentication



class IceCubedSyncClient(IceCubedClientABC):
    @property
    def _has_auth_details(self) -> bool:
        """Internal helper function which checks that an API key and secret have been provided"""
        return all([self.secret is not None, self.api_key is not None])

    def _get_post_headers(self, signature: str) -> Dict:
        """"""
        return {
            'Key': self.api_key,
            'Sign': signature
        }

    def sign(self, params: Dict) -> str:
        """Sign a dict of query params for private API calls

        Args:
            params: A dict of query params

        Returns:
            A sha512 signed payload
        """
        query = urllib.parse.urlencode(params)
        signature = hmac.new(self.secret.encode(), query.encode(), hashlib.sha512)
        
        return signature.hexdigest()
    
    def __init__(self, api_key: str=None, secret: str=None) -> None:
        """Instantiate the client

        Args:
            api_key: An ICE3X public API key
            secret: An ICE3X private API key
        """
        self.session = requests.Session()
                
        self.api_key = api_key
        self.secret = secret

        # Set the default session request headers
        self.session.headers['user-agent'] = 'Mozilla/4.0 (compatible; Ice3x Python client)'

    def get_public_trade_info(self, trade_id: int, **params: Dict) -> Dict:
        """Fetch public info relating to a specified trade

        Args:
            trade_id: A valid trade id

        Returns:
            Data relating to the specified trade id
        """
        url = f'{self.BASE_URL}/trade/info'
        
        params.update({'trade_id': trade_id})
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
            
    def get_public_trade_list(self, **params: Dict) -> Dict:
        """Fetch a public facing list of trades

        Returns:
            A list of public trade data
        """
        url = f'{self.BASE_URL}/trade/list'

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_market_depth(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/stats/marketdepth'

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
        
    def get_pair_info(self, pair_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/pair/info'

        params.update({'pair_id': pair_id})
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_pair_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/pair/list'

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_currency_info(self, currency_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/currency/info'
    
        params.update({'currency_id': currency_id})
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_currency_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/currency/list'
    
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_orderbook_info(self, pair_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/orderbook/info'
    
        params.update({'pair_id': pair_id})
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_market_depth_full(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/stats/marketdepthfull'

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    def get_market_depth_bt_cav(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/stats/marketdepthbtcav'

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_invoice_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/invoice/list'
            
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_invoice_info(self, invoice_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/invoice/info'
        
        params.update({'invoice_id': invoice_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_invoice_pdf(self, invoice_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/invoice/pdf'
        
        params.update({'invoice_id': invoice_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def cancel_order(self, order_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/order/cancel'
        
        params.update({'order_id': order_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def create_order(self, pair_id: int, amount: float, otype: str, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/order/new'
        
        params.update(
            {
                'pair_id': pair_id,
                'amount': amount,
                'type': otype
            }
        )

        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_order_info(self, order_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/order/info'
        
        params.update({'order_id': order_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_order_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/order/list'
        
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_transaction_info(self, transaction_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/transaction/info'
        
        params.update({'transaction_id': transaction_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_transaction_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/transaction/list'
        
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_trade_info(self, trade_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/trade/info'
        
        params.update({'trade_id': trade_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_trade_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/trade/list'

        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_balance_list(self, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/balance/list'

        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()
    
    @add_nonce
    @requires_authentication
    def get_balance_info(self, currency_id: int, **params: Dict) -> Dict:
        """"""
        url = f'{self.BASE_URL}/balance/info'

        params.update({'currency_id': currency_id})
        signature = self.sign(params)
        headers = self._get_post_headers(signature)
        
        resp = self.session.post(url, params=params, headers=headers)
        resp.raise_for_status()
        
        return resp.json()