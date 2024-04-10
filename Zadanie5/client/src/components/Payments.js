import React, { useState, useContext } from 'react';
import { CartContext } from '../CartContext';

function Payments() {
    const [status, setStatus] = useState('nieopłacone');
    const [cartItems, , , products] = useContext(CartContext);

    const handlePayment = () => {
        fetch('http://localhost:3001/payments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cartItems, products })
        })
            .then(response => response.text())
            .then(data => setStatus(data))
            .catch(error => console.error('Error processing payment:', error));
    };

    return (
        <div>
            <h1>Płatności</h1>
            <button onClick={handlePayment}>Zapłać teraz</button>
            <p>Status: {status}</p>
        </div>
    );
}

export default Payments;