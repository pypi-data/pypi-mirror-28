
from django.db import models
from django.contrib.auth.models import User

#用户扩展
class UserPlus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    chinese_name = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

#访问日志
class AccessLog(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    user_name = models.CharField(max_length=100)
    path = models.CharField(max_length=500, blank=True, null=True)
    method = models.CharField(max_length=10)
    start_time_stamp = models.BigIntegerField(blank=True, null=True)
    end_time_stamp = models.BigIntegerField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    error_stack = models.TextField(blank=True, null=True)

# class ConstStatistics:
#     TIME = 'time'
#     CPU = 'cpu'
#     MEM = 'mem'
#     MEM_PERCENT = 'percent'
#     MEM_USED = 'used'
#     MEM_TOTAL = 'total'
#     MEM_SWAP_PERCENT = 'swap_percent'
#     MEM_SWAP_USED = 'swap_used'
#     MEM_SWAP_TOTAL = 'swap_total'
#     IO = 'io'
#     IO_READ = 'read'
#     IO_WRITE = 'write'
#     NET_IO = 'net_io'
#     NET_IO_SEND = 'send'
#     NET_IO_RECV = 'recv'

#硬件性能
class Hardware(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    cpu_percent = models.SmallIntegerField(blank=True, null=True)
    mem_percent = models.SmallIntegerField(blank=True, null=True)
    mem_used = models.IntegerField(blank=True, null=True)
    mem_total = models.IntegerField(blank=True, null=True)
    mem_swap_percent = models.SmallIntegerField(blank=True, null=True)
    mem_swap_used = models.IntegerField(blank=True, null=True)
    mem_swap_total = models.IntegerField(blank=True, null=True)
    io_read = models.FloatField(blank=True, null=True)
    io_write = models.FloatField(blank=True, null=True)
    net_io_send = models.FloatField(blank=True, null=True)
    net_io_recv = models.FloatField(blank=True, null=True)
