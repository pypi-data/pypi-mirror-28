#!/usr/bin/python
# -*-coding:utf-8-*-

import os
import json
import urllib
import urllib2
import SimpleHTTPServer
import SocketServer
import time
import datetime
import ntplib
import commands
import logging
import socket
import threading
import signal
import sys
import fcntl
import struct
from optparse import OptionParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scapy.all import srp, Ether, ARP

LOG_FILE_PATH = '/var/log/network_opt/network_opt.log'
CONFIG_FILE_PATH = '/opt/network_opt/config.json'
logging.basicConfig(level=logging.DEBUG,
                    filename=LOG_FILE_PATH,
                    filemode='a+',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - [func:%(funcName)s] - %(levelname)s: %(message)s')

available_ips = []

# watchdog handle function
class MyHandler(FileSystemEventHandler):
  def __init__(self, lc):
    self.config = lc.config
    self.lc = lc

  def on_modified(self, event):
    src_abspath = os.path.abspath(event.src_path)

    logging.info("event_abspath = %s" % src_abspath)
    logging.info("conf_abspath = %s" % self.config)

    if src_abspath == self.config:
      logging.info("log file %s changed!" % src_abspath)
      self.lc.load()
      logging.info(self.lc.ips)


# load/save json config with a file
class Config():
  def __init__(self, configFile):
    self.configFile = configFile
    self.load()

  # add new config
  def add(self, key, values):
    addedFlag = False
    if self.configData.get(key) is not None:
      for val in values:
        if (self.configData.get(key).count(val) == 0):
          self.configData.get(key).append(val)
          addedFlag = True
    else:
      self.configData[key] = values
      addedFlag = True

    if addedFlag:
      logging.info('[add config] %s : %s have been added' % (key, values))

    return addedFlag

  # delete config
  def delete(self, key, values=[]):
    deleteFlag = False
    if self.configData.get(key) is not None:
      if len(values) == 0:
        self.configData.pop(key)
        deleteFlag = True
        logging.info('[delete config] key \'%s\' has been deleted' %key)
      else:
        for val in values:
          try:
            self.configData.get(key).remove(val)
            deleteFlag = True
            logging.info('[delete config] value \'%s\' of key \'%s\' has been deleted' % (val,key))
          except ValueError:
            logging.info('[delete config] value \'%s\' of key \'%s\' does not exists' % (val,key))
    else:
      logging.info('[delete config] \'%s\' does not exists' % key)

    return deleteFlag

  def load(self):
    with open(self.configFile, 'r') as fp:
      try:
        self.configData = json.load(fp)
      except ValueError:
        self.configData = {}
      except IOError,e:
        raise Exception('config file error',e)

  def save(self):
    with open(self.configFile, 'w') as fp:
      json.dump(self.configData,fp)

    logging.info('File %s has been saved' % self.configFile);


# network operation ping, tcp, udp(ntp), http-Get, http-Post
class network_opt():
  def __init__(self, ip):
    self.ip = ip

  # network GET http
  def get_operation(self):
    url = 'http://%s:80/' % self.ip
    req = urllib2.Request(url)

    res_data = urllib2.urlopen(req, timeout=10)
    res = res_data.read()
    logging.info("GET Operation Success")

  # network Post http
  def post_operation(self):
    data = {'a': 'aaaa', 'b': 'bbbbb'}
    data_urlencode = urllib.urlencode(data)

    requrl = 'http://%s:80/' % self.ip
    req = urllib2.Request(url=requrl, data=data_urlencode)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    logging.info("POST Operation Success")

  # network ping operation
  def ping_operation(self, timeout=1):
    def ping_operation_inner(timeout1):
      cmd = 'ping -w %d %s' % (timeout1, self.ip)
      output = commands.getstatusoutput(cmd)[0]

      if output == 0:
        logging.info("Ping Operation Success: %s" % self.ip)
      else:
        logging.info("Ping Operation Failed: %s" % self.ip)

    icmp_thread = threading.Thread(target=ping_operation_inner, args=(timeout,))
    icmp_thread.start()

  def tcp_operation(self):
    def tcp_operation_inner():
      port = 80
      tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      try:
        tcpClient.settimeout(10)
        tcpClient.connect((self.ip, int(port)))
        tcpClient.settimeout(None)

        sdata = 'Get /Test HTTP/1.1\r\nHost: %s\r\n\r\n' % self.ip
        tcpClient.send(sdata)

        sresult = tcpClient.recv(1024)
        # print "Response: \r\n%s\r\n" % sresult
        logging.info("TCP operation Success: %s" % self.ip)
        time.sleep(50)
      except Exception:
        logging.info("TCP operation Failed: %s" % self.ip)
      finally:
        tcpClient.close()

    tcp_thread = threading.Thread(target=tcp_operation_inner)
    tcp_thread.start()

  '''
  def ntp_operation(self):
      ntp_client = ntplib.NTPClient()
      response = ntp_client.request('ntp.api.bz')
      logging.info("NTP Sync Operation Success %s " % datetime.datetime.fromtimestamp(response.tx_time))
  '''

  def udp_operation(self):
    def udp_operation_inner():
      port = 9999
      udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      addr = (self.ip, int(port))

      data = (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())).encode()
      try:
        udpClient.sendto(data.encode(), addr)
        udpClient.settimeout(10)
        recvdata, addr = udpClient.recvfrom(1024)
        udpClient.settimeout(None)
        time.sleep(50)
        logging.info("UDP operation Success: %s" % self.ip)
      except Exception:
        logging.info("UDP operation Failed: %s" % self.ip)
      finally:
        udpClient.close()

    udp_thread = threading.Thread(target=udp_operation_inner)
    udp_thread.start()


