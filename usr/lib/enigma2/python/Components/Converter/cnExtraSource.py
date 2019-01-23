#######################################################################
#
#    Converter for Enigma2
#    Coded by shamann (c)2012
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Components.Converter.Converter import Converter
from Components.Element import cached
from time import localtime, strftime
from Tools.HardwareInfo import HardwareInfo
from Components.config import config

class cnExtraSource(Converter, object):
	SNRNUM = 0
	AGCNUM = 1
	BERNUM = 2
	STEP = 3
	SNRTEXT = 4
	AGCTEXT = 5
	LOCK = 6
	SLOT_NUMBER = 7
	SECHAND = 8
	MINHAND = 9
	HOURHAND = 10	
	SNRDB = 11
	SNRANALOG = 12
	SNRAGCOLED = 13
	SNRAGCTXT = 14
	SNRDB2 = 15
    	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "SnrNum":
			self.type = self.SNRNUM	
		elif type == "AgcNum":
			self.type = self.AGCNUM	
		elif type == "BerNum":
			self.type = self.BERNUM
		elif type == "Step":
			self.type = self.STEP
		elif type == "SnrText":
			self.type = self.SNRTEXT
		elif type == "SnrdB":
			self.type = self.SNRDB
		elif type == "SnrdB2":
			self.type = self.SNRDB2
		elif type == "AgcText":
			self.type = self.AGCTEXT
		elif type == "NUMBER":
			self.type = self.SLOT_NUMBER
		elif type == "secHand":
			self.type = self.SECHAND
		elif type == "minHand":
			self.type = self.MINHAND
		elif type == "hourHand":
			self.type = self.HOURHAND
		elif type == "SnrAnalog":
			self.type = self.SNRANALOG
		elif type == "SnrAgcOled":
			self.type = self.SNRAGCOLED
		elif type == "SnrAgcTxt":
			self.type = self.SNRAGCTXT
		else:
			self.type = self.LOCK

	@cached
	def getText(self):
		assert self.type not in (self.LOCK, self.SLOT_NUMBER), "error"
		percent = None
		ret = "S:--"
		if self.type == self.SNRAGCOLED or self.type == self.SNRAGCTXT:
			percent = self.source.snr
			if percent is not None:
				if self.getBase():
					if HardwareInfo().get_device_name() == 'dm7020hd':
						percent = abs(65536 - percent)
					else:
						percent = self.getPercent(percent)
				ret = "S:%d" % (percent * 100 / 65536)				
			percent = None
			percent = self.source.agc
			if percent is not None:
				if HardwareInfo().get_device_name() == 'dm800se':
					percent = min((percent*10), 65536)
				elif HardwareInfo().get_device_name() == 'dm7020hd':
					percent = abs(65536 - percent)
				tmp = "%s/%d" % (ret, (percent * 100 / 65536))
			else:
				tmp = "%s/--" % ret					
			if self.type == self.SNRAGCTXT:
				tmp = tmp.replace("S:", "Q/S: ")
			return tmp
		elif self.type == self.SNRTEXT:
			percent = self.source.snr
			if percent is not None:
				if self.getBase():
					if HardwareInfo().get_device_name() == 'dm7020hd':
						percent = abs(65536 - percent)
					else:
						percent = self.getPercent(percent)
		elif self.type in (self.SNRDB,self.SNRDB2):
			percent = "0.00"
			if self.source.snr_db is not None:
				percent = "%3.02f" % (self.source.snr_db / 100.0)
			elif self.source.snr is not None:
				percent = '%3.01f' % (0.32 * (self.source.snr * 100 / 65536.0) / 2)
			if self.type == self.SNRDB2:
				return percent + " dB"
			return percent
		elif self.type == self.AGCTEXT:
			percent = self.source.agc
			if HardwareInfo().get_device_name() == 'dm800se' and percent is not None:
				percent = min((percent*10), 65536)
			elif percent is not None and HardwareInfo().get_device_name() == 'dm7020hd':
				percent = abs(65536 - percent)
		if percent is None:
			return "N/A"
		return "%d %%" % (percent * 100 / 65536)

	text = property(getText)

	@cached
	def getValue(self):	
		if self.type == self.SNRNUM:
			count = self.source.snr		
			if count is None:
				return 0	
			if self.getBase():
				if HardwareInfo().get_device_name() == 'dm7020hd':
					count = abs(65536 - count)
				else:
					count = self.getPercent(count)
			return (count * 100 / 65536)
		elif self.type == self.SNRANALOG:
			count = self.source.snr		
			if count is None:
				return 45	
			if self.getBase():
				if HardwareInfo().get_device_name() == 'dm7020hd':
					count = abs(65536 - count)
				else:
					count = self.getPercent(count)
			if count < 32767:
				return ((count * 15 / 32768) + 45)
			else:
				count -= 32768
				return (count * 15 / 32768)
		elif self.type == self.AGCNUM:
			count = self.source.agc			
			if HardwareInfo().get_device_name() == 'dm800se' and count is not None:
				count = min((count*10), 65536)
			elif count is not None and HardwareInfo().get_device_name() == 'dm7020hd':
				count = abs(65536 - count)
			if count is None:
				return 0						
			return (count * 100 / 65536)
		elif self.type == self.BERNUM:
			count = self.source.ber		
			if count is not None:
				return count
			return 319999
		elif self.type == self.STEP:
			time = self.source.time
			if time is None:
				return 0
			t = localtime(time)
			c = t.tm_sec			
			if c < 10:
				return c
			elif c < 20:
				return (c - 10)
			elif c < 30:
				return (c - 20)
			elif c < 40:
				return (c - 30)
			elif c < 50:
				return (c - 40)
			return (c - 50)
		elif self.type == self.SECHAND:
			time = self.source.time
			if time is None:
				return 0
			t = localtime(time)
			c = t.tm_sec
			return c
		elif self.type == self.MINHAND:
			time = self.source.time
			if time is None:
				return 0
			t = localtime(time)
			c = t.tm_min
			return c			
		elif self.type == self.HOURHAND:
			time = self.source.time
			if time is None:
				return 0
			t = localtime(time)
			c = t.tm_hour
			m = t.tm_min
			if c > 11:
				c = c - 12
			val = (c * 5) + (m / 12)
			return val
		return 0

	range = 100
	value = property(getValue)

	def getBase(self):
		ret = False
		try:
			ret = config.plugins.setupGlass16.par70.value 
		except: pass
		return ret	

	def getPercent(self, percent): # correction for USB DVB-T tuners
		tmp = percent*256
		if tmp < 65536:
			percent = min(tmp, 65536)
		return percent			
