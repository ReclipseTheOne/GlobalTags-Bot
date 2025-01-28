import os

# Logging
from logs import GTLogger

# Discord
from bot import bot, tree
from discord import app_commands
import discord

import handling
import tags
import events


# Logic
@bot.event
async def on_ready():
    GTLogger.success(f'We have logged in as {bot.user}')
    try:
        GTLogger.debug(f"Syncing tree...")
        synced = await tree.sync()
        GTLogger.success(f"Synced {len(synced)} command(s)!")
        for command in synced:
            GTLogger.info(f"Synced command: {command.name}")
    except Exception as e:
        GTLogger.error(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    GTLogger.info(f"Received message: {message.content}")


@tree.command(
    name="create",
    description="Creates a tag with the provided name and saved message"
)
@app_commands.describe(tag_name="Tag Name", tag_message="Tag Message")
async def create(interaction: discord.Interaction, tag_name: str, tag_message: str):
    tag: dict = handling.fetchTag(tag_name)
    if ("owner_id" not in tag.keys()):
        await interaction.response.send_message(f"'{tag_name}' created successfully! <a:pop:1333844597352300564>", ephemeral=True)
        handling.handleCreateTagRequest(tags.TagSchema(
            name=tag_name, 
            message=tag_message, 
            owner=interaction.user.name,
            owner_id=str(interaction.user.id),
            key=os.environ.get('DATABASE_KEY')
            ))
    else:
        await interaction.response.send_message(f"'{tag_name}' already exists! <a:pop:1333844597352300564>", ephemeral=True)


@tree.command(
    name="delete",
    description="Deletes a tag with the provided name"
)
@app_commands.describe(tag_name="Tag Name")
async def delete(interaction: discord.Interaction, tag_name: str):
    tag: dict = handling.fetchTag(tag_name)
    if ("owner_id" not in tag.keys()):
        await interaction.response.send_message(f"'{tag_name}' does not exist! <a:pop:1333844597352300564>", ephemeral=True)
        return

    if (tag["owner_id"] != str(interaction.user.id)):
        await interaction.response.send_message(f"Tag '{tag_name}' is owned by <@{tag['owner_id']}>! <a:pop:1333844597352300564>", ephemeral=True)
        return

    await interaction.response.send_message(f"'{tag_name}' deleted successfully! <a:pop:1333844597352300564>", ephemeral=True)
    handling.handleDeleteTagRequest(tag_name, os.environ.get('DATABASE_KEY'))


@tree.command(
    name="gt",
    description="Fetches a tag with the provided name"
)
@app_commands.describe(tag_name="Tag Name")
async def fetch(interaction: discord.Interaction, tag_name: str):
    tag: dict = handling.fetchTag(tag_name)
    if ("owner_id" not in tag.keys()):
        await interaction.response.send_message(f"{tag_name} does not exist! <a:pop:1333844597352300564>", ephemeral=True)
        return

    await interaction.response.send_message(tag["message"])


@tree.command(
    name="who",
    description="Fetches the owner of a tag with the provided name"
)
@app_commands.describe(tag_name="Tag Name")
async def who(interaction: discord.Interaction, tag_name: str):
    tag: dict = handling.fetchTag(tag_name)
    if ("owner_id" not in tag.keys()):
        await interaction.response.send_message(f"{tag_name} does not exist! <a:pop:1333844597352300564>", ephemeral=True)
        return

    await interaction.response.send_message(f"{tag_name} is owned by <@{tag['owner_id']}>", ephemeral=True)

@tree.command(
    name="list",
    description="Lists all tags of a specific person"
)
@app_commands.describe(user="User ID to search for")
async def listTags(interaction: discord.Interaction, user: str):
    tags = handling.fetchTags(user)
    if (len(tags) == 0):
        await interaction.response.send_message(f"No tags found for <@{user}>", ephemeral=True)
        return

    tag_list = ""
    for tag in tags:
        tag_list += f"{tag['name']}\n"

    await interaction.response.send_message(tag_list, ephemeral=True)


# Main
def main():
    token = os.environ.get('BOT_TOKEN')
    print("Loaded Database Key: " + os.environ.get('DATABASE_KEY'))
    bot.run(token)


if __name__ == "__main__":
    main()
