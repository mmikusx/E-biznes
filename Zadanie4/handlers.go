package main

import (
	"fmt"
	"github.com/labstack/echo/v4"
	"net/http"
)

func getProducts(c echo.Context) error {
	var products []Product
	result := db.Find(&products)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.JSON(http.StatusOK, products)
}

func getProduct(c echo.Context) error {
	id := c.Param("id")
	var product Product
	result := db.First(&product, "id = ?", id)
	if result.Error != nil {
		return c.JSON(http.StatusNotFound, nil)
	}
	return c.JSON(http.StatusOK, product)
}

func createProduct(c echo.Context) error {
	product := Product{}
	if err := c.Bind(&product); err != nil {
		return err
	}
	result := db.Create(&product)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.JSON(http.StatusCreated, product)
}

func updateProduct(c echo.Context) error {
	id := c.Param("id")
	product := Product{}
	if err := c.Bind(&product); err != nil {
		return err
	}
	result := db.Model(&Product{}).Where("id = ?", id).Updates(product)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.JSON(http.StatusOK, product)
}

func deleteProduct(c echo.Context) error {
	id := c.Param("id")
	result := db.Delete(&Product{}, id)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.NoContent(http.StatusNoContent)
}

func createCart(c echo.Context) error {
	cart := Cart{}
	if err := c.Bind(&cart); err != nil {
		return err
	}

	if len(cart.Products) == 0 {
		return c.JSON(http.StatusBadRequest, "No products in the request")
	}

	for i, product := range cart.Products {
		if db.First(&Product{}, "id = ?", product.ID).Error != nil {
			return c.JSON(http.StatusBadRequest, "Product with id "+product.ID+" does not exist")
		}
		cart.Products[i] = product
	}

	result := db.Create(&cart)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.JSON(http.StatusCreated, cart)
}

func getCart(c echo.Context) error {
	id := c.Param("id")
	var cart Cart
	result := db.Preload("Products").First(&cart, "id = ?", id)
	if result.Error != nil {
		fmt.Println("Error getting cart:", result.Error)
		return c.JSON(http.StatusNotFound, nil)
	}
	return c.JSON(http.StatusOK, cart)
}

func updateCart(c echo.Context) error {
	id := c.Param("id")
	cart := Cart{}
	if err := c.Bind(&cart); err != nil {
		return err
	}
	result := db.Model(&Cart{}).Where("id = ?", id).Updates(cart)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.JSON(http.StatusOK, cart)
}

func deleteCart(c echo.Context) error {
	id := c.Param("id")
	result := db.Delete(&Cart{}, id)
	if result.Error != nil {
		return c.JSON(http.StatusInternalServerError, result.Error)
	}
	return c.NoContent(http.StatusNoContent)
}
