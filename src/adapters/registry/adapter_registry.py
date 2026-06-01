from typing import Dict, Type, Optional

class AdapterRegistry:
    _adapters: Dict[str, Type] = {}
    @classmethod
    def register(cls, product_type: str, product_name: str, adapter_class: Type):
        cls._adapters[f"{product_type}:{product_name}"] = adapter_class
    @classmethod
    def get(cls, product_type: str, product_name: str) -> Optional[Type]:
        return cls._adapters.get(f"{product_type}:{product_name}")
