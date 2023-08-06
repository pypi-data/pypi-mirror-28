import abc

from typing import Dict


class IceCubedClientABC(abc.ABC):
    BASE_URL = 'https://ice3x.com/api/v1'
    
    @abc.abstractproperty
    def _has_auth_details(self) -> bool:
        pass

    @abc.abstractmethod
    def sign(self, params: Dict) -> str:
        pass

    @abc.abstractmethod
    def _get_post_headers(self, signature: str) -> Dict:
    	pass