# start a thread to run simple http server
def Servers():
  handler = SimpleHTTPServer.SimpleHTTPRequestHandler
  port = 80
  httpd = SocketServer.TCPServer(("", port), handler)

  httpd.serve_forever()


def UDP_Servers(local_ip):
  port = 9999
  udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udp_server.bind((local_ip, int(port)))
  while True:
    data, addr = udp_server.recvfrom(1024)
    udp_server.sendto(data.decode('utf-8').upper().encode(), addr)


# start a thread to run watchdog ,this is to monitor the change of config file
def network_watchdog(lc):
  event_handler = MyHandler(lc)
  observer = Observer()
  observer.schedule(event_handler, path="/root/conf", recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()


def quit(signum, frame):
  logging.debug('network opt stop!! pid = %d' % os.getpid())
  os.kill(os.getpid(), signal.SIGINT)
  sys.exit()


def get_if_ip(ifnames):
  local_ips = []
  logging.debug('======== get local_ips ========')
  for ifname in ifnames:
    logging.info('======== current interface: %s ========' % ifname)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ips.append(socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24]))

  logging.debug('======== get local_ips end ========')
  logging.debug('======== local_ips: %s ========' % local_ips)
  return local_ips


def get_available_ips(local_subnets):
  while True:
    global available_ips

    # get all subnet ip
    config = Config(CONFIG_FILE_PATH)
    config.load()

    subnets = local_subnets
    if config.configData.get('subnet') is not None:
      for tmpVal in config.configData.get('subnet'):
        if tmpVal.find('/') == -1:
          tmpVal = tmpVal + '/24'

        if subnets.count(tmpVal) == 0:
          subnets.append(tmpVal)

    logging.info("== [Start] to GET AVAILABLE IPS ==")

    ips = []
    for IpScan in subnets:
      try:
        ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=IpScan), timeout=2)
      except Exception as e:
        print e
      else:
        for send, rcv in ans:
          ListMACAddr = rcv.sprintf("%ARP.psrc%")
          print ListMACAddr
          if ips.count(ListMACAddr) == 0:
            ips.append(ListMACAddr)
        logging.info("====== GET IPS START ======")
        logging.info("====== SUBNET: %s" % IpScan)
        logging.info(ips)
        logging.info("====== GET IPS END ========")

    available_ips = ips

    logging.info("All available ips: %s" % available_ips)
    time.sleep(60)


def addConfig(confStr):
  """
  :param confStr: [string]
  """
  conf = confStr.split('=')
  if len(conf) <> 2:
    logging.error("[add config] Invalid paramater was given:%s" % confStr)
    return
  else:
    confKey = conf[0]
    confValues = conf[1].split(',')

  config = Config(CONFIG_FILE_PATH)
  if config.add(confKey, confValues):
    config.save()

def delConfig(confStr):
  """
  :param confStr: [string]
  """
  conf = confStr.split('=')

  if len(conf) == 1:
    config = Config(CONFIG_FILE_PATH)

    if config.delete(conf[0]):
      config.save()
  elif len(conf) == 2:
    confKey = conf[0]
    confValues = conf[1].split(',')

    config = Config(CONFIG_FILE_PATH)
    if config.delete(confKey, confValues):
      config.save()
  else:
    logging.info('[delete conf] Invalid paramater %s has been given' % confStr)

