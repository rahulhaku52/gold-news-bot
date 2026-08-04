from database import performance_db

def get_historical_performance_metrics():
    """Retrieves empirical win rates and setup reliability from SQLite DB"""
    stats = performance_db.get_performance_summary()
    return stats

if __name__ == '__main__':
    print("Performance layer module ready.")
