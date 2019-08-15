#Imports
import discord
from discord.ext import commands
import asyncio
import json

class tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
        self.required_permissions = discord.Embed(
            title = "Missing Permissions",
            description = "I am missing some permissions, make sure to give me access to all of [these](https://github.com/xPolar/WumpusMod#required-permissions) permissions!",
            color = 0xFF2B2B
        )


    #On guild join set up ticket stuff
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role = discord.utils.get(guild.roles, name = "Хелпер")
        if role == None:
            role = await guild.create_role(name = "Замучен")
        ticketcategory = discord.utils.get(guild.categories, name = "Хелпер")
        if ticketcategory == None:
            category_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                self.bot.user: discord.PermissionOverwrite(read_messages = True),
                supporter: discord.PermissionOverwrite(read_messages = True)
            }
            ticketcategory = await guild.create_category(name = "Тикеты", overwrites = category_overwrites)

    #Ticket
    @commands.command()
    async def ticket(self, ctx, *, reason = None):
        prefix = '!'
        try:
            supporter = discord.utils.get(ctx.guild.roles, name = "Хелпер")
            if supporter == None:
                supporter = await ctx.guild.create_role(name = "Хелпер")
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                ctx.author: discord.PermissionOverwrite(read_messages = True),
                self.bot.user: discord.PermissionOverwrite(read_messages = True),
                supporter: discord.PermissionOverwrite(read_messages = True),
            }
            ticketcategory = discord.utils.get(ctx.guild.categories, name = "Тикеты")
            if ticketcategory == None:
                category_overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                    self.bot.user: discord.PermissionOverwrite(read_messages = True),
                    supporter: discord.PermissionOverwrite(read_messages = True)
                }
                ticketcategory = await ctx.guild.create_category(name = "Тикеты", overwrites = category_overwrites)
            ticketname = f"{ctx.message.author.id}"
            ticketalreadymade = discord.utils.get(ctx.guild.text_channels, name = ticketname)
            if ticketalreadymade != None:
                alreadymade = discord.Embed(
                    title = "Ошибка",
                    description = "Вы уже создали тикет.",
                    color = self.errorcolor
                )
                await ctx.send(embed = alreadymade)
            else:
                if reason == None:
                    tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - Причина не указана"
                    if ctx.message.author.nick == None:
                        tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - Причина не указана"
                    else:
                        tickettitle = f"{ctx.message.author.nick}#{ctx.author.discriminator} - Причина не указана"
                else:
                    if ctx.message.author.nick == None:
                        tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - {reason}"
                    else:
                        tickettitle = f"{ctx.message.author.nick}#{ctx.author.discriminator} - {reason}"
                ticketchannel = await ctx.guild.create_text_channel(ticketname, overwrites = overwrites, category = ticketcategory, topic = tickettitle)
                creating = discord.Embed(
                title = "Тикет",
                description = "Создаем ваш тикет.",
                color = self.blurple
                )
                msg = await ctx.send(embed = creating)
                await asyncio.sleep(3)
                created = discord.Embed(
                title = "Тикет",
                description = "Ваш тикет успешно создан.",
                color = self.blurple
                )
                await msg.edit(embed = created)
                ticketchannelmsg = discord.Embed(
                title = "Тикет",
                description = f"Привет {ctx.author.mention}, это твой тикет! Закрой тикет с помощью команды ``{prefix}close``, добавь пользователя в тикет командой ``{prefix}adduser @пользователь``, и удали пользователя командой ``{prefix}rmuser @пользователь``.",
                color = self.blurple
                )
                await ticketchannel.send(embed = ticketchannelmsg)
                await ticketchannel.send("@here", delete_after = 0.1)
        except:
            await ctx.send(embed = self.required_permissions)

    #Close
    @commands.command()
    async def close(self, ctx):
        try:
            supporter = discord.utils.get(ctx.guild.roles, name = "Хелпер")
            if supporter == None:
                supporter = await ctx.guild.create_role(name = "Хелпер")
            ticketcategory = discord.utils.get(ctx.guild.categories, name = "Тикеты")
            if ctx.channel.category_id == ticketcategory.id:
                if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                    await ctx.channel.delete()
                else:
                    notyourticket = discord.Embed(
                     title = "Ошибка",
                     description = "У вас нет прав что бы закрыть этот тикет!",
                     color = self.errorcolor
                    )
                    await ctx.send(embed = notyourticket)
        except:
            await ctx.send(embed = self.required_permissions)

    #Add user
    @commands.command()
    async def adduser(self, ctx, *, member : discord.Member = None):
        try:
            if member != None:
                supporter = discord.utils.get(ctx.guild.roles, name = "Хелпер")
                if supporter == None:
                    supporter = await ctx.guild.create_role(name = "Хелпер")
                ticketcategory = discord.utils.get(ctx.guild.categories, name = "Тикеты")
                if ctx.channel.category_id == ticketcategory.id:
                    if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                        if member in ctx.channel.members:
                            alreadyin = discord.Embed(
                                title = "Ошибка",
                                description = "Вы уже добавили этого пользователя.",
                                color = self.errorcolor
                            )
                            await ctx.send(embed = alreadyin)
                        else:
                            await ctx.channel.set_permissions(member, read_messages = True, send_messages = True)
                            successadd = discord.Embed(
                                title="Тикет",
                                description = f"{member.mention}  был добавлен в этот тикет!",
                                color = self.blurple
                            )
                            mentionadded = await ctx.send(member.mention)
                            await mentionadded.delete()
                            await ctx.send(embed = successadd)
                    else:
                        notyourticket = discord.Embed(
                        title="Ошибка",
                        description="У вас нет прав на закрытие этого тикета.",
                        color = self.errorcolor
                        )
                        await ctx.send(embed = notyourticket)
            else:
                specify = discord.Embed(
                    title="Ошибка",
                    description="Укажите пользователя!",
                    color = self.errorcolor
                )
                await ctx.send(embed=specify)
                return
        except:
            await ctx.send(embed = self.required_permissions)

    #Remove user
    @commands.command(aliases = ["rmuser"])
    async def removeuser(self, ctx, *, member : discord.Member = None):
        try:
            if member != None:
                supporter = discord.utils.get(ctx.guild.roles, name = "Хелпер")
                if supporter == None:
                    supporter = await ctx.guild.create_role(name = "Хелпер")
                ticketcategory = discord.utils.get(ctx.guild.categories, name="Tickets")
                if ctx.channel.category_id == ticketcategory.id:
                    if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                        if member not in ctx.channel.members:
                            alreadyin = discord.Embed(
                                title = "Ошибка",
                                description = "Данного пользователя нет в тикете.",
                                color = self.errorcolor
                            )
                            await ctx.send(embed = alreadyin)
                        if supporter in member.roles:
                            embed = discord.Embed(
                                title = "Ошибка",
                                description = "Вы не можете удалить Хелпера из тикета.",
                                color = self.errorcolor
                            )
                        else:
                            await ctx.channel.set_permissions(member, read_messages = False, send_messages = False)
                            successadd = discord.Embed(
                                title = "Тикет",
                                description = f"{member.mention} удален из тикета!",
                                color = self.blurple
                            )
                            mentionadded = await ctx.send(member.mention)
                            await mentionadded.delete()
                            await ctx.send(embed=successadd)
                    else:
                        notyourticket = discord.Embed(
                            title = "Ошибка",
                            description = "Это не твой тикет!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed=notyourticket)
            else:
                specify = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя!",
                    color = self.errorcolor
                )
                await ctx.send(embed=specify)
                return
        except:
            await ctx.send(embed = self.required_permissions)



def setup(bot):
    bot.add_cog(tickets(bot))
