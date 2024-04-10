import React, { useState, createContext, useEffect } from 'react';

export const CartContext = createContext();

export const CartProvider = (props) => {
    const [cartItems, setCartItems] = useState([]);
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch('http://localhost:3001/products')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('Error fetching products:', error));
    }, []);

    const removeFromCart = (product) => {
        const productInCart = cartItems.find(item => item.product.id === product.id);
        if (productInCart.quantity > 1) {
            setCartItems(cartItems.map(item =>
                item.product.id === product.id
                    ? { ...item, quantity: item.quantity - 1 }
                    : item
            ));
        } else {
            setCartItems(cartItems.filter(item => item.product.id !== product.id));
        }
    };

    return (
        <CartContext.Provider value={[cartItems, setCartItems, removeFromCart, products, setProducts]}>
            {props.children}
        </CartContext.Provider>
    );
};