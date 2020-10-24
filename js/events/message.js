module.exports = (client, message) => {
    // Ignore all bots
    if (message.author.bot) return;
    
    // Do not reply to comments from these users, including itself (client.user)
    blocked_users = [ client.user ]

    // Bot does not reply to itself and only when mentioned
    if (client.user.mentioned_in(message) and message.author not in blocked_users){
        logger.info("Replied to message of user '{}' in guild '{}' / channel '{}'".format(message.author, message.guild, message.channel))
        msg = get_random_quote().format(message)
        await message.channel.send(msg)
    }

    // Ignore messages not starting with the prefix (in config.json)
    if (message.content.indexOf(client.config.prefix) !== 0) return;

    // Our standard argument/command name definition.
    const args = message.content.slice(client.config.prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();

    // Grab the command data from the client.commands Enmap
    const cmd = client.commands.get(command);

    // If that command doesn't exist, silently exit and do nothing
    if (!cmd) return;

    // Run the command
    cmd.run(client, message, args);
};