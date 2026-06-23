import os
import datetime
import urllib.parse
from fastapi import APIRouter, BackgroundTasks, Response
import httpx

# We use an APIRouter so this code can hook perfectly into your main app
router = APIRouter()

# 1. DATA LAYER CONFIGURATION
LEADS_FILE = "leads.txt"

# 2. B2B NETWORK CONFIGURATION (Africa's Talking Gateway)
import os

# By removing the hardcoded string, you eliminate the risk of accidental exposure.
# AT_USERNAME = "sandbox"
# AT_API_KEY = "your_actual_key_here" # REMOVED FOR SECURITY
# AT_SMS_URL = "..."
AT_SMS_URL = "https://api.sandbox.africastalking.com/version1/messaging/bulk"

# 3. VERIFIED B2B PARTNERS REGISTRY
PARTNERS_DB = {
    "wilson_aviation": {
        "name": "Wilson Light Aircraft Charters", 
        "phone": "+254712345678", 
        "base_fee": 0.15
    },
    "mara_cruisers": {
        "name": "Mara 4x4 Safari Rentals", 
        "phone": "+254787654321", 
        "base_fee": 0.12
    }
}

# 4. ROUTE ENHANCER BACKGROUND ENGINE
def send_route_enhancer_sms(operator_phone: str, operator_name: str, base_fee: float, details: dict):
    """Dispatches the automated B2B text message via Africa's Talking API"""
    promo_fee = max(0.02, base_fee - 0.05) 
    timestamp = datetime.datetime.now().strftime("%H:%M")
    
    sms_text = (
        f"Osare Route Enhancer [{timestamp}]\n"
        f"New Lead: {details['client_type']} seeking {details['vehicle']} to {details['destination']}.\n"
        f"Accept via Osare App now. Your platform fee drops from {base_fee*100:.0f}% to {promo_fee*100:.0f}%!"
    )
    
    headers = {
        "apiKey": AT_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "username": AT_USERNAME,
        "to": operator_phone,
        "message": sms_text,
        "from": "OSARE"
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(AT_SMS_URL, headers=headers, data=data)
            print(f"SMS Dispatch Log - Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to execute background B2B SMS routing: {e}")

# 5. THE ROUTE CONTROLLER (THE REVENUE HUB)
@router.get("/click-lead/safari")
def process_safari_lead(operator_id: str, transport: str, dest: str, background_tasks: BackgroundTasks):
    timestamp = datetime.datetime.now().isoformat()
    partner = PARTNERS_DB.get(operator_id)
    
    if not partner:
        return {"status": "error", "message": "Operator not registered in Osare."}

    # Write securely to the Data Layer Ledger (leads.txt)
    with open(LEADS_FILE, "a") as f:
        f.write(f"{timestamp}|SAFARI_PORTAL|{operator_id}|{transport}|{dest}\n")

    # Pass background tasks out immediately to keep the user interface lightning-fast
    lead_details = {"client_type": "Premium Tourist", "vehicle": transport, "destination": dest}
    background_tasks.add_task(
        send_route_enhancer_sms, 
        partner["phone"], 
        partner["name"], 
        partner["base_fee"], 
        lead_details
    )

    # Build the custom WhatsApp tracking redirect
    client_msg = f"Hi {partner['name']}, I found you via the Osare Safari Portal. I'd like to book a {transport} to {dest}. Code: OSARESPECIAL"
    encoded_msg = urllib.parse.quote_plus(client_msg)
    whatsapp_redirect_url = f"https://wa.me/{partner['phone']}?text={encoded_msg}"

    return Response(status_code=303, headers={"Location": whatsapp_redirect_url})
