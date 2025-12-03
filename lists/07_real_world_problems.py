"""
Lists - Real World Problems
===========================
Practical problems you might encounter in real applications.
"""

# Problem 1: Shopping Cart Management
class ShoppingCart:
    """
    Manage items in an online shopping cart.
    Real-world use: E-commerce platforms
    """
    def __init__(self):
        self.items = []
    
    def add_item(self, name, price, quantity=1):
        """Add item to cart"""
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def remove_item(self, name):
        """Remove item from cart"""
        self.items = [item for item in self.items if item['name'] != name]
    
    def update_quantity(self, name, quantity):
        """Update item quantity"""
        for item in self.items:
            if item['name'] == name:
                item['quantity'] = quantity
                break
    
    def get_total(self):
        """Calculate total price"""
        return sum(item['price'] * item['quantity'] for item in self.items)
    
    def apply_discount(self, discount_percent):
        """Apply discount to all items"""
        for item in self.items:
            item['price'] *= (1 - discount_percent / 100)
    
    def get_cart_summary(self):
        """Return formatted cart summary"""
        return self.items

# Test Shopping Cart
print("Problem 1: Shopping Cart Management")
cart = ShoppingCart()
cart.add_item("Laptop", 999.99, 1)
cart.add_item("Mouse", 29.99, 2)
cart.add_item("Keyboard", 79.99, 1)
print(f"Total: ${cart.get_total():.2f}")
cart.apply_discount(10)
print(f"After 10% discount: ${cart.get_total():.2f}")
print()


# Problem 2: Task Priority Queue (Simple Todo App)
class TodoList:
    """
    Manage tasks with priorities.
    Real-world use: Task management apps, project management tools
    """
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task, priority=1):
        """Add task with priority (1=high, 2=medium, 3=low)"""
        self.tasks.append({'task': task, 'priority': priority, 'completed': False})
        self.tasks.sort(key=lambda x: x['priority'])
    
    def complete_task(self, task):
        """Mark task as completed"""
        for t in self.tasks:
            if t['task'] == task:
                t['completed'] = True
                break
    
    def get_pending_tasks(self):
        """Get all pending tasks"""
        return [t['task'] for t in self.tasks if not t['completed']]
    
    def get_high_priority_tasks(self):
        """Get high priority pending tasks"""
        return [t['task'] for t in self.tasks if t['priority'] == 1 and not t['completed']]

# Test Todo List
print("Problem 2: Task Priority Queue")
todo = TodoList()
todo.add_task("Fix critical bug", 1)
todo.add_task("Review code", 2)
todo.add_task("Update documentation", 3)
todo.add_task("Deploy to production", 1)
print(f"High priority tasks: {todo.get_high_priority_tasks()}")
print(f"All pending: {todo.get_pending_tasks()}")
print()


# Problem 3: Stock Price Analysis
def analyze_stock_prices(prices):
    """
    Analyze stock prices for trading insights.
    Real-world use: Trading platforms, financial apps
    """
    if not prices:
        return None
    
    # Best day to buy and sell
    min_price = prices[0]
    max_profit = 0
    buy_day = 0
    sell_day = 0
    temp_buy = 0
    
    for i, price in enumerate(prices):
        if price < min_price:
            min_price = price
            temp_buy = i
        
        profit = price - min_price
        if profit > max_profit:
            max_profit = profit
            buy_day = temp_buy
            sell_day = i
    
    # Calculate moving average (7-day)
    window = 7
    moving_avg = []
    for i in range(len(prices) - window + 1):
        avg = sum(prices[i:i+window]) / window
        moving_avg.append(round(avg, 2))
    
    # Detect price volatility
    price_changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    volatility = sum(abs(change) for change in price_changes) / len(price_changes)
    
    return {
        'best_buy_day': buy_day,
        'best_sell_day': sell_day,
        'max_profit': max_profit,
        'moving_average_7d': moving_avg[:5],  # First 5 values
        'volatility': round(volatility, 2)
    }

# Test Stock Analysis
print("Problem 3: Stock Price Analysis")
prices = [100, 102, 98, 105, 110, 95, 108, 112, 107, 115, 118, 120, 116]
analysis = analyze_stock_prices(prices)
print(f"Buy on day {analysis['best_buy_day']}, sell on day {analysis['best_sell_day']}")
print(f"Maximum profit: ${analysis['max_profit']}")
print(f"Volatility: {analysis['volatility']}")
print()


