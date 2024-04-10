const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;

let products = [
    { id: 1, name: 'Product 1', price: 10 },
    { id: 2, name: 'Product 2', price: 20 }
];

app.use(express.json());

app.get('/products', (req, res) => {
    res.json(products);
});

app.post('/products', (req, res) => {
    const newProduct = { id: products.length + 1, ...req.body };
    products.push(newProduct);
    res.json(products);
});

app.post('/payments', (req, res) => {
    console.log(req.body);
    res.status(200).send('Płatność zakończona pomyślnie!');
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});