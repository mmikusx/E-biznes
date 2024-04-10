import React, { useContext } from 'react';
import { CartContext } from '../CartContext';

function Cart() {
    const [cartItems, , removeFromCart] = useContext(CartContext);

    const totalCost = cartItems.reduce((total, item) => total + item.product.price * item.quantity, 0);

    return (
        <div>
            <h1>Koszyk</h1>
            <ul>
                {cartItems.map((item, index) => (
                    <li key={index}>
                        {item.product.name} - ${item.product.price} x {item.quantity} = ${item.product.price * item.quantity}
                        <button onClick={() => removeFromCart(item.product)}>Usuń z koszyka</button>
                    </li>
                ))}
            </ul>
            <h2>Całkowity koszt: ${totalCost}</h2>
        </div>
    );
}

export default Cart;