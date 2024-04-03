package main

import (
	"github.com/labstack/echo/v4"
	"net/http"
)

type Product struct {
	ID    string  `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

var products = []Product{
	{ID: "p1", Name: "Product 1", Price: 100.23},
	{ID: "p2", Name: "Product 2", Price: 200.23},
}

func getProducts(c echo.Context) error {
	return c.JSON(http.StatusOK, products)
}

func getProduct(c echo.Context) error {
	id := c.Param("id")

	for _, product := range products {
		if product.ID == id {
			return c.JSON(http.StatusOK, product)
		}
	}

	return c.JSON(http.StatusNotFound, nil)
}

func createProduct(c echo.Context) error {
	product := Product{}

	if err := c.Bind(&product); err != nil {
		return err
	}

	products = append(products, product)

	return c.JSON(http.StatusCreated, product)
}

func updateProduct(c echo.Context) error {
	id := c.Param("id")

	product := Product{}

	if err := c.Bind(&product); err != nil {
		return err
	}

	for i, p := range products {
		if p.ID == id {
			products[i] = product
			return c.JSON(http.StatusOK, product)
		}
	}

	return c.JSON(http.StatusNotFound, nil)
}

func deleteProduct(c echo.Context) error {
	id := c.Param("id")

	for i, product := range products {
		if product.ID == id {
			products = append(products[:i], products[i+1:]...)
			return c.NoContent(http.StatusNoContent)
		}
	}

	return c.JSON(http.StatusNotFound, nil)
}

func main() {
	e := echo.New()

	e.GET("/products", getProducts)
	e.GET("/products/:id", getProduct)
	e.POST("/products", createProduct)
	e.PUT("/products/:id", updateProduct)
	e.DELETE("/products/:id", deleteProduct)

	e.Start(":8080")
}
