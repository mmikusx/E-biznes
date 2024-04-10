import React, { useEffect, useState, useContext } from 'react';
import { CartContext } from '../CartContext';

function Products() {
    const [products, setProducts] = useState([]);
    const [newProduct, setNewProduct] = useState({ name: '', price: '' });
    const [cartItems, setCartItems] = useContext(CartContext);

    useEffect(() => {
        fetch('http://localhost:3001/products')
            .then(response => response.json())
            .then(data => setProducts(data))
            .catch(error => console.error('Error fetching products:', error));
    }, []);

    const handleInputChange = (event) => {
        setNewProduct({ ...newProduct, [event.target.name]: event.target.value });
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:3001/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newProduct)
        })
            .then(response => response.json())
            .then(data => {
                setProducts(data);
                setNewProduct({ name: '', price: '' });
            })
            .catch(error => console.error('Error adding product:', error));
    };

    const addToCart = (product) => {
        const productInCart = cartItems.find(item => item.product.id === product.id);
        if (productInCart) {
            setCartItems(cartItems.map(item =>
                item.product.id === product.id
                    ? { ...item, quantity: item.quantity + 1 }
                    : item
            ));
        } else {
            setCartItems([...cartItems, { product, quantity: 1 }]);
        }
    };

    return (
        <div>
            <h1>Produkty</h1>
            <ul>
                {products.map(product => (
                    <li key={product.id}>
                        {product.name} - ${product.price}
                        <button onClick={() => addToCart(product)}>Dodaj do koszyka</button>
                    </li>
                ))}
            </ul>
            <form onSubmit={handleFormSubmit}>
                <input type="text" name="name" value={newProduct.name} onChange={handleInputChange}
                       placeholder="Nazwa produktu" required/>
                <input type="number" name="price" value={newProduct.price} onChange={handleInputChange}
                       placeholder="Cena produktu" required/>
                <button type="submit">Dodaj produkt</button>
            </form>
        </div>
    );
}

export default Products;