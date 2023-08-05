import psutil as p
from ..time_plus import DatetimePlus
import time,threading



class ConstStatistics:
    TIME = 'time'
    CPU = 'cpu'
    MEM = 'mem'
    MEM_PERCENT = 'percent'
    MEM_USED = 'used'
    MEM_TOTAL = 'total'
    MEM_SWAP_PERCENT = 'swap_percent'
    MEM_SWAP_USED = 'swap_used'
    MEM_SWAP_TOTAL = 'swap_total'
    IO = 'io'
    IO_READ = 'read'
    IO_WRITE = 'write'
    NET_IO = 'net_io'
    NET_IO_SEND = 'send'
    NET_IO_RECV = 'recv'

class Statistics(object):
    _statistic_data = []
    _module_visitor_count = {}
    __thread_collect = None
    _send_bytes_count = 0
    _recv_bytes_count = 0

    def bytes2human(self,n):
        """
        bytes2human(10000)
        '9.8 K'
        bytes2human(100001221)
        '95.4 M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f %s' % (value, s)
        return '%.2f B' % (n)

    def __init__(self):
        self.__io_old = None
        self.__thread_collect = threading.Thread(target=self.collect_data,args=())
        self.__thread_collect.daemon = True
        self.__thread_collect.start()



    def collect_data(self):
        from ..data_models.models import Hardware
        while True:
            time.sleep(10)
            data = {}
            data[ConstStatistics.CPU] = self.__get_cpu_data()
            data[ConstStatistics.MEM] = self.__get_mem_data()
            data[ConstStatistics.NET_IO],data[ConstStatistics.IO] = self.__get_io_data()
            hardware = Hardware()
            hardware.datetime = DatetimePlus.get_now_datetime()
            hardware.cpu_percent = data[ConstStatistics.CPU]
            hardware.mem_percent = data[ConstStatistics.MEM][ConstStatistics.MEM_PERCENT]
            hardware.mem_used = data[ConstStatistics.MEM][ConstStatistics.MEM_USED]
            hardware.mem_total = data[ConstStatistics.MEM][ConstStatistics.MEM_TOTAL]
            hardware.mem_swap_percent = data[ConstStatistics.MEM][ConstStatistics.MEM_SWAP_PERCENT]
            hardware.mem_swap_used = data[ConstStatistics.MEM][ConstStatistics.MEM_SWAP_USED]
            hardware.mem_swap_total = data[ConstStatistics.MEM][ConstStatistics.MEM_SWAP_TOTAL]
            hardware.io_read = data[ConstStatistics.IO][ConstStatistics.IO_READ]
            hardware.io_write = data[ConstStatistics.IO][ConstStatistics.IO_WRITE]
            hardware.net_io_recv = data[ConstStatistics.NET_IO][ConstStatistics.NET_IO_RECV]
            hardware.net_io_send = data[ConstStatistics.NET_IO][ConstStatistics.NET_IO_SEND]
            hardware.save()


    def __get_cpu_data(self):
        '''取百分比'''
        return p.cpu_percent(1)


    def __get_mem_data(self):
        result = {}
        phymem = p.virtual_memory()
        result[ConstStatistics.MEM_PERCENT] = phymem.percent
        result[ConstStatistics.MEM_USED] = round(phymem.used / 1024 / 1024 /1024,2)
        result[ConstStatistics.MEM_TOTAL] = round(phymem.total / 1024 / 1024 /1024,2)

        phymem_swap = p.swap_memory()
        result[ConstStatistics.MEM_SWAP_PERCENT] = phymem_swap.percent
        result[ConstStatistics.MEM_SWAP_USED] = round(phymem_swap.used / 1024 / 1024 /1024,2)
        result[ConstStatistics.MEM_SWAP_TOTAL] = round(phymem_swap.total / 1024 / 1024 /1024,2)
        return result




    def __get_io_data(self):
        if self.__io_old == None:
            self.__io_old = p.disk_io_counters()
            self.__net_io_old = p.net_io_counters()

        _net_io_new = p.net_io_counters()
        _io_new = p.disk_io_counters()

        _net_io_result = {}
        _net_io_result[ConstStatistics.NET_IO_SEND] = round((_net_io_new.bytes_sent - self.__net_io_old.bytes_sent) / 1024,2)
        _net_io_result[ConstStatistics.NET_IO_RECV] = round((_net_io_new.bytes_recv - self.__net_io_old.bytes_recv) / 1024,2)

        _io_result = {}
        _io_result[ConstStatistics.IO_READ] = round((_io_new.read_bytes - self.__io_old.read_bytes) / 1024,2)
        _io_result[ConstStatistics.IO_WRITE] = round((_io_new.write_bytes - self.__io_old.write_bytes) / 1024,2)

        self.__io_old = _io_new
        self.__net_io_old = _net_io_new

        return _net_io_result,_io_result


statistics = Statistics()