# Problem 4: Meeting Room Scheduler
def can_attend_all_meetings(meetings):
    """
    Check if person can attend all meetings (no overlaps).
    Real-world use: Calendar apps, scheduling systems
    meetings: list of [start_time, end_time]
    """
    if not meetings:
        return True
    
    # Sort by start time
    meetings.sort(key=lambda x: x[0])
    
    for i in range(1, len(meetings)):
        if meetings[i][0] < meetings[i-1][1]:
            return False
    
    return True

def min_meeting_rooms(meetings):
    """
    Find minimum number of meeting rooms needed.
    Real-world use: Office space management, resource allocation
    """
    if not meetings:
        return 0
    
    starts = sorted([m[0] for m in meetings])
    ends = sorted([m[1] for m in meetings])
    
    rooms_needed = 0
    max_rooms = 0
    start_ptr = 0
    end_ptr = 0
    
    while start_ptr < len(starts):
        if starts[start_ptr] < ends[end_ptr]:
            rooms_needed += 1
            max_rooms = max(max_rooms, rooms_needed)
            start_ptr += 1
        else:
            rooms_needed -= 1
            end_ptr += 1
    
    return max_rooms

# Test Meeting Scheduler
print("Problem 4: Meeting Room Scheduler")
meetings1 = [[9, 10], [10, 11], [11, 12]]
meetings2 = [[9, 10], [9.5, 10.5], [10, 11]]
print(f"Can attend all {meetings1}: {can_attend_all_meetings(meetings1)}")
print(f"Can attend all {meetings2}: {can_attend_all_meetings(meetings2)}")
print(f"Rooms needed for {meetings2}: {min_meeting_rooms(meetings2)}")
print()


# Problem 5: Social Media Feed (News Feed Algorithm)
class SocialFeed:
    """
    Manage and rank social media posts.
    Real-world use: Facebook, Twitter, Instagram feed algorithms
    """
    def __init__(self):
        self.posts = []
    
    def add_post(self, user, content, timestamp, likes=0, comments=0):
        """Add new post"""
        self.posts.append({
            'user': user,
            'content': content,
            'timestamp': timestamp,
            'likes': likes,
            'comments': comments,
            'engagement_score': 0
        })
    
    def calculate_engagement(self):
        """Calculate engagement score for ranking"""
        for post in self.posts:
            # Simple engagement formula
            post['engagement_score'] = post['likes'] * 2 + post['comments'] * 5
    
    def get_top_posts(self, n=5):
        """Get top N posts by engagement"""
        self.calculate_engagement()
        sorted_posts = sorted(self.posts, key=lambda x: x['engagement_score'], reverse=True)
        return [{'user': p['user'], 'content': p['content'][:50], 'score': p['engagement_score']} 
                for p in sorted_posts[:n]]
    
    def get_recent_posts(self, n=5):
        """Get most recent posts"""
        sorted_posts = sorted(self.posts, key=lambda x: x['timestamp'], reverse=True)
        return [{'user': p['user'], 'content': p['content'][:50]} for p in sorted_posts[:n]]

# Test Social Feed
print("Problem 5: Social Media Feed")
feed = SocialFeed()
feed.add_post("alice", "Just launched my new app!", 1700000000, likes=150, comments=25)
feed.add_post("bob", "Beautiful sunset today", 1700000060, likes=80, comments=10)
feed.add_post("charlie", "Check out my new blog post", 1700000120, likes=200, comments=30)
feed.add_post("diana", "Coffee time!", 1700000180, likes=50, comments=5)
print("Top posts by engagement:")
for post in feed.get_top_posts(3):
    print(f"  @{post['user']}: {post['content']} (score: {post['score']})")
print()


# Problem 6: URL History and Bookmarks (Browser History)
class BrowserHistory:
    """
    Manage browser history and bookmarks.
    Real-world use: Web browsers, navigation apps
    """
    def __init__(self):
        self.history = []
        self.bookmarks = []
        self.current_index = -1
    
    def visit(self, url):
        """Visit a new URL"""
        # Remove forward history if exists
        self.history = self.history[:self.current_index + 1]
        self.history.append(url)
        self.current_index += 1
    
    def back(self):
        """Go back in history"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def forward(self):
        """Go forward in history"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None
    
    def add_bookmark(self, url, title):
        """Add bookmark"""
        self.bookmarks.append({'url': url, 'title': title})
    
    def search_history(self, keyword):
        """Search in history"""
        return [url for url in self.history if keyword.lower() in url.lower()]
    
    def get_most_visited(self, n=5):
        """Get most visited URLs"""
        from collections import Counter
        counter = Counter(self.history)
        return counter.most_common(n)

