import ntplib
import time
import decimal
import arrow

decimal.getcontext().prec = 20

c = ntplib.NTPClient()

# server = 'time.cloudflare.com'
server = 'clock.stdtime.gov.tw'
# server = 'pool.ntp.org'

response = c.request(server, version=3)
print('tx_time: {}'.format(response.tx_time))
print('type tx_time: {}'.format(type(response.tx_time)))
print('decimal tx_time: {}'.format(decimal.Decimal(response.tx_time)))

print('tx_timestamp: {}'.format(response.tx_timestamp))
print('type tx_timestamp: {}'.format(type(response.tx_timestamp)))
print('decimal tx_timestamp: {}'.format(decimal.Decimal(response.tx_timestamp)))

print('ctime: {}'.format(time.ctime(response.tx_time)))
print('gmtime: {}'.format(time.gmtime(response.tx_time)))
print('localtime: {}'.format(time.localtime(response.tx_time)))

print('leap: {}'.format(ntplib.leap_to_text(response.leap)))
print('mode: {}'.format(ntplib.mode_to_text(response.mode)))
print('stratum: {}'.format(ntplib.stratum_to_text(response.stratum)))
print('ref id: {}'.format(ntplib.ref_id_to_text(response.ref_id, response.stratum)))

print('arrow lib')
print('arrow {}'.format(arrow.get(response.tx_time)))
