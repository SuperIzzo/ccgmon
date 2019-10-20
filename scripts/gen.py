import json
import textwrap

from PIL import Image, ImageFilter, ImageDraw, ImageFont

class Path:
	root 		= ""
	art 		= root + "art/"
	traits_art 	= art  + "traits/"
	cards_art 	= art  + "cards/"
	sets 		= root + "json/"
	out 		= root + "out/"

#=======================================
class Color:
	transparent = (0,0,0,0)
	black = (0,0,0,255)
	white = (255,255,255,255)

#=======================================
class Style:
	def __init__(self):
		self.namefont = ImageFont.truetype("arial.ttf", 30)
		self.traitfont = ImageFont.truetype("arial.ttf", 10)
		self.statsfont = ImageFont.truetype("ariblk.ttf", 30)
		self.statslabelfont = ImageFont.truetype("arial.ttf", 20)
		self.modsfont = ImageFont.truetype("arial.ttf", 16)
		self.effectfont = ImageFont.truetype("arial.ttf", 14)
		self.flavorfont = ImageFont.truetype("ariali.ttf", 14)
		
#=======================================
class Trait:
	def __init__(self, name):
		self.name = name
				
		try:
			artpath = Path.traits_art + self.name + ".png"
			self.image = Image.open(artpath)
		except FileNotFoundError:
			self.image = Image.new("RGBA", (41,41), Color.transparent)
			draw = ImageDraw.Draw(self.image)
			draw.arc((0,0,40,40),0,360, Color.black)
			del draw
			
	def genimage(self):
		return self.image

#=======================================
class Traits:
	def __init__(self):
		traitnames = [
			"any",
			"water","fire","wind","earth","cloud", "thunder", "sand","plant","ice","lava",
			"claws","thorns","spike","beak","fangs","wings","tail","shell","scales"
		]
		
		self.traits = {}
		for name in traitnames:
			self.traits[name] = Trait(name)
		
	def gettrait(self, name):
		return self.traits.get(name)
		
	def gettraitlist(self, namelist):
		traitlist = []
		for name in namelist:
			trait = self.gettrait(name)
			if trait:
				traitlist.append(trait)
				
		return traitlist
		
	def getmodlist(self, modlist):		
		traitlist = []
		if modlist:
			for mod in modlist:
				trait = self.gettrait(mod["trait"])
				if trait:
					trait.mod = mod["mod"]
					traitlist.append(trait)
					
			return traitlist
		
g_traits = Traits()

#=======================================
class Card:
	size = (400, 576)
	
	def __init__(self, type, guid, name):
		self.type = type
		self.guid = guid
		self.name = name
		self.image = Image.new("RGBA", Card.size, Color.white)
		self.draw = ImageDraw.Draw(self.image)
		self.style = Style()
		
	def genimage(self):
		return None
	
	def save(self,fp):
		self.image.save(fp)
		
	def drawtrait(self, trait, i):
		size = 41
		spacing = 6
		maxtraits = 8
		offset = int((Card.size[0] - (size*maxtraits + spacing*(maxtraits-1)))/2)
		textoffset = 2
		textsize = self.draw.textsize(trait.name, self.style.traitfont)
		
		x = offset + (size + spacing) * i
		y = 300
		trait_layer = Image.new(self.image.mode, self.image.size, Color.transparent)
		trait_layer.paste(trait.genimage(), (x,y))
		self.image = Image.alpha_composite(self.image, trait_layer);
		self.draw = ImageDraw.Draw(self.image)
		del trait_layer
		
		textx = x+(size-textsize[0])/2
		self.draw.text((textx,y+size+textoffset), trait.name, Color.black, self.style.traitfont)
		
	def drawname(self):
		self.draw.text((20,20), self.name, Color.black, self.style.namefont)
		
	def draweffect(self, effects, flavor):
		y = 370
		textlen = 54
		
		if isinstance(effects, str):
			text = textwrap.fill(effects, textlen)
			self.draw.text((20,y), text, Color.black, self.style.effectfont)
			
		if isinstance(effects, list):
			for effect in effects:
				text = textwrap.fill(effect, textlen)
				self.draw.text((20,y), text, Color.black, self.style.effectfont)
				
				textsize = self.draw.textsize(text)
				y+=textsize[1]+14
				
		if isinstance(flavor, str):
			y+=10
			text = textwrap.fill(flavor, textlen)
			self.draw.text((20,y), text, Color.black, self.style.flavorfont)
			
	def drawart(self):
		filepath = Path.cards_art + self.guid + ".png"
		try:			
			art = Image.open(filepath,mode="r");
			self.image.paste(art)
		except FileNotFoundError:
			pass
		

