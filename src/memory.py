# memory.py
import ctypes
import ctypes.wintypes
import win32process
import win32api
import win32con
import os
import json
from ctypes import wintypes

PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_ALL_ACCESS = 0x1F0FFF

class Memory:
    def __init__(self, process_name):
        self.process_name = process_name
        self.handle = None
        self.base_address = None
        self._open_process()

    def _open_process(self):
        pids = win32process.EnumProcesses()
        for pid in pids:
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
                if handle:
                    name = win32process.GetModuleFileNameEx(handle, 0)
                    if name and self.process_name.lower() in name.lower():
                        self.handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
                        if not self.handle:
                            raise Exception("Не удалось открыть процесс с полным доступом")
                        self.base_address = self._get_base_address(pid)
                        return
            except:
                continue
        raise Exception(f"Процесс {self.process_name} не найден")

    def _get_base_address(self, pid):
        return 0x400000

    def read_int(self, offset):
        if not self.handle:
            raise Exception("Процесс не открыт")
        address = self.base_address + offset
        buffer = ctypes.c_int()
        bytes_read = ctypes.c_size_t()
        if not ctypes.windll.kernel32.ReadProcessMemory(
            self.handle, ctypes.c_void_p(address),
            ctypes.byref(buffer), ctypes.sizeof(buffer),
            ctypes.byref(bytes_read)
        ):
            raise Exception("Ошибка чтения памяти")
        return buffer.value

    def write_int(self, offset, value):
        if not self.handle:
            raise Exception("Процесс не открыт")
        address = self.base_address + offset
        buffer = ctypes.c_int(value)
        bytes_written = ctypes.c_size_t()
        if not ctypes.windll.kernel32.WriteProcessMemory(
            self.handle, ctypes.c_void_p(address),
            ctypes.byref(buffer), ctypes.sizeof(buffer),
            ctypes.byref(bytes_written)
        ):
            raise Exception("Ошибка записи памяти")

    def close(self):
        if self.handle:
            ctypes.windll.kernel32.CloseHandle(self.handle)
            self.handle = None
