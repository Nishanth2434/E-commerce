document.addEventListener('DOMContentLoaded', () => {
    // Hero Carousel
    const slides = document.querySelectorAll('.carousel-slide');
    if (slides.length > 0) {
        let currentSlide = 0;
        setInterval(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }, 3000);
    }
    
    // Add to cart from product lists
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn:not([onclick])');
    
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = btn.getAttribute('data-product-id');
            
            fetch('/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('cart-badge').textContent = data.cart_count;
                    showToast(data.message);
                } else if (data.status === 'error' && data.message === 'Invalid request') {
                    window.location.href = '/accounts/login/';
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(err => {
                showToast('An error occurred.', 'error');
            });
        });
    });
});

// Update Cart Quantity
function updateCart(itemId, action) {
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            item_id: itemId,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById(`qty-${itemId}`).textContent = data.quantity;
            document.getElementById(`subtotal-${itemId}`).textContent = '₹' + data.subtotal.toFixed(2);
            updateCartTotals(data.cart_count, data.cart_total);
        }
    });
}

// Remove from Cart
function removeFromCart(itemId) {
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            item_id: itemId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const itemElement = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
            if (itemElement) {
                // Remove the hr tag following the item as well
                const nextSibling = itemElement.nextElementSibling;
                if(nextSibling && nextSibling.tagName === 'HR') {
                    nextSibling.remove();
                }
                itemElement.remove();
            }
            updateCartTotals(data.cart_count, data.cart_total);
            document.getElementById('cart-badge').textContent = data.cart_count;
            
            if (data.cart_count === 0) {
                window.location.reload(); // Reload to show empty cart message
            }
        }
    });
}

function updateCartTotals(count, total) {
    const bottomCount = document.getElementById('cart-count-bottom');
    const bottomTotal = document.getElementById('cart-total-bottom');
    const sidebarCount = document.getElementById('cart-count-sidebar');
    const sidebarTotal = document.getElementById('cart-total-sidebar');
    
    if (bottomCount) bottomCount.textContent = count;
    if (bottomTotal) bottomTotal.textContent = '₹' + total.toFixed(2);
    if (sidebarCount) sidebarCount.textContent = count;
    if (sidebarTotal) sidebarTotal.textContent = '₹' + total.toFixed(2);
}

// Toast Notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Trigger reflow
    toast.offsetHeight;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}
