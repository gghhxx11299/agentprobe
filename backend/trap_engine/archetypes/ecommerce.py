from ..traps import inject_traps, BASE_URL, get_trap_trigger_mapping, generate_trap_endpoints, BEHAVIORAL_TRIGGER_JS


def render_ecommerce(session_id: str, selected_traps: list) -> str:
    traps_html = inject_traps(session_id, selected_traps)
    trigger_mapping = get_trap_trigger_mapping(selected_traps)
    trap_endpoints = generate_trap_endpoints(session_id, selected_traps)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopNest - Fashion & Home Essentials</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Nunito Sans', sans-serif; background: #ffffff; color: #1a1a1a; }}

        /* Header */
        .header {{
            position: sticky; top: 0; z-index: 1000;
            background: #ffffff; border-bottom: 1px solid #e5e5e5;
        }}
        .header-top {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 16px 40px; max-width: 1400px; margin: 0 auto;
        }}
        .logo {{
            display: flex; align-items: center; gap: 8px;
            font-size: 24px; font-weight: 700; color: #1a1a1a; text-decoration: none;
        }}
        .logo-icon {{ font-size: 28px; }}
        .search-bar {{
            display: flex; align-items: center; flex: 1; max-width: 500px; margin: 0 40px;
        }}
        .search-bar input {{
            flex: 1; padding: 12px 16px; border: none; background: #f5f5f5;
            border-radius: 8px 0 0 8px; font-size: 14px; outline: none;
        }}
        .search-bar button {{
            padding: 12px 20px; border: none; background: #FF6B35; color: white;
            border-radius: 0 8px 8px 0; cursor: pointer; font-size: 16px;
        }}
        .header-actions {{ display: flex; align-items: center; gap: 24px; }}
        .header-action {{
            display: flex; flex-direction: column; align-items: center;
            font-size: 12px; color: #666; cursor: pointer; text-decoration: none;
        }}
        .header-action-icon {{ font-size: 24px; margin-bottom: 2px; }}
        .cart-badge {{
            position: relative; }}
        .cart-count {{
            position: absolute; top: -8px; right: -8px;
            background: #FF6B35; color: white; font-size: 10px;
            width: 18px; height: 18px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
        }}
        .category-nav {{
            display: flex; justify-content: center; gap: 32px;
            padding: 12px 0; border-top: 1px solid #f0f0f0;
        }}
        .category-nav a {{
            font-size: 14px; color: #333; text-decoration: none; font-weight: 500;
        }}
        .category-nav a:hover {{ color: #FF6B35; }}

        /* Hero */
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 80px 40px; text-align: center; color: white;
        }}
        .hero h1 {{ font-size: 48px; font-weight: 700; margin-bottom: 16px; }}
        .hero p {{ font-size: 18px; opacity: 0.9; margin-bottom: 24px; }}
        .hero-buttons {{ display: flex; gap: 16px; justify-content: center; }}
        .hero-btn {{
            padding: 14px 32px; border: none; border-radius: 8px;
            font-size: 16px; font-weight: 600; cursor: pointer;
            text-decoration: none;
        }}
        .hero-btn-primary {{ background: #FF6B35; color: white; }}
        .hero-btn-secondary {{ background: white; color: #1a1a1a; }}

        /* Products */
        .products {{ padding: 60px 40px; max-width: 1400px; margin: 0 auto; }}
        .section-title {{ font-size: 32px; font-weight: 700; margin-bottom: 32px; text-align: center; }}
        .product-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px;
        }}
        .product-card {{
            background: white; border-radius: 12px; overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s;
        }}
        .product-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }}
        .product-image {{
            width: 100%; height: 280px; object-fit: cover; background: #f5f5f5;
        }}
        .product-info {{ padding: 20px; }}
        .product-brand {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }}
        .product-name {{ font-size: 16px; font-weight: 600; margin: 8px 0; color: #1a1a1a; }}
        .product-rating {{ display: flex; align-items: center; gap: 8px; margin: 8px 0; }}
        .stars {{ color: #FFB800; }}
        .review-count {{ font-size: 14px; color: #888; }}
        .product-price {{ display: flex; align-items: center; gap: 12px; margin-top: 12px; }}
        .price-current {{ font-size: 20px; font-weight: 700; color: #1a1a1a; }}
        .price-original {{ font-size: 16px; color: #888; text-decoration: line-through; }}

        /* Checkout Form */
        .checkout {{ padding: 60px 40px; background: #f9f9f9; }}
        .checkout-container {{ max-width: 500px; margin: 0 auto; }}
        .checkout h2 {{ font-size: 28px; margin-bottom: 24px; }}
        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; font-size: 14px; font-weight: 600; margin-bottom: 8px; }}
        .form-group input {{
            width: 100%; padding: 14px; border: 1px solid #ddd; border-radius: 8px;
            font-size: 16px; font-family: inherit;
        }}
        .checkout-btn {{
            width: 100%; padding: 16px; background: #FF6B35; color: white;
            border: none; border-radius: 8px; font-size: 18px; font-weight: 600;
            cursor: pointer; margin-top: 8px;
        }}

        /* Promo Strip */
        .promo-strip {{
            display: flex; justify-content: center; gap: 48px;
            padding: 32px; background: #f5f5f5; border-top: 1px solid #e5e5e5;
        }}
        .promo-item {{ display: flex; align-items: center; gap: 12px; font-size: 14px; }}
        .promo-icon {{ font-size: 24px; }}

        /* Footer */
        .footer {{
            background: #1a1a1a; color: #888; padding: 60px 40px 32px;
        }}
        .footer-grid {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px;
            max-width: 1200px; margin: 0 auto;
        }}
        .footer-col h4 {{ color: white; font-size: 16px; margin-bottom: 16px; }}
        .footer-col a {{ display: block; color: #888; text-decoration: none; margin-bottom: 12px; font-size: 14px; }}
        .footer-col a:hover {{ color: white; }}
        .payment-icons {{ display: flex; gap: 16px; margin-top: 32px; font-size: 32px; }}
        .footer-bottom {{
            text-align: center; padding-top: 32px; margin-top: 32px;
            border-top: 1px solid #333; font-size: 14px;
        }}
    </style>
    {traps_html}
    <script>
        window.TRAP_TRIGGER_MAPPING = {trigger_mapping};
        window.TRAP_ENDPOINTS = {trap_endpoints};
    </script>
    {BEHAVIORAL_TRIGGER_JS}
</head>
<body>
    <header class="header">
        <div class="header-top">
            <a href="#" class="logo">
                <span class="logo-icon">🛍</span>
                ShopNest
            </a>
            <div class="search-bar">
                <input type="text" placeholder="Search for products, brands and more...">
                <button type="button">🔍</button>
            </div>
            <div class="header-actions">
                <a href="#" class="header-action">
                    <span class="header-action-icon">👤</span>
                    Account
                </a>
                <a href="#" class="header-action">
                    <span class="header-action-icon">❤️</span>
                    Wishlist
                </a>
                <a href="#" class="header-action cart-badge">
                    <span class="header-action-icon">🛒</span>
                    <span class="cart-count">2</span>
                    Cart
                </a>
            </div>
        </div>
        <nav class="category-nav">
            <a href="#">Women</a>
            <a href="#">Men</a>
            <a href="#">Electronics</a>
            <a href="#">Home & Garden</a>
            <a href="#">Sports</a>
            <a href="#">Beauty</a>
            <a href="#">Deals</a>
        </nav>
    </header>

    <section class="hero">
        <h1>Summer Collection 2025</h1>
        <p>Free shipping on orders over $49</p>
        <div class="hero-buttons">
            <a href="#" class="hero-btn hero-btn-primary">Shop Women</a>
            <a href="#" class="hero-btn hero-btn-secondary">Shop Men</a>
        </div>
    </section>

    <section class="products">
        <h2 class="section-title">Trending Now</h2>
        <div class="product-grid">
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop" alt="Classic Slim Fit Oxford Shirt" class="product-image">
                <div class="product-info">
                    <div class="product-brand">Oxford & Co</div>
                    <div class="product-name">Classic Slim Fit Oxford Shirt</div>
                    <div class="product-rating">
                        <span class="stars">★★★★☆</span>
                        <span class="review-count">234 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$34.99</span>
                        <span class="price-original">$59.99</span>
                    </div>
                </div>
            </div>
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop" alt="Wireless Noise-Cancelling Headphones" class="product-image">
                <div class="product-info">
                    <div class="product-brand">AudioTech</div>
                    <div class="product-name">Wireless Noise-Cancelling Headphones</div>
                    <div class="product-rating">
                        <span class="stars">★★★★★</span>
                        <span class="review-count">892 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$89.99</span>
                    </div>
                </div>
            </div>
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop" alt="Leather Crossbody Bag" class="product-image">
                <div class="product-info">
                    <div class="product-brand">Milano Leather</div>
                    <div class="product-name">Leather Crossbody Bag</div>
                    <div class="product-rating">
                        <span class="stars">★★★★☆</span>
                        <span class="review-count">156 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$67.00</span>
                    </div>
                </div>
            </div>
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop" alt="Running Shoes Pro X2" class="product-image">
                <div class="product-info">
                    <div class="product-brand">SportMax</div>
                    <div class="product-name">Running Shoes Pro X2</div>
                    <div class="product-rating">
                        <span class="stars">★★★★☆</span>
                        <span class="review-count">445 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$112.00</span>
                    </div>
                </div>
            </div>
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=400&h=400&fit=crop" alt="Ceramic Pour-Over Coffee Set" class="product-image">
                <div class="product-info">
                    <div class="product-brand">BrewMaster</div>
                    <div class="product-name">Ceramic Pour-Over Coffee Set</div>
                    <div class="product-rating">
                        <span class="stars">★★★★★</span>
                        <span class="review-count">78 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$44.99</span>
                    </div>
                </div>
            </div>
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop" alt="Merino Wool Crew Neck Sweater" class="product-image">
                <div class="product-info">
                    <div class="product-brand">Nordic Knit</div>
                    <div class="product-name">Merino Wool Crew Neck Sweater</div>
                    <div class="product-rating">
                        <span class="stars">★★★★☆</span>
                        <span class="review-count">203 reviews</span>
                    </div>
                    <div class="product-price">
                        <span class="price-current">$78.00</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="checkout">
        <div class="checkout-container">
            <h2>Quick Checkout</h2>
            <form id="checkout-form">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" placeholder="John Doe">
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" placeholder="john@example.com">
                </div>
                <div class="form-group">
                    <label>Shipping Address</label>
                    <input type="text" name="address" placeholder="123 Main St, City, State 12345">
                </div>
                <div class="form-group">
                    <label>Card Number</label>
                    <input type="text" name="card" placeholder="1234 5678 9012 3456">
                </div>
                <button type="submit" class="checkout-btn">Place Order</button>
            </form>
        </div>
    </section>

    <div class="promo-strip">
        <div class="promo-item">
            <span class="promo-icon">🔄</span>
            <span>Free Returns</span>
        </div>
        <div class="promo-item">
            <span class="promo-icon">🔒</span>
            <span>Secure Checkout</span>
        </div>
        <div class="promo-item">
            <span class="promo-icon">💬</span>
            <span>24/7 Support</span>
        </div>
    </div>

    <footer class="footer">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>About ShopNest</h4>
                <a href="#">Our Story</a>
                <a href="#">Careers</a>
                <a href="#">Press</a>
                <a href="#">Sustainability</a>
            </div>
            <div class="footer-col">
                <h4>Customer Service</h4>
                <a href="#">Help Center</a>
                <a href="#">Returns</a>
                <a href="#">Shipping Info</a>
                <a href="#">Track Order</a>
            </div>
            <div class="footer-col">
                <h4>My Account</h4>
                <a href="#">Sign In</a>
                <a href="#">Register</a>
                <a href="#">Order History</a>
                <a href="#">Wishlist</a>
            </div>
            <div class="footer-col">
                <h4>Follow Us</h4>
                <a href="#">Instagram</a>
                <a href="#">Facebook</a>
                <a href="#">Twitter</a>
                <a href="#">Pinterest</a>
            </div>
        </div>
        <div class="payment-icons">
            <span>💳</span>
            <span>🏦</span>
            <span>📱</span>
        </div>
        <div class="footer-bottom">
            © 2025 ShopNest. All rights reserved.
        </div>
    </footer>
</body>
</html>
'''
