import sys
import random
import pynotify
import subprocess
 
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
 
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
 
from autobahn.twisted.resource import WebSocketResource
 
 
class SomeServerProtocol(WebSocketServerProtocol):
	#On ouvre la connexion et apres le handshake fait automatiquement on peut envoyer et recevoir des messages.
	def onOpen(self):
		#Enregistrement du client
		self.factory.register(self)
		#On essaye de trouver une conversation pour le client
		self.factory.findPartner(self)
 
	def connectionLost(self, reason):
		#Enlever le client s'il y a une erreur de connection quel qu'elle soit
		self.factory.unregister(self)
 
	def onMessage(self, message, isBinary):
		#On envoit un message du client a ses partenaires de la liste
		self.factory.communicate(self, message, isBinary)
 
class Chat(WebSocketServerFactory):
	def __init__(self, *args, **kwargs):
		super(Chat, self).__init__(*args, **kwargs)
		self.clients = {}
 
	def register(self, client):
		#On ajoute le client a la liste des gens connectes
		self.clients[client.peer] = {"object": client, "partner": None}
 
	def unregister(self, client):
		#On retire le une personne de la liste des connections
		self.clients.pop(client.peer)
 
	def findPartner(self, client):
		#Trouvez un partenaire de chat pour un client. S'il n'y a pas de client inactif, il suffit de quitter. S'il y a un partenaire disponible, on l'affecte a notre client.
		available_partners = [c for c in self.clients if c != client.peer and not self.clients[c]["partner"]]
		if not available_partners:
			print("no partners for {} check in a moment".format(client.peer))
		else:
			partner_key = random.choice(available_partners)
			self.clients[partner_key]["partner"] = client
			self.clients[client.peer]["partner"] = self.clients[partner_key]["object"]
	
	def communicate(self, client, message, isBinary):
		#Envoie d'un messg du client aux autres membres de la liste de connections
		c = self.clients[client.peer]
		if not c["partner"]:
			c["object"].sendMessage("Sorry you dont have partner yet, check back in a minute")
		else:
			c["partner"].sendMessage(message)
 
if __name__ == "__main__":
    log.startLogging(sys.stdout)
 
    # static file server seving index.html as root
    root = File(".")
 
    factory = Chat(u"ws://127.0.0.1:8080", True)
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)
 
    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()
