"""
Real-World Graph Problems
==========================
Practical applications of graphs in real scenarios.
"""

from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple
import heapq


print("=" * 60)
print("Real-World Graph Applications")
print("=" * 60)
print()


# Example 1: Social Network
print("=" * 60)
print("Example 1: Social Network (Friend Connections)")
print("=" * 60)
print()
print("Problem: Find mutual friends, friend suggestions, degree of separation")
print()


class SocialNetwork:
    """
    Social network using undirected graph.
    
    Vertices = People
    Edges = Friendships
    """
    
    def __init__(self):
        self.friends = defaultdict(set)
    
    def add_friendship(self, person1, person2):
        """Add bidirectional friendship"""
        self.friends[person1].add(person2)
        self.friends[person2].add(person1)
    
    def remove_friendship(self, person1, person2):
        """Remove friendship"""
        self.friends[person1].discard(person2)
        self.friends[person2].discard(person1)
    
    def get_friends(self, person):
        """Get direct friends"""
        return list(self.friends[person])
    
    def mutual_friends(self, person1, person2):
        """
        Find mutual friends.
        
        How it works:
        1. Get friends of both people
        2. Find intersection
        
        Time: O(F) where F = number of friends
        """
        return list(self.friends[person1] & self.friends[person2])
    
    def friend_suggestions(self, person, limit=5):
        """
        Suggest new friends (friends of friends).
        
        How it works:
        1. Get friends of friends
        2. Exclude current friends and self
        3. Rank by number of mutual friends
        
        Time: O(F²)
        """
        current_friends = self.friends[person]
        suggestions = defaultdict(int)
        
        # Count mutual connections
        for friend in current_friends:
            for friend_of_friend in self.friends[friend]:
                if friend_of_friend != person and friend_of_friend not in current_friends:
                    suggestions[friend_of_friend] += 1
        
        # Sort by number of mutual friends
        sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        return [person for person, _ in sorted_suggestions[:limit]]
    
    def degrees_of_separation(self, person1, person2):
        """
        Find degrees of separation (BFS shortest path).
        
        How it works:
        1. BFS from person1
        2. Track distance to each person
        3. Return distance to person2
        
        Time: O(V + E)
        Returns: Number of connections, or -1 if not connected
        """
        if person1 == person2:
            return 0
        
        visited = {person1}
        queue = deque([(person1, 0)])
        
        while queue:
            current, dist = queue.popleft()
            
            for friend in self.friends[current]:
                if friend == person2:
                    return dist + 1
                
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, dist + 1))
        
        return -1  # Not connected
    
    def find_path(self, person1, person2):
        """
        Find connection path between two people.
        
        Time: O(V + E)
        Returns: Path or None if not connected
        """
        if person1 == person2:
            return [person1]
        
        visited = {person1}
        queue = deque([person1])
        parent = {person1: None}
        
        while queue:
            current = queue.popleft()
            
            if current == person2:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            
            for friend in self.friends[current]:
                if friend not in visited:
                    visited.add(friend)
                    parent[friend] = current
                    queue.append(friend)
        
        return None


# Demo Social Network
print("Social Network Example:")
print()
sn = SocialNetwork()
sn.add_friendship("Alice", "Bob")
sn.add_friendship("Alice", "Charlie")
sn.add_friendship("Bob", "David")
sn.add_friendship("Charlie", "David")
sn.add_friendship("David", "Eve")

print("Friendships:")
print("  Alice ↔ Bob, Charlie")
print("  Bob ↔ David")
print("  Charlie ↔ David")
print("  David ↔ Eve")
print()

print(f"Alice's friends: {sn.get_friends('Alice')}")
print(f"Mutual friends (Alice, David): {sn.mutual_friends('Alice', 'David')}")
print(f"Friend suggestions for Bob: {sn.friend_suggestions('Bob')}")
print(f"Degrees of separation (Alice, Eve): {sn.degrees_of_separation('Alice', 'Eve')}")
print(f"Path from Alice to Eve: {' → '.join(sn.find_path('Alice', 'Eve'))}")
print()


