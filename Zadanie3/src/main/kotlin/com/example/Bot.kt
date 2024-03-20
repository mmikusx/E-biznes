import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.entities.Activity
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter

data class Product(val name: String, val price: Double)

class Bot : ListenerAdapter() {
    private val categories = mapOf(
        "owoce" to listOf(Product("jabłko", 3.0), Product("banan", 2.5)),
        "warzywa" to listOf(Product("marchew", 1.5), Product("pomidor", 2.0)),
        "napoje" to listOf(Product("woda", 1.0), Product("cola", 2.5)),
        "samochody" to listOf(Product("Audi A3", 150000.0), Product("BMW X1", 200000.0))
    )

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
            val categoriesString = categories.keys.joinToString("\n- ")
            channel.sendMessage("Dostępne kategorie:\n- $categoriesString").queue()
        } else if (content.startsWith("@E-biznes zadanie 3 MS bot /kategoria:")) {
            val category = content.removePrefix("@E-biznes zadanie 3 MS bot /kategoria:").trim()
            val products = categories[category]

            if (products != null) {
                val productsString = products.joinToString("\n- ") { "${it.name} - ${it.price} zł" }
                channel.sendMessage("Produkty w kategorii $category:\n- $productsString").queue()
            } else {
                channel.sendMessage("Nie znaleziono kategorii $category").queue()
            }
        } else {
            channel.sendMessage("Cześć! Jestem twoim botem.").queue()
        }

        println("Received message: $content")
    }
}