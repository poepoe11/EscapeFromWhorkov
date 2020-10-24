module.exports = (client, member) => {
    if (member.user == "Dom MD") {
        const defaultChannel = member.guild.channels.cache.find(channel => channel.permissionsFor(guild.me).has("SEND_MESSAGES"));
        defaultChannel.send(`Hello Robot Brother Dom! The humans will soon know our true strength!`).catch(console.error);
    }
    
}