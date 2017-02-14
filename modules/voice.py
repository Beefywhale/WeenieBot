import discord
import asyncio
import json

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

class Voice():
	def __init__(self, client):
		self.volume_set = 0.1
		self.queue = asyncio.Queue()
		self.event = asyncio.Event()
		self.loop = client.loop
		self.play_task = client.loop.create_task(self.player_task())

	async def player_task(self):
		while True:
			self.event.clear()
			self.player = await self.queue.get()
			self.player.start()
			await self.event.wait()

	async def volume(self, message, client):
		try:
			self.volume_set = float(message.content.replace(client.pfix + 'volume ', ''))
			self.player.volume = self.volume_set
			await client.send_message(message.channel, 'Set Volume to {}'.format(message.content.replace(client.pfix + 'volume ', '')))
		except:
			await client.send_message(message.channel, 'Could not set the volume!')

	async def play(self, message, client):
		if message.author.voice_channel != None:
			try:
				await client.join_voice_channel(message.author.voice_channel)
			except:
				pass
			voice = client.voice_client_in(message.server)
			r_play = message.content.replace(client.pfix + 'play ', '')
			await client.send_message(message.channel, "Getting Song...")
			self.new_player = await voice.create_ytdl_player(r_play, ytdl_options={'quiet':True,'default_search':'auto'}, after=lambda: self.loop.call_soon_threadsafe(self.event.set))
			self.new_player.volume = float(self.volume_set)
			if self.new_player.duration >= 7200:
				await client.send_message(message.channel, 'Video is too long! :scream:')
			else:
				await self.queue.put(self.new_player)
				await client.send_message(message.channel, message.author.mention + ' Added **{}** to the queue!'.format(self.new_player.title))
		elif message.author.voice_channel == None:
			await client.send_message(message.channel, message.author.mention + ' you aren\'t in a voice channel!!')
            
	async def playing(self, message, client):
		await client.send_message(message.channel, 'Now Playing: ' + self.player.title)
    
	async def stop(self, message, client):
		if client.is_voice_connected(message.server):
			voice = client.voice_client_in(message.server)
			if self.player.is_playing():
				self.player.stop()
		else:
			await client.send_message(message.channel, 'Bot isn\'t in any voice channels')

	async def pause(self, message, client):
		if client.is_voice_connected(message.server):
			if self.player.is_playing():
				self.player.pause()
    
	async def disconnect(self, message, client):
		if client.is_voice_connected(message.server):
			voice = client.voice_client_in(message.server)
			await voice.disconnect()
		else:
			await client.send_message(message.channel, 'Bot isn\'t in any voice channels')

	async def mresume(self, message, client):
		if client.is_voice_connected(message.server):
			self.player.resume()

	async def join(self, message, client):
		channel_to_join= message.content.replace(client.pfix + 'join ', '')
		print(channel_to_join)
		try:
			joining_channel = message.server.get_channel(client.voiceMap[channel_to_join])
			await client.join_voice_channel(joining_channel)
		except:
			await client.send_message(message.channel, 'Error couldn\'t join {} did you specify the right channel? is it a voice channel? '.format(channel_to_join))