# Example 2: Web Crawler
print("=" * 60)
print("Example 2: Web Crawler (Following Links)")
print("=" * 60)
print()
print("Problem: Crawl websites starting from seed URL")
print()


class WebCrawler:
    """
    Web crawler using directed graph.
    
    Vertices = URLs
    Edges = Hyperlinks
    """
    
    def __init__(self, max_depth=3, max_pages=100):
        self.graph = defaultdict(set)
        self.max_depth = max_depth
        self.max_pages = max_pages
    
    def crawl_bfs(self, start_url, get_links_func):
        """
        Crawl web pages using BFS (level by level).
        
        How it works:
        1. Start from seed URL
        2. Visit page, extract links
        3. Add links to queue
        4. Respect max depth and max pages
        
        Time: O(V + E)
        
        Args:
            start_url: Starting URL
            get_links_func: Function that returns links from a URL
        
        Returns: Set of visited URLs
        """
        visited = set()
        queue = deque([(start_url, 0)])
        visited.add(start_url)
        
        while queue and len(visited) < self.max_pages:
            url, depth = queue.popleft()
            
            if depth >= self.max_depth:
                continue
            
            # Get links from page (simulated)
            links = get_links_func(url)
            
            for link in links:
                if link not in visited and len(visited) < self.max_pages:
                    visited.add(link)
                    self.graph[url].add(link)
                    queue.append((link, depth + 1))
        
        return visited
    
    def find_path_to_url(self, start, target):
        """
        Find navigation path from start to target URL.
        
        Time: O(V + E)
        """
        if start == target:
            return [start]
        
        visited = {start}
        queue = deque([start])
        parent = {start: None}
        
        while queue:
            url = queue.popleft()
            
            if url == target:
                path = []
                while url:
                    path.append(url)
                    url = parent[url]
                return path[::-1]
            
            for link in self.graph[url]:
                if link not in visited:
                    visited.add(link)
                    parent[link] = url
                    queue.append(link)
        
        return None


# Demo Web Crawler
print("Web Crawler Example:")
print()

# Simulate getting links from a page
def simulate_get_links(url):
    links_map = {
        "home.com": ["home.com/about", "home.com/products"],
        "home.com/about": ["home.com/team", "home.com/contact"],
        "home.com/products": ["home.com/product1", "home.com/product2"],
        "home.com/team": [],
        "home.com/contact": [],
        "home.com/product1": [],
        "home.com/product2": [],
    }
    return links_map.get(url, [])

crawler = WebCrawler(max_depth=2, max_pages=10)
visited_urls = crawler.crawl_bfs("home.com", simulate_get_links)

print(f"Crawled {len(visited_urls)} pages:")
for url in sorted(visited_urls):
    print(f"  {url}")
print()


# Example 3: Task Scheduler with Dependencies
print("=" * 60)
print("Example 3: Task Scheduler (Build System)")
print("=" * 60)
print()
print("Problem: Execute tasks respecting dependencies")
print()