def showConfig(confStr):
  """
  :param confStr: [string]
  """

  config = Config(CONFIG_FILE_PATH)

  if confStr == 'all' or confStr == None:
    print config.configData
  elif config.configData.get(confStr) is not None:
    print config.configData.get(confStr)
  else:
    print 'Key \'%s\' does not exist in configure file' % confStr

def get_options():
  parser = OptionParser(version="%prog 1.0")

  parser.add_option("-c", "--config", dest="config",
                    help="config network operation file")

  parser.add_option("-t", "--time", dest="time",
                    help="the time interval of doing network operation")

  parser.add_option("-i", "--interface", dest="interface",
                    help="the name of the network interface")

  parser.add_option("-w", "--watchdog", dest="watchdog",
                    help="open or not open file watchdog",
                    action="store_true", default=False)

  parser.add_option("-v", "--verbose", dest="verbose",
                    help="display additional logging information",
                    action="store_true", default=False)

  parser.add_option("-a", "--add", dest="add",
                    help="Add configuration to config file.")

  parser.add_option("-d", "--delete", dest="delete",
                    help="Delete configuration from config file.")

  parser.add_option("-s", "--show", dest="show",
                    help="Show configuration of config file.")

  (options, args) = parser.parse_args()

  return options

# where begin to handle network
def network_handle(options):
  global CONFIG_FILE_PATH

  # config file path
  if (options.config):
    CONFIG_FILE_PATH = options.config

  # check the config file path
  try:
    fp = open(CONFIG_FILE_PATH)
  except Exception:
    logging.error('config file does not exist')
    print('[Error] Please specify the config file with option -c')
    return 0
  else:
    fp.close()

  # add config command
  if (options.add):
    addConfig(options.add)
    return 0

  # delete config command
  if (options.delete):
    delConfig(options.delete)
    return 0

  # show config command
  if (options.show):
    showConfig(options.show)
    return 0


  interfaces = options.interface.rstrip(",").split(",");
  logging.debug('options.interface: %s' % options.interface)
  local_ips = get_if_ip(interfaces)
  logging.info("[local_ips]: %s" % local_ips)

  server = threading.Thread(target=Servers)
  server.start()

  udp_server = threading.Thread(target=UDP_Servers, args=(local_ips[0],))
  udp_server.start()

  local_subnets = []
  for local_ip in local_ips:
    local_subnets.append(local_ip + '/24')

  available_ip_thread = threading.Thread(target=get_available_ips, args=(local_subnets,))
  available_ip_thread.start()

  '''
  lc = Config(options.config)
  lc.load()
  logging.info("lc.confg = %s" % lc.config)
  '''
  # if options.watchdog:
  #     watchdog = threading.Thread(target=network_watchdog, args=(lc,))
  #     #watchdog.setDaemon(True)
  #     watchdog.start()

  # hostname = socket.getfqdn(socket.gethostname( ))
  # hostname = socket.gethostname( )
  # local_ip = socket.gethostbyname(hostname)
  '''
  for index in range(1,255):
      internal_ip = ('.'.join(str(local_ip).split('.')[0:3])) + '.' + str(index)
      lc.ips.append(internal_ip)
  '''
  while True:
    global available_ips
    for a_ip in available_ips:
      logging.debug("--------------------------------------------")
      logging.debug("The current ip = %s" % a_ip)
      opt = network_opt(a_ip)
      try:
        opt.ping_operation(50)
      except Exception as info:
        logging.error("PING opt error message: %s" % info)
      # try:
      #     opt.get_operation()
      # except Exception as info:
      #     logging.error("HTTP GET opt error message: %s" % info)
      try:
        opt.tcp_operation()
      except Exception as info:
        logging.error("TCP error message: %s" % info)
      try:
        opt.udp_operation()
      except Exception as info:
        logging.error("UDP error message: %s" % info)
        # try:
        #     opt.ntp_operation()
        # except Exception as info:
        #     logging.error("NTP error message: %s" % info)

    time.sleep(60)

def main():
  signal.signal(signal.SIGINT, quit)
  signal.signal(signal.SIGTERM, quit)

  options = get_options()
  network_handle(options)

if __name__ == "__main__":
  main()
