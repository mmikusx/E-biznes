package main

import (
	"github.com/labstack/echo/v4"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	_ "net/http"
)

type Product struct {
	gorm.Model
	ID    string  `gorm:"primaryKey" json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

type Cart struct {
	gorm.Model
	ID       string    `gorm:"primaryKey" json:"id"`
	Products []Product `gorm:"many2many:cart_products;" json:"products"`
}

var db *gorm.DB

func main() {
	var err error
	db, err = gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	db.AutoMigrate(&Product{}, &Cart{})

	e := echo.New()

	e.GET("/products", getProducts)
	e.GET("/products/:id", getProduct)
	e.POST("/products", createProduct)
	e.PUT("/products/:id", updateProduct)
	e.DELETE("/products/:id", deleteProduct)

	e.POST("/carts", createCart)
	e.GET("/carts/:id", getCart)
	e.PUT("/carts/:id", updateCart)
	e.DELETE("/carts/:id", deleteCart)

	e.Start(":8080")
}
