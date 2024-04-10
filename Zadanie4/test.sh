#!/bin/bash

# Dodaj produkty
for i in {0..5}
do
  response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"id\":\"$i\", \"name\":\"Product $i\", \"price\":300.23}" http://localhost:8080/products)
  echo "Dodano produkt id $i"
done

# Pobierz i wyświetl produkty
response=$(curl -s -X GET http://localhost:8080/products)
echo "Znaleziono produkty: $response"

# Zaktualizuj produkt
id_to_update=1
response=$(curl -s -X PUT -H "Content-Type: application/json" -d '{"name":"Updated Product", "price":400.23}' http://localhost:8080/products/$id_to_update)
echo "Zaktualizowano produkt $id_to_update"

# Usuń produkt
id_to_delete=4
response=$(curl -s -X DELETE http://localhost:8080/products/$id_to_delete)
echo "Usunięto produkt $id_to_delete"

# Stwórz koszyk z produktami
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"id\":\"30\", \"products\":[{\"id\":\"0\"},{\"id\":\"1\"},{\"id\":\"3\"},{\"id\":\"5\"}]}" http://localhost:8080/carts)
echo $response
echo "Dodano koszyk 30"

# Pobierz i wyświetl koszyk
response=$(curl -s -X GET http://localhost:8080/carts/30)
echo "Znaleziono koszyk: $response"

# Zaktualizuj koszyk
response=$(curl -s -X PUT -H "Content-Type: application/json" -d "{\"products\":[{\"id\":\"p1\"},{\"id\":\"p2\"}]}" http://localhost:8080/carts/30)
echo "Zaktualizowano koszyk 30"