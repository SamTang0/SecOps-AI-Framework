from abc import ABC, abstractmethod
from typing import List

class SecurityActions(ABC):
    @abstractmethod
    def block_ip(self, ip: str, duration: int = 3600) -> bool: pass
    @abstractmethod
    def isolate_host(self, host_id: str) -> bool: pass
    @abstractmethod
    def kill_process(self, host_id: str, pid: int) -> bool: pass
    @abstractmethod
    def create_ticket(self, title: str, content: str, priority: str) -> str: pass
    @abstractmethod
    def send_notification(self, channel: str, message: str) -> bool: pass
    @abstractmethod
    def query_logs(self, query: str, time_range: str) -> List[dict]: pass
