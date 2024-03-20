import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.entities.Activity
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

class Bot : ListenerAdapter() {
    private val categories = listOf("owoce", "warzywa", "napoje", "samochody")

    init {
        val jda = JDABuilder.createDefault("TOKEN")
            .setActivity(Activity.listening("messages"))
            .addEventListeners(this)
            .build()

        jda.awaitReady()
    }

    override fun onMessageReceived(event: MessageReceivedEvent) {
        if (event.author.isBot) return

        val channel = event.channel
        val content = event.message.contentDisplay

        if (content == "@E-biznes zadanie 3 MS bot /kategorie") {
            val categoriesString = categories.joinToString(", ")
            channel.sendMessage("Dostępne kategorie: $categoriesString").queue()
        } else {
            channel.sendMessage("Cześć! Jestem twoim botem.").queue()
        }

        println("Received message: $content")
    }
}