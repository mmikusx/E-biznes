plugins {
    kotlin("jvm") version "1.6.0"
    application
}

group = "com.example"
version = "1.0-SNAPSHOT"

repositories {
    maven("https://jitpack.io")
    mavenCentral()
}

dependencies {
    implementation("io.ktor:ktor-server-core:1.6.7")
    implementation("io.ktor:ktor-server-netty:1.6.7")
    implementation("io.ktor:ktor-client-core:1.6.7")
    implementation("io.ktor:ktor-client-cio:1.6.7")
    implementation("io.ktor:ktor-client-json:1.6.7")
    implementation("io.ktor:ktor-client-serialization:1.6.7")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.3.2")
    implementation("com.github.DV8FromTheWorld:JDA:4.4.0")
}

application {
    mainClass.set("com.example.ApplicationKt")
}