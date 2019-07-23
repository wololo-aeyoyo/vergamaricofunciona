import discord
from threading import Thread
from discord.ext import commands
from random import randint
import aiohttp
import aiofiles
import os
from PIL import Image
from TwitterAPI import TwitterAPI
api = TwitterAPI(os.environ["betica"],os.environ["betica2"],os.environ["betica3"],os.environ["betica4"])
NUMBER_OF_TWEETS_TO_DELETE = 1
class DeleteTweet(Thread):

    def __init__(self, tweet_id, count):
        Thread.__init__(self)
        self.tweet_id = tweet_id
        self.count = count

    def run(self):
        r = api.request('statuses/destroy/:%d' % self.tweet_id)
        print(self.count if r.status_code == 200 else 'PROBLEM: ' + r.text)


class comando(commands.Cog):
	
	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	async def twitter(self,ctx,*,texto:str):
	    e=str(ctx.message.attachments[0])
	    nani=e.split()
	    link=str(nani[3])
	    nombre=str(nani[2])
	    nombre=nombre.replace("filename='","")
	    nombre=nombre[:-1]
	    link=link.replace("url='","")
	    link=link[:-2]
	    async with aiohttp.ClientSession() as session:
	        async with session.get(link) as imagen:
	            if imagen.status == 200:
	                pic = await imagen.read()
	                with open("images/{}".format(nombre), "wb") as f:
	                    f.write(pic)

	                    if nombre.endswith(".png" or ".jpg"):
		                    foo = Image.open("images/{}".format(nombre))
		                    rgb_im = foo.convert('RGB')
		                    rgb_im.thumbnail((1024, 1080), Image.ANTIALIAS)
		                    rgb_im.save("images/tumbnaila_{}".format(nombre)+".jpg",quality=95,optimize=True)
		                    file = open("images/tumbnaila_{}".format(nombre)+".jpg", 'rb')

	                    else:
	                    	file = open("images/{}".format(nombre), 'rb')

	                    data = file.read()
	                    r = api.request('media/upload', None, {'media': data})
	                    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

	                    if r.status_code == 200:
	                    	media_id = r.json()['media_id']
	                    print(media_id)
	                    r = api.request('statuses/update', {'status': texto, 'media_ids': media_id})
	                    print(r)
	                    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE: ' + r.text)
	                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	                    count=0
	                    r=api.request('statuses/user_timeline', {'count': 1})
	                    for item in r:
	                        if 'id' in item:
	                            count += 1
	                            tweet_id = item['id']
	                    embed=discord.Embed(title="[Click pa ve donde]", url="https://twitter.com/Wololo_aeyoyo/status/"+str(tweet_id), description="el mensaje autista: "+texto, color=0x031cfc)
	                    embed.set_author(name="Tu Tweet se posteo relajado en @wololo_aeyoyo", url="https://twitter.com/Wololo_aeyoyo", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTvrFytZTMQnW6cD-85691yjeNYHetZ3aXe1Ts3sYzLzptQXXx")
	                    embed.set_thumbnail(url=link)
	                    embed.set_footer(text=str(ctx.author.name)+" si tu pendejo")
	                    await ctx.send(embed=embed)


#Codigos de error

	async def cog_command_error(self,ctx,error):
	 	if isinstance(error,commands.MissingRequiredArgument):
	 		await ctx.send("Manda la vaina bien $twitter contenido del tweet y adjunta la vaina")
	 	elif isinstance(error,commands.CommandInvokeError):
	 		if len(ctx.message.attachments)==0:
	 			await ctx.send("manda la foto masturbatorio")
	 		else: await ctx.send("**Ese guevo tuyo tan bien largo uwu. Esa vaina pesa mucho**")
def setup(bot):
	bot.add_cog(comando(bot))
