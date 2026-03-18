// DOM Elements
const elements = {
    // Nav
    navbar: document.getElementById('navbar'),
    loginBtn: document.getElementById('loginBtn'),
    userMenu: document.getElementById('userMenu'),
    logoutBtn: document.getElementById('logoutBtn'),
    cartBtn: document.getElementById('cartBtn'),
    cartBadge: document.getElementById('cartBadge'),
    ordersBtn: document.getElementById('ordersBtn'),
    navLine: document.getElementById('navLine'),
    navProducts: document.getElementById('navProducts'),
    
    // Sections
    heroSection: document.getElementById('heroSection'),
    productsSection: document.getElementById('productsSection'),
    heroShopNowBtn: document.getElementById('heroShopNowBtn'),
    
    // Products
    productsGrid: document.getElementById('productsGrid'),
    searchInput: document.getElementById('searchInput'),
    
    // Modals
    cartModal: document.getElementById('cartModal'),
    authModal: document.getElementById('authModal'),
    ordersModal: document.getElementById('ordersModal'),
    
    // Close Buttons
    closeCartBtn: document.getElementById('closeCartBtn'),
    closeAuthBtn: document.getElementById('closeAuthBtn'),
    closeOrdersBtn: document.getElementById('closeOrdersBtn'),
    
    // Auth Form
    authForm: document.getElementById('authForm'),
    authTitle: document.getElementById('authTitle'),
    emailGroup: document.getElementById('emailGroup'),
    authSubmitBtn: document.getElementById('authSubmitBtn'),
    toggleAuthBtn: document.getElementById('toggleAuthBtn'),
    authToggleText: document.getElementById('authToggleText'),
    authError: document.getElementById('authError'),
    
    // Cart & Orders
    cartItems: document.getElementById('cartItems'),
    cartFooter: document.getElementById('cartFooter'),
    cartTotalAmount: document.getElementById('cartTotalAmount'),
    checkoutBtn: document.getElementById('checkoutBtn'),
    ordersList: document.getElementById('ordersList'),
    
    // Toasts
    toastContainer: document.getElementById('toastContainer')
};

// State
const state = {
    isLoginMode: true,
    user: null,
    products: [],
    cart: [],
    isNavigating: false
};

// Utility to show toasts
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    
    elements.toastContainer.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Format currency
const formatPrice = (price) => `$${price.toFixed(2)}`;

// Initialize Application
async function initApp() {
    setupEventListeners();
    await checkAuth();
    if (state.user) {
        updateNavbar();
        await loadProducts();
        await updateCart();
    } else {
        await loadProducts();
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Navigation
    elements.heroShopNowBtn.addEventListener('click', showProducts);
    elements.navLine.addEventListener('click', (e) => { e.preventDefault(); showHome(); });
    elements.navProducts.addEventListener('click', (e) => { e.preventDefault(); showProducts(); });
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            elements.navbar.style.background = 'rgba(15, 17, 21, 0.9)';
            elements.navbar.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        } else {
            elements.navbar.style.background = 'rgba(26, 29, 36, 0.6)';
            elements.navbar.style.boxShadow = 'none';
        }
    });

    // Modals
    elements.loginBtn.addEventListener('click', () => toggleModal(elements.authModal, true));
    elements.cartBtn.addEventListener('click', openCart);
    elements.ordersBtn.addEventListener('click', openOrders);
    
    elements.closeAuthBtn.addEventListener('click', () => toggleModal(elements.authModal, false));
    elements.closeCartBtn.addEventListener('click', () => toggleModal(elements.cartModal, false));
    elements.closeOrdersBtn.addEventListener('click', () => toggleModal(elements.ordersModal, false));
    
    // Close modal on background click
    [elements.authModal, elements.cartModal, elements.ordersModal].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) toggleModal(modal, false);
        });
    });

    // Auth
    elements.toggleAuthBtn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleAuthMode();
    });
    
    elements.authForm.addEventListener('submit', handleAuthSubmit);
    elements.logoutBtn.addEventListener('click', handleLogout);

    // Products Search
    elements.searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        renderProducts(state.products.filter(p => p.name.toLowerCase().includes(query) || p.description.toLowerCase().includes(query)));
    });

    // Cart Checkout
    elements.checkoutBtn.addEventListener('click', handleCheckout);
}