class TaskScheduler:
    """
    Task scheduler using directed acyclic graph (DAG).
    
    Vertices = Tasks
    Edges = Dependencies (A → B means B depends on A)
    """
    
    def __init__(self):
        self.dependencies = defaultdict(list)
        self.tasks = set()
    
    def add_task(self, task):
        """Add task"""
        self.tasks.add(task)
    
    def add_dependency(self, task, depends_on):
        """
        Add dependency: task depends on depends_on.
        (depends_on must complete before task)
        """
        self.dependencies[depends_on].append(task)
        self.tasks.add(task)
        self.tasks.add(depends_on)
    
    def can_complete_all_tasks(self):
        """
        Check if all tasks can be completed (no cycles).
        
        How it works:
        1. Use cycle detection
        2. If cycle exists, deadlock (cannot complete)
        
        Time: O(V + E)
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {task: WHITE for task in self.tasks}
        
        def has_cycle(task):
            color[task] = GRAY
            
            for dependent in self.dependencies[task]:
                if color[dependent] == GRAY:
                    return True  # Back edge = cycle
                if color[dependent] == WHITE:
                    if has_cycle(dependent):
                        return True
            
            color[task] = BLACK
            return False
        
        for task in self.tasks:
            if color[task] == WHITE:
                if has_cycle(task):
                    return False
        
        return True
    
    def get_execution_order(self):
        """
        Get valid task execution order (topological sort).
        
        How it works:
        1. Kahn's algorithm (BFS-based topological sort)
        2. Start with tasks that have no dependencies
        3. Process and reduce dependency count
        
        Time: O(V + E)
        Returns: Valid order or [] if cycle exists
        """
        in_degree = {task: 0 for task in self.tasks}
        
        # Calculate in-degrees
        for task in self.dependencies:
            for dependent in self.dependencies[task]:
                in_degree[dependent] += 1
        
        # Start with zero in-degree tasks
        queue = deque([task for task in self.tasks if in_degree[task] == 0])
        result = []
        
        while queue:
            task = queue.popleft()
            result.append(task)
            
            for dependent in self.dependencies[task]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        return result if len(result) == len(self.tasks) else []
    
    def get_parallel_execution_groups(self):
        """
        Group tasks that can be executed in parallel.
        
        How it works:
        1. Topological sort with levels
        2. Tasks at same level can run in parallel
        
        Time: O(V + E)
        Returns: List of groups (each group can run in parallel)
        """
        in_degree = {task: 0 for task in self.tasks}
        
        for task in self.dependencies:
            for dependent in self.dependencies[task]:
                in_degree[dependent] += 1
        
        current_level = [task for task in self.tasks if in_degree[task] == 0]
        groups = []
        
        while current_level:
            groups.append(current_level[:])
            next_level = []
            
            for task in current_level:
                for dependent in self.dependencies[task]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_level.append(dependent)
            
            current_level = next_level
        
        return groups


# Demo Task Scheduler
print("Task Scheduler Example:")
print()
print("Build system with task dependencies:")
print("  compile → link → test")
print("  compile → docs")
print()

scheduler = TaskScheduler()
scheduler.add_dependency("link", "compile")
scheduler.add_dependency("test", "link")
scheduler.add_dependency("docs", "compile")

print(f"Can complete all tasks? {scheduler.can_complete_all_tasks()}")
print(f"Execution order: {' → '.join(scheduler.get_execution_order())}")
print()
print("Parallel execution groups:")
groups = scheduler.get_parallel_execution_groups()
for i, group in enumerate(groups, 1):
    print(f"  Level {i}: {', '.join(group)}")
print()


# Example 4: Navigation/Maps (Shortest Path)
print("=" * 60)
print("Example 4: GPS Navigation (Shortest Path)")
print("=" * 60)
print()
print("Problem: Find shortest route between locations")
print()


class GPSNavigator:
    """
    GPS navigation using weighted directed graph.
    
    Vertices = Locations
    Edges = Roads (with distances)
    """
    
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_road(self, from_loc, to_loc, distance, bidirectional=True):
        """Add road with distance"""
        self.graph[from_loc].append((to_loc, distance))
        if bidirectional:
            self.graph[to_loc].append((from_loc, distance))
    
    def shortest_path_dijkstra(self, start, end):
        """
        Find shortest path using Dijkstra's algorithm.
        
        How it works:
        1. Use min-heap to always process nearest unvisited location
        2. Update distances to neighbors
        3. Track path using parent pointers
        
        Time: O((V + E) log V)
        Returns: (distance, path) or (inf, None) if unreachable
        """
        distances = {start: 0}
        parent = {start: None}
        heap = [(0, start)]
        visited = set()
        
        while heap:
            dist, loc = heapq.heappop(heap)
            
            if loc in visited:
                continue
            
            visited.add(loc)
            
            if loc == end:
                # Reconstruct path
                path = []
                current = end
                while current:
                    path.append(current)
                    current = parent[current]
                return dist, path[::-1]
            
            for neighbor, road_dist in self.graph[loc]:
                new_dist = dist + road_dist
                
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parent[neighbor] = loc
                    heapq.heappush(heap, (new_dist, neighbor))
        
        return float('inf'), None
    
    def alternative_routes(self, start, end, max_routes=3):
        """
        Find alternative routes (k shortest paths).
        
        Simplified: Find paths avoiding each edge once
        Time: O(E × (V + E) log V)
        """
        routes = []
        
        # Get main route
        dist, path = self.shortest_path_dijkstra(start, end)
        if path:
            routes.append((dist, path))
        
        # Find alternatives by temporarily removing edges
        # (Simplified - real implementation would use Yen's algorithm)
        
        return routes


# Demo GPS Navigator
print("GPS Navigator Example:")
print()
print("City map:")
print()
print("   Home --5-- Work")
print("    |          |")
print("    3          2")
print("    |          |")
print("   Gym ---4--- Mall")
print()

gps = GPSNavigator()
gps.add_road("Home", "Work", 5)
gps.add_road("Home", "Gym", 3)
gps.add_road("Work", "Mall", 2)
gps.add_road("Gym", "Mall", 4)

dist, path = gps.shortest_path_dijkstra("Home", "Mall")
print(f"Shortest path from Home to Mall:")
print(f"  Distance: {dist} km")
print(f"  Route: {' → '.join(path)}")
print()


# Example 5: Recommendation System
print("=" * 60)
print("Example 5: Movie Recommendation System")
print("=" * 60)
print()
print("Problem: Recommend movies based on user preferences")
print()


class MovieRecommender:
    """
    Bipartite graph: Users ↔ Movies
    Edge weight = Rating
    """
    
    def __init__(self):
        self.user_ratings = defaultdict(dict)  # user -> {movie: rating}
        self.movie_ratings = defaultdict(dict)  # movie -> {user: rating}
    
    def add_rating(self, user, movie, rating):
        """Add user rating for movie"""
        self.user_ratings[user][movie] = rating
        self.movie_ratings[movie][user] = rating
    
    def similar_users(self, user, limit=5):
        """
        Find users with similar taste.
        
        How it works:
        1. Find users who rated same movies
        2. Calculate similarity score (common ratings)
        3. Return most similar users
        
        Time: O(M × U) where M=movies, U=users
        """
        if user not in self.user_ratings:
            return []
        
        user_movies = set(self.user_ratings[user].keys())
        similarity = defaultdict(int)
        
        for movie in user_movies:
            for other_user in self.movie_ratings[movie]:
                if other_user != user:
                    # Simple similarity: count common movies
                    similarity[other_user] += 1
        
        sorted_similar = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
        return [u for u, _ in sorted_similar[:limit]]
    
    def recommend_movies(self, user, limit=5):
        """
        Recommend movies based on similar users.
        
        How it works:
        1. Find similar users
        2. Get movies they liked
        3. Filter out movies user already watched
        4. Rank by popularity among similar users
        
        Time: O(M × U)
        """
        if user not in self.user_ratings:
            return []
        
        user_movies = set(self.user_ratings[user].keys())
        similar = self.similar_users(user, limit=10)
        
        recommendations = defaultdict(float)
        
        for similar_user in similar:
            for movie, rating in self.user_ratings[similar_user].items():
                if movie not in user_movies and rating >= 4:
                    recommendations[movie] += rating
        
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in sorted_recs[:limit]]


# Demo Recommender
print("Movie Recommendation Example:")
print()

recommender = MovieRecommender()

# Add ratings
recommender.add_rating("Alice", "Inception", 5)
recommender.add_rating("Alice", "Interstellar", 5)
recommender.add_rating("Alice", "Matrix", 4)

recommender.add_rating("Bob", "Inception", 5)
recommender.add_rating("Bob", "Interstellar", 4)
recommender.add_rating("Bob", "Tenet", 5)

recommender.add_rating("Charlie", "Matrix", 5)
recommender.add_rating("Charlie", "Terminator", 4)

print("Ratings:")
print("  Alice: Inception(5), Interstellar(5), Matrix(4)")
print("  Bob: Inception(5), Interstellar(4), Tenet(5)")
print("  Charlie: Matrix(5), Terminator(4)")
print()

similar = recommender.similar_users("Alice")
print(f"Users similar to Alice: {similar}")

recommendations = recommender.recommend_movies("Alice")
print(f"Recommended movies for Alice: {recommendations}")
print()


# Example 6: Network Routing
print("=" * 60)
print("Example 6: Network Packet Routing")
print("=" * 60)
print()
print("Problem: Route packets through network efficiently")
print()


class NetworkRouter:
    """
    Network topology as weighted directed graph.
    
    Vertices = Routers
    Edges = Network connections (with bandwidth/latency)
    """
    
    def __init__(self):
        self.network = defaultdict(list)
    
    def add_connection(self, router1, router2, latency, bidirectional=True):
        """Add network connection"""
        self.network[router1].append((router2, latency))
        if bidirectional:
            self.network[router2].append((router1, latency))
    
    def find_fastest_route(self, source, destination):
        """
        Find lowest latency route (Dijkstra).
        
        Time: O((V + E) log V)
        """
        distances = {source: 0}
        parent = {source: None}
        heap = [(0, source)]
        visited = set()
        
        while heap:
            latency, router = heapq.heappop(heap)
            
            if router in visited:
                continue
            
            visited.add(router)
            
            if router == destination:
                path = []
                current = destination
                while current:
                    path.append(current)
                    current = parent[current]
                return latency, path[::-1]
            
            for neighbor, link_latency in self.network[router]:
                new_latency = latency + link_latency
                
                if neighbor not in distances or new_latency < distances[neighbor]:
                    distances[neighbor] = new_latency
                    parent[neighbor] = router
                    heapq.heappush(heap, (new_latency, neighbor))
        
        return float('inf'), None
    
    def is_network_connected(self):
        """
        Check if all routers can communicate.
        
        Time: O(V + E)
        """
        if not self.network:
            return True
        
        start = next(iter(self.network.keys()))
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            router = queue.popleft()
            for neighbor, _ in self.network[router]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.network)


# Demo Network Router
print("Network Routing Example:")
print()
print("Network topology:")
print("  R1 --10ms-- R2")
print("  |           |")
print("  5ms        2ms")
print("  |           |")
print("  R3 --8ms-- R4")
print()

router = NetworkRouter()
router.add_connection("R1", "R2", 10)
router.add_connection("R1", "R3", 5)
router.add_connection("R2", "R4", 2)
router.add_connection("R3", "R4", 8)

latency, path = router.find_fastest_route("R1", "R4")
print(f"Fastest route from R1 to R4:")
print(f"  Latency: {latency}ms")
print(f"  Path: {' → '.join(path)}")
print(f"Network connected? {router.is_network_connected()}")
print()


# Summary
print("=" * 60)
print("Summary of Real-World Applications")
print("=" * 60)
print()
print("1. Social Networks:")
print("   • Friend suggestions (BFS neighbors)")
print("   • Degrees of separation (BFS shortest path)")
print("   • Community detection (connected components)")
print()
print("2. Web Crawling:")
print("   • Page discovery (BFS/DFS)")
print("   • Link analysis (PageRank)")
print("   • Sitemap generation")
print()
print("3. Task Scheduling:")
print("   • Dependency resolution (topological sort)")
print("   • Parallel execution (level-based grouping)")
print("   • Deadlock detection (cycle detection)")
print()
print("4. Navigation/Maps:")
print("   • Shortest path (Dijkstra/A*)")
print("   • Alternative routes")
print("   • Traffic optimization")
print()
print("5. Recommendation Systems:")
print("   • Collaborative filtering (bipartite graph)")
print("   • Similar users/items")
print("   • Content recommendations")
print()
print("6. Network Routing:")
print("   • Packet routing (shortest path)")
print("   • Network topology (connectivity)")
print("   • Load balancing")
print()
print("Common Patterns:")
print("  • BFS: Shortest path, nearest neighbors")
print("  • DFS: Path finding, cycle detection")
print("  • Topological Sort: Dependencies, scheduling")
print("  • Dijkstra: Weighted shortest path")
print("  • Connected Components: Communities, clusters")
print()
