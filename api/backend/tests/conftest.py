"""
Общая конфигурация pytest.

asyncio_mode = "auto" означает, что все async-тесты запускаются автоматически
без явного декоратора @pytest.mark.asyncio (но он тоже работает).
"""
import pytest