// Navigation Functions
function showHome() {
    elements.heroSection.classList.remove('hidden');
    elements.productsSection.classList.add('hidden');
    elements.navLine.classList.add('active');
    elements.navProducts.classList.remove('active');
}

function showProducts() {
    elements.heroSection.classList.add('hidden');
    elements.productsSection.classList.remove('hidden');
    elements.navLine.classList.remove('active');
    elements.navProducts.classList.add('active');
}

function toggleModal(modal, show) {
    if (show) {
        modal.classList.remove('hidden');
    } else {
        modal.classList.add('hidden');
    }
}

// Auth Functions
async function checkAuth() {
    if (api.getToken()) {
        try {
            state.user = await api.getProfile();
        } catch (e) {
            console.error("Token invalid or expired", e);
            api.clearToken();
            state.user = null;
        }
    }
}

function updateNavbar() {
    if (state.user) {
        elements.loginBtn.classList.add('hidden');
        elements.userMenu.classList.remove('hidden');
    } else {
        elements.loginBtn.classList.remove('hidden');
        elements.userMenu.classList.add('hidden');
        elements.cartBadge.innerText = '0';
    }
}

function toggleAuthMode() {
    state.isLoginMode = !state.isLoginMode;
    elements.authError.innerText = '';
    
    if (state.isLoginMode) {
        elements.authTitle.innerText = 'Welcome Back';
        elements.authSubmitBtn.innerText = 'Login';
        elements.authToggleText.innerHTML = 'Don\'t have an account? <a href="#" id="toggleAuthBtn">Sign up</a>';
    } else {
        elements.authTitle.innerText = 'Create Account';
        elements.authSubmitBtn.innerText = 'Sign Up';
        elements.authToggleText.innerHTML = 'Already have an account? <a href="#" id="toggleAuthBtn">Login</a>';
    }
    
    // Reattach listener since innerHTML replaced it
    document.getElementById('toggleAuthBtn').addEventListener('click', (e) => {
        e.preventDefault();
        toggleAuthMode();
    });
}

async function handleAuthSubmit(e) {
    e.preventDefault();
    const btn = elements.authSubmitBtn;
    const initialText = btn.innerText;
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i>';
    btn.disabled = true;
    elements.authError.innerText = '';
    
    try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (state.isLoginMode) {
            const res = await api.login(email, password);
            if (res && res.access_token) {
                api.setToken(res.access_token);
                state.user = await api.getProfile();
                showToast(`Welcome back, ${state.user.email}!`);
                toggleModal(elements.authModal, false);
                initApp(); // reload setup
            }
        } else {
            await api.signup(email, password);
            showToast('Account created successfully! Please log in.');
            toggleAuthMode(); // switch to login
        }
    } catch (err) {
        elements.authError.innerText = err.message || 'Authentication failed';
    } finally {
        btn.innerText = initialText;
        btn.disabled = false;
    }
}

function handleLogout() {
    api.clearToken();
    state.user = null;
    state.cart = [];
    updateNavbar();
    showHome();
    showToast('Logged out successfully');
}

// Product Functions
async function loadProducts() {
    try {
        elements.productsGrid.innerHTML = '<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i></div>';
        state.products = await api.getProducts();
        renderProducts(state.products);
    } catch (err) {
        elements.productsGrid.innerHTML = `<div class="error-msg">Failed to load products: ${err.message}</div>`;
    }
}

function renderProducts(productsToRender) {
    if (!productsToRender || productsToRender.length === 0) {
        elements.productsGrid.innerHTML = '<p>No products available.</p>';
        return;
    }

    elements.productsGrid.innerHTML = productsToRender.map(product => `
        <div class="product-card">
            <div class="product-image-placeholder">
                <i class="fa-solid fa-image"></i>
            </div>
            <h3 class="product-title">${product.name}</h3>
            <p class="product-desc">${product.description || 'No description available'}</p>
            <div class="product-footer">
                <span class="product-price">${formatPrice(product.price)}</span>
                <button class="btn-primary" onclick="addToCartEvent(${product.id})">
                    <i class="fa-solid fa-cart-plus"></i> Add
                </button>
            </div>
        </div>
    `).join('');
}

