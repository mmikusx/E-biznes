import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.entities.Activity
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

class Bot : ListenerAdapter() {
    init {
        val jda = JDABuilder.createDefault("TU JEST TOKEN ALE GIT BLOKUJE UDOSTEPNIANIE TOKENOW")
            .setActivity(Activity.listening("messages"))
            .addEventListeners(this)
            .build()

        jda.awaitReady()
    }

    override fun onMessageReceived(event: MessageReceivedEvent) {
        if (event.author.isBot) return

        val channel = event.channel
        channel.sendMessage("Hello, I'm your bot!").queue()

        val content = event.message.contentDisplay
        println("Received message: $content")
    }
}