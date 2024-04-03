package main

import (
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