// Cart Functions
async function addToCartEvent(productId) {
    if (!state.user) {
        toggleModal(elements.authModal, true);
        showToast('Please login to add items to cart', 'error');
        return;
    }

    try {
        await api.addToCart(productId, 1);
        showToast('Item added to cart!');
        await updateCart();
    } catch (err) {
        showToast(`Failed to add item: ${err.message}`, 'error');
    }
}

async function updateCart() {
    if (!state.user) return;
    try {
        state.cart = await api.getCart();
        const totalItems = state.cart.reduce((acc, item) => acc + item.quantity, 0);
        elements.cartBadge.innerText = totalItems;
    } catch (e) {
        console.error("Failed to load cart", e);
    }
}

async function openCart() {
    if (!state.user) {
        toggleModal(elements.authModal, true);
        return;
    }
    
    toggleModal(elements.cartModal, true);
    elements.cartItems.innerHTML = '<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i></div>';
    
    try {
        await updateCart();
        renderCart();
    } catch (err) {
        elements.cartItems.innerHTML = `<div class="error-msg">Failed to load cart: ${err.message}</div>`;
    }
}

function renderCart() {
    if (!state.cart || state.cart.length === 0) {
        elements.cartItems.innerHTML = '<p>Your cart is empty.</p>';
        elements.cartFooter.classList.add('hidden');
        return;
    }

    let total = 0;
    
    // Map product info for rendering
    const cartHtml = state.cart.map(item => {
        const product = state.products.find(p => p.id === item.product_id);
        const name = product ? product.name : `Product #${item.product_id}`;
        const price = product ? product.price : 0;
        const itemTotal = price * item.quantity;
        total += itemTotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-img"><i class="fa-solid fa-image"></i></div>
                <div class="cart-item-details">
                    <div class="cart-item-title">${name}</div>
                    <div class="cart-item-price">${formatPrice(price)} x ${item.quantity}</div>
                </div>
                <div style="font-weight: 600;">${formatPrice(itemTotal)}</div>
                <button class="btn-danger" onclick="removeFromCartEvent(${item.id})">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `;
    }).join('');

    elements.cartItems.innerHTML = cartHtml;
    elements.cartTotalAmount.innerText = formatPrice(total);
    elements.cartFooter.classList.remove('hidden');
}

window.removeFromCartEvent = async (cartId) => {
    try {
        await api.removeFromCart(cartId);
        showToast('Item removed from cart');
        await updateCart();
        renderCart();
    } catch (err) {
        showToast('Failed to remove item', 'error');
    }
};

async function handleCheckout() {
    try {
        elements.checkoutBtn.innerText = 'Processing...';
        elements.checkoutBtn.disabled = true;
        
        // In backend, place_order reads from user's cart
        const order = await api.createOrder();
        
        // Simulate payment for the new order
        if(order && order.id) {
            await api.payOrder(order.id);
            showToast('Order placed successfully!', 'success');
            toggleModal(elements.cartModal, false);
            await updateCart();
            openOrders(); // Show orders
        }
    } catch (err) {
        showToast(`Checkout failed: ${err.message}`, 'error');
    } finally {
        elements.checkoutBtn.innerText = 'Proceed to Checkout';
        elements.checkoutBtn.disabled = false;
    }
}

// Orders Functions
async function openOrders() {
    if (!state.user) return;
    
    toggleModal(elements.ordersModal, true);
    elements.ordersList.innerHTML = '<div class="loading-spinner"><i class="fa-solid fa-circle-notch fa-spin"></i></div>';
    
    try {
        const orders = await api.getOrders();
        
        if (!orders || orders.length === 0) {
            elements.ordersList.innerHTML = '<p>You have no past orders.</p>';
            return;
        }

        elements.ordersList.innerHTML = orders.map(order => `
            <div class="order-card">
                <div class="order-header">
                    <span>Order #${order.id}</span>
                    <span>Status: ${order.status}</span>
                </div>
                <div class="order-items">
                    Overall Total:
                </div>
                <div class="order-total">${formatPrice(order.total_price)}</div>
            </div>
        `).join('');
    } catch (err) {
        elements.ordersList.innerHTML = `<div class="error-msg">Failed to load orders: ${err.message}</div>`;
    }
}

// Run boot sequence
document.addEventListener('DOMContentLoaded', initApp);
