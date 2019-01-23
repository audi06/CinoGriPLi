# -*- coding: utf-8 -*-

from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache
from Renderer import Renderer
from time import localtime

class cnNextEvent(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.text=""
		self.__epgQuery = eEPGCache.getInstance().lookupEvent
	GUI_WIDGET = eLabel
	
	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
	
	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			if self.instance:
				self.instance.hide()
		else:
			if self.instance:
				self.text=""
				if self.source.info is not None and self.source.service:
					Nextevent = self.__epgQuery(['BDT', (self.source.service.toString(), 1, -1)])
					if Nextevent and len(Nextevent) and len(Nextevent[0])==3:
						t0 = localtime(Nextevent[0][0])
						t1 = localtime(Nextevent[0][0] + Nextevent[0][1])
						self.text = _("   Next:.  %02d:%02d - %02d:%02d  (%d min)\n%s") % (t0[3],t0[4],t1[3],t1[4],(Nextevent[0][1]/60), Nextevent[0][2])
				self.instance.show()

	def postWidgetCreate(self, instance):
		instance.hide()