# Test Browser History
print("Problem 6: Browser History")
browser = BrowserHistory()
browser.visit("google.com")
browser.visit("github.com")
browser.visit("stackoverflow.com")
browser.visit("python.org")
print(f"Current: python.org")
print(f"Back: {browser.back()}")
print(f"Back: {browser.back()}")
print(f"Forward: {browser.forward()}")
browser.add_bookmark("github.com", "GitHub")
print(f"Search 'git': {browser.search_history('git')}")
print()


# Problem 7: Playlist Manager (Music/Video Streaming)
class Playlist:
    """
    Manage music/video playlist.
    Real-world use: Spotify, YouTube, Netflix
    """
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.current_index = 0
    
    def add_song(self, title, artist, duration):
        """Add song to playlist"""
        self.songs.append({
            'title': title,
            'artist': artist,
            'duration': duration,
            'play_count': 0
        })
    
    def play_next(self):
        """Play next song"""
        if self.current_index < len(self.songs) - 1:
            self.current_index += 1
            self.songs[self.current_index]['play_count'] += 1
            return self.songs[self.current_index]
        return None
    
    def shuffle(self):
        """Shuffle playlist"""
        import random
        random.shuffle(self.songs)
        self.current_index = 0
    
    def get_total_duration(self):
        """Get total playlist duration in seconds"""
        return sum(song['duration'] for song in self.songs)
    
    def get_most_played(self, n=3):
        """Get most played songs"""
        sorted_songs = sorted(self.songs, key=lambda x: x['play_count'], reverse=True)
        return [f"{s['title']} by {s['artist']}" for s in sorted_songs[:n]]
    
    def remove_duplicates(self):
        """Remove duplicate songs"""
        seen = set()
        unique_songs = []
        for song in self.songs:
            key = (song['title'], song['artist'])
            if key not in seen:
                seen.add(key)
                unique_songs.append(song)
        self.songs = unique_songs

# Test Playlist
print("Problem 7: Playlist Manager")
playlist = Playlist("My Favorites")
playlist.add_song("Bohemian Rhapsody", "Queen", 354)
playlist.add_song("Stairway to Heaven", "Led Zeppelin", 482)
playlist.add_song("Hotel California", "Eagles", 391)
print(f"Total duration: {playlist.get_total_duration()} seconds")
next_song = playlist.play_next()
if next_song:
    print(f"Now playing: {next_song['title']} by {next_song['artist']}")
print()


# Problem 8: Log Analysis System
def analyze_server_logs(logs):
    """
    Analyze server logs for errors and patterns.
    Real-world use: DevOps, monitoring systems
    logs: list of log entries with timestamp, level, message
    """
    error_count = 0
    warning_count = 0
    error_messages = []
    peak_hours = [0] * 24
    
    for log in logs:
        level = log.get('level', 'INFO')
        timestamp = log.get('timestamp', 0)
        message = log.get('message', '')
        
        # Count by severity
        if level == 'ERROR':
            error_count += 1
            error_messages.append(message)
        elif level == 'WARNING':
            warning_count += 1
        
        # Track peak hours (assuming timestamp is hour 0-23)
        hour = timestamp % 24
        peak_hours[hour] += 1
    
    # Find peak hour
    peak_hour = peak_hours.index(max(peak_hours))
    
    return {
        'total_logs': len(logs),
        'errors': error_count,
        'warnings': warning_count,
        'error_rate': round(error_count / len(logs) * 100, 2) if logs else 0,
        'peak_hour': peak_hour,
        'recent_errors': error_messages[-3:]  # Last 3 errors
    }

# Test Log Analysis
print("Problem 8: Log Analysis System")
logs = [
    {'timestamp': 10, 'level': 'INFO', 'message': 'Server started'},
    {'timestamp': 10, 'level': 'ERROR', 'message': 'Database connection failed'},
    {'timestamp': 11, 'level': 'WARNING', 'message': 'High memory usage'},
    {'timestamp': 11, 'level': 'INFO', 'message': 'Request processed'},
    {'timestamp': 14, 'level': 'ERROR', 'message': 'Timeout error'},
    {'timestamp': 14, 'level': 'INFO', 'message': 'Cache cleared'},
]
analysis = analyze_server_logs(logs)
print(f"Total logs: {analysis['total_logs']}")
print(f"Error rate: {analysis['error_rate']}%")
print(f"Peak hour: {analysis['peak_hour']}:00")
print()


