import React from 'react';
import './App.css';
import Products from './components/Products';
import Payments from './components/Payments';
import Cart from './components/Cart';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { CartProvider } from './CartContext';

function App() {
    return (
        <CartProvider>
            <Router>
                <div className="App">
                    <header className="App-header">
                        <h1>Sklep Online</h1>
                        <nav>
                            <ul>
                                <li><Link to="/">Produkty</Link></li>
                                <li><Link to="/payments">Płatności</Link></li>
                                <li><Link to="/cart">Koszyk</Link></li>
                            </ul>
                        </nav>
                    </header>
                    <Routes>
                        <Route path="/" element={<Products />} />
                        <Route path="/payments" element={<Payments />} />
                        <Route path="/cart" element={<Cart />} />
                    </Routes>
                </div>
            </Router>
        </CartProvider>
    );
}

export default App;