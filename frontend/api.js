const API_URL = '/';

const api = {
    getToken: () => localStorage.getItem('token'),
    
    setToken: (token) => localStorage.setItem('token', token),
    
    clearToken: () => localStorage.removeItem('token'),

    async request(endpoint, options = {}) {
        const url = `${API_URL}${endpoint.startsWith('/') ? endpoint.slice(1) : endpoint}`;
        const token = this.getToken();
        
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // Handle URL encoded form data (like OAuth2 password flow)
        let body = options.body;
        if (options.isForm) {
            headers['Content-Type'] = 'application/x-www-form-urlencoded';
            body = new URLSearchParams(options.body).toString();
        } else if (body && typeof body === 'object') {
            body = JSON.stringify(body);
        }

        try {
            const response = await fetch(url, { ...options, headers, body });
            
            if (response.status === 204) return null;
            
            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                let errorMessage = 'An error occurred';
                if (data.detail) {
                    errorMessage = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
                }
                throw new Error(errorMessage);
            }
            
            return data;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    },

    // Auth
    login(email, password) {
        return this.request('auth/login', {
            method: 'POST',
            isForm: true,
            body: { username: email, password }
        });
    },

    signup(email, password) {
        return this.request('auth/signup', {
            method: 'POST',
            body: { email, password }
        });
    },

    getProfile() {
        return this.request('auth/profile');
    },

    // Products
    getProducts() {
        return this.request('products/');
    },

    getProduct(id) {
        return this.request(`products/${id}`);
    },

    // Cart
    getCart() {
        return this.request('cart/');
    },

    addToCart(product_id, quantity = 1) {
        return this.request('cart/', {
            method: 'POST',
            body: { product_id, quantity }
        });
    },

    removeFromCart(cart_id) {
        return this.request(`cart/${cart_id}`, {
            method: 'DELETE'
        });
    },

    // Orders
    getOrders() {
        return this.request('orders/');
    },

    createOrder() {
        return this.request('orders/', {
            method: 'POST',
            body: {}
        });
    },

    payOrder(order_id) {
        return this.request('orders/pay', {
            method: 'POST',
            body: { order_id, success: true }
        });
    }
};

window.api = api;