#=======================================	
class MonsterCard(Card):

	def __init__(self, guid, name, hp, attack, defense, traits, effect, flavor):
		Card.__init__(self,"monster", guid, name)
		self.hp 		= hp
		self.attack 	= attack
		self.defense 	= defense
		self.traits		= g_traits.gettraitlist(traits)
		self.effects	= effect
		self.flavor		= flavor		
		self.isdrawn	= False
		
	def genimage(self):
		if not self.isdrawn:
			self.drawart()
			self.drawname()
			self.drawstats()
			self.draweffect(self.effects, self.flavor)
			
			for i in range(len(self.traits)):
				self.drawtrait(self.traits[i],i)
			self.isdrawn = True
			
		return self.image
		
	def drawstats(self):
		y = 220
		offset = 20
		self.draw.text((20,y+offset*0), "HP:  " + str(self.hp), Color.black, self.style.statsfont)
		self.draw.text((20,y+offset*1), "ATK: " + str(self.attack), Color.black, self.style.statsfont)
		self.draw.text((20,y+offset*2), "DEF: " + str(self.defense), Color.black, self.style.statsfont)	
		
	def drawstats(self):
		y = 220
		offset = 20
		
		atk_x = 60
		hp_x = 200
		def_x = 340
		
		lbl_y = 510
		stat_y = 530
		
		atktext = str(self.attack)
		deftext = str(self.defense)
		hptext = str(self.hp)
		
		atktext_size = self.draw.textsize(atktext, self.style.statsfont)		
		deftext_size = self.draw.textsize(deftext, self.style.statsfont)
		hptext_size = self.draw.textsize(hptext, self.style.statsfont)
		
		atklbl = "ATK"		
		deflbl = "DEF"
		hplbl = "HP"

		atklbl_size = self.draw.textsize(atklbl, self.style.statslabelfont)			
		deflbl_size = self.draw.textsize(deflbl, self.style.statslabelfont)
		hplbl_size = self.draw.textsize(hplbl, self.style.statslabelfont)
		
		self.draw.text((atk_x-atklbl_size[0]/2,lbl_y), atklbl, Color.black, self.style.statslabelfont)		
		self.draw.text((def_x-deflbl_size[0]/2,lbl_y), deflbl, Color.black, self.style.statslabelfont)
		self.draw.text((hp_x-hplbl_size[0]/2,lbl_y), hplbl, Color.black, self.style.statslabelfont)
		
		self.draw.text((atk_x-atktext_size[0]/2,stat_y), atktext, Color.black, self.style.statsfont)
		self.draw.text((def_x-deftext_size[0]/2,stat_y), deftext, Color.black, self.style.statsfont)
		self.draw.text((hp_x-deftext_size[0]/2,stat_y), hptext, Color.black, self.style.statsfont)
	

