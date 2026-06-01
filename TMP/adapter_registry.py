from typing import Dict, Type, Optional
from src.adapters.interfaces.security_actions import SecurityActions

class AdapterRegistry:
    """适配器注册器 - 动态管理所有产品适配器"""
    
    _adapters: Dict[str, Type[SecurityActions]] = {}
    _instances: Dict[str, SecurityActions] = {}
    
    @classmethod
    def register(cls, product_type: str, product_name: str, adapter_class: Type[SecurityActions]):
        """注册适配器类"""
        key = f"{product_type}:{product_name}"
        cls._adapters[key] = adapter_class
        print(f"📦 注册适配器: {key}")
    
    @classmethod
    def get(cls, product_type: str, product_name: str, config: dict = None) -> Optional[SecurityActions]:
        """获取适配器实例（单例模式）"""
        key = f"{product_type}:{product_name}"
        
        if key not in cls._instances:
            adapter_class = cls._adapters.get(key)
            if adapter_class:
                cls._instances[key] = adapter_class(config or {})
        
        return cls._instances.get(key)
    
    @classmethod
    def list_all(cls) -> Dict[str, Type[SecurityActions]]:
        return cls._adapters.copy()