# Problem 9: Inventory Management System
class Inventory:
    """
    Manage product inventory for e-commerce.
    Real-world use: Warehouse management, retail systems
    """
    def __init__(self):
        self.products = []
    
    def add_product(self, product_id, name, quantity, price, min_stock=10):
        """Add product to inventory"""
        self.products.append({
            'id': product_id,
            'name': name,
            'quantity': quantity,
            'price': price,
            'min_stock': min_stock
        })
    
    def update_stock(self, product_id, quantity_change):
        """Update product quantity (positive for restock, negative for sale)"""
        for product in self.products:
            if product['id'] == product_id:
                product['quantity'] += quantity_change
                return True
        return False
    
    def get_low_stock_items(self):
        """Get products below minimum stock level"""
        return [p['name'] for p in self.products if p['quantity'] < p['min_stock']]
    
    def get_inventory_value(self):
        """Calculate total inventory value"""
        return sum(p['quantity'] * p['price'] for p in self.products)
    
    def get_out_of_stock(self):
        """Get products that are out of stock"""
        return [p['name'] for p in self.products if p['quantity'] == 0]
    
    def search_product(self, keyword):
        """Search products by name"""
        return [p for p in self.products if keyword.lower() in p['name'].lower()]

# Test Inventory
print("Problem 9: Inventory Management System")
inventory = Inventory()
inventory.add_product(1, "Laptop", 50, 999.99, min_stock=20)
inventory.add_product(2, "Mouse", 15, 29.99, min_stock=30)
inventory.add_product(3, "Keyboard", 0, 79.99, min_stock=25)
inventory.update_stock(1, -10)  # Sold 10 laptops
print(f"Low stock items: {inventory.get_low_stock_items()}")
print(f"Out of stock: {inventory.get_out_of_stock()}")
print(f"Total inventory value: ${inventory.get_inventory_value():,.2f}")
print()


# Problem 10: Movie Recommendation System (Basic)
def recommend_movies(user_ratings, all_movies):
    """
    Simple movie recommendation based on user ratings.
    Real-world use: Netflix, Amazon Prime, streaming platforms
    user_ratings: dict of {movie: rating}
    all_movies: list of dicts with movie info and genres
    """
    # Find user's favorite genres
    favorite_genres = []
    for movie in all_movies:
        if movie['title'] in user_ratings and user_ratings[movie['title']] >= 4:
            favorite_genres.extend(movie['genres'])
    
    # Count genre preferences
    from collections import Counter
    genre_counts = Counter(favorite_genres)
    top_genres = [genre for genre, _ in genre_counts.most_common(3)]
    
    # Recommend unwatched movies from favorite genres
    recommendations = []
    for movie in all_movies:
        if movie['title'] not in user_ratings:
            # Check if movie has any of user's favorite genres
            if any(genre in movie['genres'] for genre in top_genres):
                recommendations.append({
                    'title': movie['title'],
                    'genres': movie['genres'],
                    'rating': movie.get('avg_rating', 0)
                })
    
    # Sort by average rating
    recommendations.sort(key=lambda x: x['rating'], reverse=True)
    return recommendations[:5]

# Test Movie Recommendations
print("Problem 10: Movie Recommendation System")
user_ratings = {
    "The Matrix": 5,
    "Inception": 5,
    "Interstellar": 4,
    "The Notebook": 2
}

all_movies = [
    {"title": "The Matrix", "genres": ["Sci-Fi", "Action"], "avg_rating": 4.7},
    {"title": "Inception", "genres": ["Sci-Fi", "Thriller"], "avg_rating": 4.8},
    {"title": "Interstellar", "genres": ["Sci-Fi", "Drama"], "avg_rating": 4.6},
    {"title": "The Notebook", "genres": ["Romance", "Drama"], "avg_rating": 4.2},
    {"title": "Blade Runner", "genres": ["Sci-Fi", "Action"], "avg_rating": 4.5},
    {"title": "Arrival", "genres": ["Sci-Fi", "Drama"], "avg_rating": 4.4},
    {"title": "The Shawshank Redemption", "genres": ["Drama"], "avg_rating": 4.9},
]

recommendations = recommend_movies(user_ratings, all_movies)
print("Recommended movies:")
for movie in recommendations[:3]:
    print(f"  {movie['title']} - {', '.join(movie['genres'])} (★{movie['rating']})")
