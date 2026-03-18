def create_user_and_token(client, email="user@example.com", password="secret123"):
    signup_response = client.post(
        "/auth/signup",
        json={"email": email, "password": password},
    )
    assert signup_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_product(client, name, price, category):
    response = client.post(
        "/products/",
        json={"name": name, "price": price, "category": category},
    )
    assert response.status_code == 201
    return response.json()


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the E-commerce API"}


def test_signup_login_and_profile(client):
    headers = create_user_and_token(client, email="mani@example.com")

    profile_response = client.get("/auth/profile", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "mani@example.com"

    duplicate_signup = client.post(
        "/auth/signup",
        json={"email": "mani@example.com", "password": "secret123"},
    )
    assert duplicate_signup.status_code == 400
    assert duplicate_signup.json()["error"] == "bad_request"


def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_products_filter_search_and_pagination(client):
    create_product(client, "iPhone 15", 999.99, "electronics")
    create_product(client, "Samsung TV", 799.99, "electronics")
    create_product(client, "Wooden Chair", 149.99, "furniture")

    filtered_response = client.get("/products/?category=electronics")
    assert filtered_response.status_code == 200
    assert len(filtered_response.json()) == 2

    search_response = client.get("/products/?search=iphone")
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["name"] == "iPhone 15"

    paginated_response = client.get("/products/?page=2&limit=2")
    assert paginated_response.status_code == 200
    assert len(paginated_response.json()) == 1


def test_validation_error_for_negative_price(client):
    response = client.post(
        "/products/",
        json={"name": "Bad Product", "price": -10, "category": "electronics"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Validation error"


def test_cart_order_and_payment_flow(client):
    headers = create_user_and_token(client, email="buyer@example.com")
    product = create_product(client, "Gaming Mouse", 49.99, "electronics")

    add_to_cart = client.post(
        "/cart/",
        json={"product_id": product["id"], "quantity": 2},
        headers=headers,
    )
    assert add_to_cart.status_code == 201
    assert add_to_cart.json()["quantity"] == 2

    view_cart = client.get("/cart/", headers=headers)
    assert view_cart.status_code == 200
    assert len(view_cart.json()) == 1

    place_order = client.post("/orders/", headers=headers)
    assert place_order.status_code == 201
    assert place_order.json()["status"] == "pending"
    assert place_order.json()["total_price"] == 99.98

    order_id = place_order.json()["id"]

    cart_after_order = client.get("/cart/", headers=headers)
    assert cart_after_order.status_code == 200
    assert cart_after_order.json() == []

    payment = client.post(
        "/orders/pay",
        json={"order_id": order_id, "success": True},
        headers=headers,
    )
    assert payment.status_code == 200
    assert payment.json()["status"] == "paid"

    order_history = client.get("/orders/", headers=headers)
    assert order_history.status_code == 200
    assert len(order_history.json()) == 1
