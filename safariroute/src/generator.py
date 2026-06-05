import random
import string
import datetime

def generate_safariroute_code(route_id):
    """
    Generates a unique Safariroute code in the format:
    SR-[YEAR]-[ROUTE_TYPE]-[RANDOM_ALPHANUMERIC]
    """
    year = datetime.datetime.now().year
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Extract route type prefix (K, T, or EA)
    prefix = route_id.split('-')[0]
    
    return f"SR-{year}-{prefix}-{random_part}"

def calculate_commission(ticket_price):
    """
    Calculates the 5% commission based on the user's requirement.
    """
    commission_rate = 0.05
    return ticket_price * commission_rate

if __name__ == "__main__":
    # Example for the user
    price = 1000  # Example ticket price in KES/TZS
    comm = calculate_commission(price)
    print(f"Ticket Price: {price} -> Commission (5%): {comm}")