import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*
import io.ktor.client.request.*
import io.ktor.http.*

suspend fun main() {
    val client = HttpClient(CIO) {
        install(JsonFeature) {
            serializer = KotlinxSerializer(kotlinx.serialization.json.Json {
                ignoreUnknownKeys = true
            })
        }
    }

    val webhookUrl = "https://discord.com/api/webhooks/1219972691826835476/A4Ei2JGctTki5Y7jQSYCNVu_OS4_anuTBuGHBK8K90bM1BJpo7G3tpCgLsSRVq5XCJo-" // Podmień na swój URL webhooka
    val message = mapOf("content" to "Hello, Discord!")

    client.post<Unit>(webhookUrl) {
        contentType(ContentType.Application.Json)
        body = message
    }

    client.close()
}