from paho.mqtt.client import Client

class Publisher:

    def __init__(self, client_id, user_id, ip):
        self.client = Client(client_id=client_id, userdata=user_id)
        self.client.connect(ip)
        self.client_id = client_id
        self.user_id = user_id
        self.ip = ip

    def pushToMQ(self, topic, message):
	self.client.publish(topic, message)
