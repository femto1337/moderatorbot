import discord
from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
        self.required_permissions = discord.Embed(
            title = "Ошибка",
            description = "У бота недостаточно прав.",
            color = 0xFF2B2B
        )

    #On guild join set up mute stuff
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role = discord.utils.get(guild.roles, name = "Замучен")
        if role == None:
            role = await guild.create_role(name = "Замучен")
        for channel in guild.text_channels:
            await channel.set_permissions(role, send_messages = False)

    #On channel create set up mute stuff
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Замучен")
        if role == None:
            role = await guild.create_role(name = "Замучен")
        await channel.set_permissions(role, send_messages = False)

    #Purge command
    @commands.command(aliases = ["clear"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = 10):
        try:
            max_purge = 500
            if amount >= 1 and amount <= max_purge:
                await ctx.channel.purge(limit = amount + 1)
                embed = discord.Embed(
                    title = "Очистка",
                    description = f"Очищено {amount} сообщений.",
                    color = self.blurple
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                if modlog == None:
                    return
                if modlog != None:
                    embed = discord.Embed(
                        title = "Очистка",
                        description = f"{amount} сообщений очистил {ctx.author.mention} в {ctx.message.channel.mention}",
                        color = self.blurple
                    )
                    await modlog.send(embed = embed)
            if amount < 1:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = f"Нельзя очистить меньше 1 соощения.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                await ctx.message.delete()
            if amount > max_purge:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = f"Нельзя удалить больше 500 сообщений.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                await ctx.message.delete()
        except:
            await ctx.send(embed = self.required_permissions)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для очистки сообщений.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    #Kick command
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                    if reason == None:
                        await member.kick(reason = f"Модератор - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nПричина: Причина не указана.")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} кикнут модератором {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{member.mention} кикнут модератором {ctx.message.author.mention} в {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        await member.kick(reason = f"Модератор - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nПричина: {reason}")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} кикнут модератором {ctx.message.author.mention} \nПричина {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{member.mention} кикнут модератором {ctx.message.author.mention} в {ctx.message.channel.mention} \nПричина: {reason}",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для кика пользователей.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Ban command
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.ban(reason = f"Модератор - {ctx.message.author.name}#{ctx.message.author.discriminator}.\Причина: Причина не указана.")
                    embed = discord.Embed(
                        title = "Блокировка",
                        description = f"{member.mention} заблокирован модератором {ctx.message.author.mention}.",
                        color = self.blurple
                    )
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Блокировка",
                            description = f"{member.mention} заблокирован модератором {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
                else:
                    await member.ban(reason = f"Модератор - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nПричина - {reason}")
                    embed = discord.Embed(
                        title = "Блокировка",
                        description = f"{member.mention} заблокирован модератором {ctx.message.author.mention} \n Причина: {reason}",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Блокировка",
                            description = f"{member.mention} заблокирован модератором {ctx.message.author.mention} в {ctx.message.channel.mention} \nПричина: {reason}",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для блокировки пользователей.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Unban command
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member : discord.User = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                banned_users = await ctx.guild.bans()
                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member.name, member.discriminator):
                        embed = discord.Embed(
                            title = "Разблокировка",
                            description = f"{user.mention} разблокирован",
                            color = self.blurple
                        )
                        await ctx.guild.unban(user)
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Разблокировка",
                                description = f"{user.mention} разблокирован модератором {ctx.message.author.mention} в {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для разблокировки пользователей.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Mute command
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                if member.id == ctx.message.author.id:
                    embed = discord.Embed(
                        title = "Ошибка",
                        description = "Нельзя замутить себя.",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed, delete_after = 5.0)
                else:
                    if reason == None:
                        role = discord.utils.get(ctx.guild.roles, name = "Замучен")
                        if role == None:
                            role = await ctx.guild.create_role(name = "Замучен")
                            for channel in ctx.guild.text_channels:
                                await channel.set_permissions(role, send_messages = False)
                        await member.add_roles(role)
                        embed = discord.Embed(
                            title = "Mute",
                            description = f"{member.mention} замучен модератором {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Mute",
                                description = f"{member.mention} замучен модератором {ctx.message.author.mention} в {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        role = discord.utils.get(ctx.guild.roles, name = "Замучен")
                        if role == None:
                            role = await ctx.guild.create_role(name = "Замучен")
                            for channel in ctx.guild.text_channels:
                                await channel.set_permissions(role, send_messages = False)
                        await member.add_roles(role)
                        embed = discord.Embed(
                            title = "Мут",
                            description = f"{member.mention} замучен модератором {ctx.message.author.mention} \nПричина: {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Mute",
                                description = f"{member.mention} замучен модератором {ctx.message.author.mention} в {ctx.message.channel.mention} \nПричина: {reason}",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для мута пользователей.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Unmute command
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member : discord.Member = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ошибка",
                    description = "Укажите пользователя.",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                role = discord.utils.get(ctx.guild.roles, name = "Muted")
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(
                        title = "Размут",
                        description = f"{member.mention} размучен модератором {ctx.message.author.mention}.",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} размучен модератором {ctx.message.author.mention} в {ctx.message.channel.mention}.",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "Ошибка",
                        description = f"{member.mention} не замучен.",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Ошибка",
                description = "У вас нет прав для мута пользователей.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(moderation(bot))