#=======================================
class MoveCard(Card):
	def __init__(self, guid, name, attack, defense, eattack, edefense, traits, mods, effect, flavor):
		Card.__init__(self,"move", guid, name)
		self.attack 	= attack
		self.defense 	= defense
		self.eattack 	= eattack
		self.edefense 	= edefense
		self.traits		= g_traits.gettraitlist(traits)		
		self.mods		= g_traits.getmodlist(mods)
		self.effects	= effect
		self.flavor		= flavor
		self.isdrawn	= False
		
	def genimage(self):
		if not self.isdrawn:
			self.drawart()
			self.drawname()
			self.drawstats()
			self.draweffect(self.effects, self.flavor)
			
			for i in range(len(self.traits)):
				self.drawtrait(self.traits[i],i)
			self.isdrawn = True
			
		return self.image
		
	def stattext(initial,enhance):
		text = "~"
		
		enhtext = None
		if enhance:
			if enhance >= 0:
				enhtext = "+" + str(enhance)
			else:
				enhtext = str(enhance)
			
		if initial:
			text = str(initial)
			if enhtext:
				text += " (" + enhtext + ")"
		elif enhtext:
			text = enhtext
		
		return text
		
	def modtext(mods):
		text = ""
		
		if mods:
			for i in range(min(2,len(mods))):
				mod = mods[i]
				
				if mod.mod >= 0:
					text += "+" + str(mod.mod)
				else:
					text += str(mod.mod)
				
				text += " " + mod.name + "\n"
			
		return text
		
	def drawstats(self):
		y = 220
		offset = 20
		
		atk_x = 60
		mod_x = 200
		def_x = 340
		
		lbl_y = 510
		stat_y = 530
		mod_y = 534
		
		atktext = MoveCard.stattext(self.attack, self.eattack)
		deftext = MoveCard.stattext(self.defense, self.edefense)
		modtext = MoveCard.modtext(self.mods)
		
		atktext_size = self.draw.textsize(atktext, self.style.statsfont)
		deftext_size = self.draw.textsize(deftext, self.style.statsfont)
		modtext_size = self.draw.textsize(modtext, self.style.modsfont)
		
		atklbl = "ATK"		
		deflbl = "DEF"
		modlbl = "MOD"

		atklbl_size = self.draw.textsize(atklbl, self.style.statslabelfont)			
		deflbl_size = self.draw.textsize(deflbl, self.style.statslabelfont)
		modlbl_size = self.draw.textsize(modlbl, self.style.statslabelfont)
		
		self.draw.text((atk_x-atklbl_size[0]/2,lbl_y), atklbl, Color.black, self.style.statslabelfont)		
		self.draw.text((def_x-deflbl_size[0]/2,lbl_y), deflbl, Color.black, self.style.statslabelfont)		
		
		self.draw.text((atk_x-atktext_size[0]/2,stat_y), atktext, Color.black, self.style.statsfont)
		self.draw.text((def_x-deftext_size[0]/2,stat_y), deftext, Color.black, self.style.statsfont)
		
		if self.mods:
			self.draw.text((mod_x-modlbl_size[0]/2,lbl_y), modlbl, Color.black, self.style.statslabelfont)
			self.draw.text((mod_x-modtext_size[0]/2,mod_y), modtext, Color.black, self.style.modsfont)


#=======================================
class Sheet:
	size = (4000, 4032)
	
	def __init__(self):
		self.image = Image.new("RGBA", Sheet.size, Color.white)
		self.draw = ImageDraw.Draw(self.image)
		self.cards = []
	
	def drawgrid(self):
		for y in range(7):
			self.draw.line((0,y*Card.size[1], Sheet.size[0], y*Card.size[1]), fill=Color.black)
	
		for x in range(10):
			self.draw.line((x*Card.size[0], 0, x*Card.size[0], Sheet.size[1]), fill=Color.black)

	def drawcard(self, card,x,y):
		image = card.genimage()
		self.image.paste(image, (
			x*Card.size[0], 
			y*Card.size[1],
			(x+1)*Card.size[0],
			(y+1)*Card.size[1]))
		
	def genimage(self):
		self.drawgrid()
		for y in range(7):
			for x in range(10):
				cardidx = x+y*10
				if cardidx < len(self.cards):
					self.drawcard(self.cards[cardidx], x,y)
				
		return self.image
				
	def addcard(self, card):
		self.cards.append(card)
			
	def save(self, fp):
		self.image.save(fp)

#=======================================
def createcard(carddef):
	if carddef["type"] == "monster":
		return MonsterCard(
			guid	= carddef["guid"],
			name	= carddef["name"],
			hp		= carddef["hp"],
			attack	= carddef["atk"],
			defense	= carddef["def"],
			traits	= carddef["traits"],
			effect	= carddef.get("effect"),
			flavor	= carddef.get("flavor")	
		)
	elif carddef["type"] == "move":
		return MoveCard(
			guid	= carddef["guid"],
			name	= carddef["name"],
			attack	= carddef.get("atk"),
			defense	= carddef.get("def"),
			eattack	= carddef.get("eatk"),
			edefense= carddef.get("edef"),
			traits	= carddef["traits"],
			mods    = carddef.get("mods"),
			effect	= carddef.get("effect"),
			flavor	= carddef.get("flavor")
		)

#=======================================
def loadsheet(name):
	sheet = Sheet()
	
	with open(name, "r") as read_file:
		data = json.load(read_file)
		for monster in data["monsters"]:
			card = createcard(monster)
			sheet.addcard(card)			
			
		for move in data["moves"]:
			card = createcard(move)
			sheet.addcard(card)
	
	return sheet
	

			
sheet = loadsheet(Path.sets + "set1.json")
sheet.genimage()
sheet.save(Path.out + "set1.png")
			

#input("Press Enter to continue...")



#lass Monster:
	


#Read image
#m = Image.open( 'card.png' )
#Display image
#m.show()