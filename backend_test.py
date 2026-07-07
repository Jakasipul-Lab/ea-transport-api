#!/usr/bin/env python3
"""
OSARE Backend Test Suite - PostgreSQL Migration Verification
Tests all endpoints end-to-end against PostgreSQL (NEON)
"""

import requests
import json
import random
import string
from typing import Dict, Any

# Base URL from .env
BASE_URL = "https://mara-guide.preview.emergentagent.com/api"

# Test results tracking
test_results = []
created_listing_id = None
vendor_token = None
vendor_id = None
vendor_email = None
owned_listing_id = None


def log_test(step: str, passed: bool, details: str = ""):
    """Log test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    result = f"{status}: {step}"
    if details:
        result += f" - {details}"
    print(result)
    test_results.append({"step": step, "passed": passed, "details": details})


def random_email():
    """Generate random email for testing"""
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"pg+{rand}@test.com"


def test_1_seed():
    """Test 1: POST /api/seed -> {inserted:15}"""
    print("\n=== TEST 1: Seed Listings ===")
    try:
        response = requests.post(f"{BASE_URL}/seed", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and data.get("inserted") == 15:
            log_test("POST /api/seed", True, f"Successfully seeded {data['inserted']} listings")
            return True
        else:
            log_test("POST /api/seed", False, f"Expected inserted=15, got {data}")
            return False
    except Exception as e:
        log_test("POST /api/seed", False, f"Exception: {str(e)}")
        return False


def test_2_get_listings():
    """Test 2: GET /api/listings with various filters"""
    print("\n=== TEST 2: Get Listings with Filters ===")
    all_passed = True
    
    # Test 2a: Get all listings
    try:
        response = requests.get(f"{BASE_URL}/listings", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and len(data) == 15:
            # Check first item structure
            item = data[0]
            required_fields = ['id', 'type', 'category', 'title', 'vendor', 'priceLabel', 'image', 'includes', 'keywords']
            missing_fields = [f for f in required_fields if f not in item]
            
            # Check UUID format (no MongoDB _id)
            has_uuid = isinstance(item['id'], str) and len(item['id']) == 36 and '-' in item['id']
            has_mongo_id = '_id' in item
            
            # Check arrays are JSON arrays
            includes_is_array = isinstance(item.get('includes'), list)
            keywords_is_array = isinstance(item.get('keywords'), list)
            
            if missing_fields:
                log_test("GET /api/listings (all)", False, f"Missing fields: {missing_fields}")
                all_passed = False
            elif has_mongo_id:
                log_test("GET /api/listings (all)", False, "MongoDB _id leaked in response")
                all_passed = False
            elif not has_uuid:
                log_test("GET /api/listings (all)", False, f"ID is not UUID format: {item['id']}")
                all_passed = False
            elif not includes_is_array or not keywords_is_array:
                log_test("GET /api/listings (all)", False, f"includes or keywords not arrays: includes={type(item.get('includes'))}, keywords={type(item.get('keywords'))}")
                all_passed = False
            else:
                log_test("GET /api/listings (all)", True, f"Returns 15 items with UUID ids, all required fields, includes/keywords as arrays")
        else:
            log_test("GET /api/listings (all)", False, f"Expected 15 items, got {len(data)}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/listings (all)", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 2b: Filter by type=safari
    try:
        response = requests.get(f"{BASE_URL}/listings?type=safari", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and len(data) == 10:
            log_test("GET /api/listings?type=safari", True, f"Returns 10 safari listings")
        else:
            log_test("GET /api/listings?type=safari", False, f"Expected 10 items, got {len(data)}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/listings?type=safari", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 2c: Filter by type=local
    try:
        response = requests.get(f"{BASE_URL}/listings?type=local", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and len(data) == 5:
            log_test("GET /api/listings?type=local", True, f"Returns 5 local listings")
        else:
            log_test("GET /api/listings?type=local", False, f"Expected 5 items, got {len(data)}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/listings?type=local", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 2d: Search query q=kilimanjaro
    try:
        response = requests.get(f"{BASE_URL}/listings?q=kilimanjaro", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and len(data) >= 1:
            log_test("GET /api/listings?q=kilimanjaro", True, f"Returns {len(data)} results")
        else:
            log_test("GET /api/listings?q=kilimanjaro", False, f"Expected >=1 results, got {len(data)}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/listings?q=kilimanjaro", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 2e: Filter by category
    try:
        response = requests.get(f"{BASE_URL}/listings?category=Hotel%20%26%20Resort", timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            # Check all results are Hotel & Resort category
            all_correct = all(item.get('category') == 'Hotel & Resort' for item in data)
            if all_correct and len(data) > 0:
                log_test("GET /api/listings?category=Hotel & Resort", True, f"Returns {len(data)} Hotel & Resort listings only")
            else:
                log_test("GET /api/listings?category=Hotel & Resort", False, f"Category filter not working correctly")
                all_passed = False
        else:
            log_test("GET /api/listings?category=Hotel & Resort", False, f"Request failed with status {response.status_code}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/listings?category=Hotel & Resort", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_3_crud_listings():
    """Test 3: POST/PUT/DELETE /api/listings"""
    print("\n=== TEST 3: CRUD Operations ===")
    global created_listing_id
    all_passed = True
    
    # Test 3a: Create listing
    try:
        payload = {
            "type": "safari",
            "category": "Sightseeing",
            "title": "PG Test Tour",
            "vendor": "PG Vendor",
            "priceValue": 100,
            "currency": "USD",
            "priceLabel": "$100",
            "includes": "A,B,C",
            "keywords": "pg,tour"
        }
        response = requests.post(f"{BASE_URL}/listings", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            # Check UUID id
            has_uuid = isinstance(data.get('id'), str) and len(data['id']) == 36 and '-' in data['id']
            # Check includes/keywords parsed to arrays
            includes_is_array = isinstance(data.get('includes'), list) and len(data['includes']) == 3
            keywords_is_array = isinstance(data.get('keywords'), list) and len(data['keywords']) == 2
            
            if has_uuid and includes_is_array and keywords_is_array:
                created_listing_id = data['id']
                log_test("POST /api/listings", True, f"Created listing with UUID id={created_listing_id[:8]}..., includes/keywords parsed to arrays")
            else:
                log_test("POST /api/listings", False, f"UUID or array parsing issue: uuid={has_uuid}, includes={includes_is_array}, keywords={keywords_is_array}")
                all_passed = False
        else:
            log_test("POST /api/listings", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/listings", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 3b: Update listing
    if created_listing_id:
        try:
            payload = {
                "priceLabel": "$120",
                "priceValue": 120
            }
            response = requests.put(f"{BASE_URL}/listings/{created_listing_id}", json=payload, timeout=30)
            data = response.json()
            
            if response.status_code == 200:
                # Check priceValue is numeric, not string
                price_is_numeric = isinstance(data.get('priceValue'), (int, float)) and data['priceValue'] == 120
                price_label_correct = data.get('priceLabel') == "$120"
                
                if price_is_numeric and price_label_correct:
                    log_test("PUT /api/listings/:id", True, f"Updated listing: priceValue={data['priceValue']} (numeric), priceLabel={data['priceLabel']}")
                else:
                    log_test("PUT /api/listings/:id", False, f"priceValue type issue or incorrect value: priceValue={data.get('priceValue')} (type={type(data.get('priceValue'))}), priceLabel={data.get('priceLabel')}")
                    all_passed = False
            else:
                log_test("PUT /api/listings/:id", False, f"Status {response.status_code}: {data}")
                all_passed = False
        except Exception as e:
            log_test("PUT /api/listings/:id", False, f"Exception: {str(e)}")
            all_passed = False
    
    # Test 3c: Delete listing
    if created_listing_id:
        try:
            response = requests.delete(f"{BASE_URL}/listings/{created_listing_id}", timeout=30)
            data = response.json()
            
            if response.status_code == 200 and data.get('deleted') == True:
                log_test("DELETE /api/listings/:id", True, f"Deleted listing {created_listing_id[:8]}...")
                
                # Verify deletion
                verify_response = requests.get(f"{BASE_URL}/listings", timeout=30)
                verify_data = verify_response.json()
                still_exists = any(item['id'] == created_listing_id for item in verify_data)
                
                if not still_exists:
                    log_test("DELETE verification", True, "Listing confirmed removed from GET /api/listings")
                else:
                    log_test("DELETE verification", False, "Listing still exists after deletion")
                    all_passed = False
            else:
                log_test("DELETE /api/listings/:id", False, f"Status {response.status_code}: {data}")
                all_passed = False
        except Exception as e:
            log_test("DELETE /api/listings/:id", False, f"Exception: {str(e)}")
            all_passed = False
    
    return all_passed


def test_4_leads():
    """Test 4: POST /api/leads with valid listingId and fallback"""
    print("\n=== TEST 4: Create Leads ===")
    all_passed = True
    
    # Get a listing id first
    try:
        response = requests.get(f"{BASE_URL}/listings?type=safari", timeout=30)
        listings = response.json()
        if not listings:
            log_test("POST /api/leads (setup)", False, "No listings available for testing")
            return False
        
        listing_id = listings[0]['id']
        listing_price = listings[0].get('priceValue', 0)
        
        # Test 4a: Create lead with valid listingId
        payload = {"listingId": listing_id}
        response = requests.post(f"{BASE_URL}/leads", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            # Check UUID id
            has_uuid = isinstance(data.get('id'), str) and len(data['id']) == 36 and '-' in data['id']
            # Check whatsappUrl
            has_whatsapp = 'whatsappUrl' in data and 'wa.me/254758378729' in data['whatsappUrl']
            # Check commission is numeric and 5% of priceValue
            commission_is_numeric = isinstance(data.get('commission'), (int, float))
            expected_commission = round(listing_price * 0.05, 2)
            commission_correct = abs(data.get('commission', 0) - expected_commission) < 0.01
            
            if has_uuid and has_whatsapp and commission_is_numeric and commission_correct:
                log_test("POST /api/leads (valid listingId)", True, f"UUID id, whatsappUrl contains wa.me/254758378729, commission={data['commission']} (5% of {listing_price})")
            else:
                log_test("POST /api/leads (valid listingId)", False, f"Issues: uuid={has_uuid}, whatsapp={has_whatsapp}, commission_numeric={commission_is_numeric}, commission_correct={commission_correct} (expected={expected_commission}, got={data.get('commission')})")
                all_passed = False
        else:
            log_test("POST /api/leads (valid listingId)", False, f"Status {response.status_code}: {data}")
            all_passed = False
        
        # Test 4b: Create lead with fake listingId + inline data (fallback)
        fake_id = "00000000-0000-0000-0000-000000000000"
        payload = {
            "listingId": fake_id,
            "title": "Fallback Test Tour",
            "priceValue": 200,
            "currency": "USD"
        }
        response = requests.post(f"{BASE_URL}/leads", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            has_whatsapp = 'whatsappUrl' in data and 'wa.me/254758378729' in data['whatsappUrl']
            if has_whatsapp:
                log_test("POST /api/leads (fallback)", True, "Fallback with inline data works, whatsappUrl present")
            else:
                log_test("POST /api/leads (fallback)", False, "whatsappUrl not present in fallback response")
                all_passed = False
        else:
            log_test("POST /api/leads (fallback)", False, f"Status {response.status_code}: {data}")
            all_passed = False
            
    except Exception as e:
        log_test("POST /api/leads", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_5_leads_and_stats():
    """Test 5: GET /api/leads and GET /api/stats"""
    print("\n=== TEST 5: Get Leads and Stats ===")
    all_passed = True
    
    # Test 5a: GET /api/leads
    try:
        response = requests.get(f"{BASE_URL}/leads", timeout=30)
        data = response.json()
        
        if response.status_code == 200 and isinstance(data, list):
            if len(data) > 0:
                # Check first lead has UUID id and no _id
                lead = data[0]
                has_uuid = isinstance(lead.get('id'), str) and len(lead['id']) == 36 and '-' in lead['id']
                has_mongo_id = '_id' in lead
                
                if has_uuid and not has_mongo_id:
                    log_test("GET /api/leads", True, f"Returns array with {len(data)} leads, UUID ids, no _id leakage")
                else:
                    log_test("GET /api/leads", False, f"UUID or _id issue: uuid={has_uuid}, has_mongo_id={has_mongo_id}")
                    all_passed = False
            else:
                log_test("GET /api/leads", True, "Returns empty array (no leads yet)")
        else:
            log_test("GET /api/leads", False, f"Status {response.status_code} or not array: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/leads", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 5b: GET /api/stats
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            required_fields = ['totalListings', 'safariCount', 'localCount', 'totalLeads', 'estRevenueUSD', 'leadsByType', 'leadsByCategory']
            missing_fields = [f for f in required_fields if f not in data]
            
            # Check numeric fields
            numeric_fields = ['totalListings', 'safariCount', 'localCount', 'totalLeads', 'estRevenueUSD']
            all_numeric = all(isinstance(data.get(f), (int, float)) for f in numeric_fields)
            
            # Check structure
            leads_by_type_is_object = isinstance(data.get('leadsByType'), dict)
            leads_by_category_is_array = isinstance(data.get('leadsByCategory'), list)
            
            if not missing_fields and all_numeric and leads_by_type_is_object and leads_by_category_is_array:
                log_test("GET /api/stats", True, f"All required fields present, numeric fields are numbers, correct structure: totalListings={data['totalListings']}, safariCount={data['safariCount']}, localCount={data['localCount']}, totalLeads={data['totalLeads']}, estRevenueUSD={data['estRevenueUSD']}")
            else:
                log_test("GET /api/stats", False, f"Issues: missing={missing_fields}, all_numeric={all_numeric}, leadsByType_object={leads_by_type_is_object}, leadsByCategory_array={leads_by_category_is_array}")
                all_passed = False
        else:
            log_test("GET /api/stats", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/stats", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_6_vendor_register():
    """Test 6: POST /api/auth/register"""
    print("\n=== TEST 6: Vendor Registration ===")
    global vendor_token, vendor_id, vendor_email
    all_passed = True
    
    # Test 6a: Register new vendor
    try:
        vendor_email = random_email()
        payload = {
            "name": "Test Vendor",
            "company": "Test Company",
            "email": vendor_email,
            "phone": "+254700000000",
            "password": "secret123"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            has_token = 'token' in data and isinstance(data['token'], str)
            has_vendor = 'vendor' in data and isinstance(data['vendor'], dict)
            
            if has_vendor:
                vendor = data['vendor']
                has_password_hash = 'password_hash' in vendor or 'passwordHash' in vendor
                has_mongo_id = '_id' in vendor
                has_uuid = 'id' in vendor and isinstance(vendor['id'], str) and len(vendor['id']) == 36
                
                if has_token and has_vendor and not has_password_hash and not has_mongo_id and has_uuid:
                    vendor_token = data['token']
                    vendor_id = vendor['id']
                    log_test("POST /api/auth/register", True, f"Returns 200 with token and vendor (UUID id, no password_hash, no _id)")
                else:
                    log_test("POST /api/auth/register", False, f"Issues: token={has_token}, vendor={has_vendor}, password_leaked={has_password_hash}, mongo_id={has_mongo_id}, uuid={has_uuid}")
                    all_passed = False
            else:
                log_test("POST /api/auth/register", False, "No vendor object in response")
                all_passed = False
        else:
            log_test("POST /api/auth/register", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/auth/register", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 6b: Register duplicate email
    try:
        payload = {
            "name": "Duplicate",
            "company": "Duplicate Co",
            "email": vendor_email,
            "phone": "+254700000001",
            "password": "secret456"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 409:
            log_test("POST /api/auth/register (duplicate)", True, "Correctly returns 409 for duplicate email")
        else:
            log_test("POST /api/auth/register (duplicate)", False, f"Expected 409, got {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/auth/register (duplicate)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_7_vendor_login():
    """Test 7: POST /api/auth/login"""
    print("\n=== TEST 7: Vendor Login ===")
    all_passed = True
    
    # Test 7a: Login with correct credentials
    try:
        payload = {
            "email": vendor_email,
            "password": "secret123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            has_token = 'token' in data and isinstance(data['token'], str)
            has_vendor = 'vendor' in data and isinstance(data['vendor'], dict)
            
            if has_vendor:
                vendor = data['vendor']
                has_password_hash = 'password_hash' in vendor or 'passwordHash' in vendor
                
                if has_token and has_vendor and not has_password_hash:
                    log_test("POST /api/auth/login", True, "Returns 200 with token and vendor (no password_hash)")
                else:
                    log_test("POST /api/auth/login", False, f"Issues: token={has_token}, vendor={has_vendor}, password_leaked={has_password_hash}")
                    all_passed = False
            else:
                log_test("POST /api/auth/login", False, "No vendor object in response")
                all_passed = False
        else:
            log_test("POST /api/auth/login", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/auth/login", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 7b: Login with wrong password
    try:
        payload = {
            "email": vendor_email,
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 401:
            log_test("POST /api/auth/login (wrong password)", True, "Correctly returns 401 for wrong password")
        else:
            log_test("POST /api/auth/login (wrong password)", False, f"Expected 401, got {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/auth/login (wrong password)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_8_vendor_me():
    """Test 8: GET /api/auth/me"""
    print("\n=== TEST 8: Get Vendor Profile ===")
    all_passed = True
    
    # Test 8a: GET /api/auth/me with valid token
    try:
        headers = {"Authorization": f"Bearer {vendor_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            has_vendor = 'vendor' in data and isinstance(data['vendor'], dict)
            
            if has_vendor:
                vendor = data['vendor']
                has_password_hash = 'password_hash' in vendor or 'passwordHash' in vendor
                
                if not has_password_hash:
                    log_test("GET /api/auth/me (with token)", True, "Returns vendor info (no password_hash)")
                else:
                    log_test("GET /api/auth/me (with token)", False, "password_hash leaked in response")
                    all_passed = False
            else:
                log_test("GET /api/auth/me (with token)", False, "No vendor object in response")
                all_passed = False
        else:
            log_test("GET /api/auth/me (with token)", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/auth/me (with token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 8b: GET /api/auth/me without token
    try:
        response = requests.get(f"{BASE_URL}/auth/me", timeout=30)
        data = response.json()
        
        if response.status_code == 401:
            log_test("GET /api/auth/me (no token)", True, "Correctly returns 401 without token")
        else:
            log_test("GET /api/auth/me (no token)", False, f"Expected 401, got {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/auth/me (no token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_9_vendor_create_listing():
    """Test 9: POST /api/listings with Bearer token (ownerId check)"""
    print("\n=== TEST 9: Vendor Create Listing ===")
    global owned_listing_id
    all_passed = True
    
    try:
        headers = {"Authorization": f"Bearer {vendor_token}"}
        payload = {
            "type": "safari",
            "category": "Sightseeing",
            "title": "Owned Tour",
            "priceValue": 200,
            "currency": "USD",
            "priceLabel": "$200"
        }
        response = requests.post(f"{BASE_URL}/listings", json=payload, headers=headers, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            owner_id = data.get('ownerId')
            if owner_id == vendor_id:
                owned_listing_id = data['id']
                log_test("POST /api/listings (with Bearer)", True, f"ownerId={owner_id[:8]}... matches vendor.id")
            else:
                log_test("POST /api/listings (with Bearer)", False, f"ownerId mismatch: expected {vendor_id}, got {owner_id}")
                all_passed = False
        else:
            log_test("POST /api/listings (with Bearer)", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/listings (with Bearer)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_10_vendor_my_listings():
    """Test 10: GET /api/my-listings"""
    print("\n=== TEST 10: Get Vendor's Listings ===")
    all_passed = True
    
    # Test 10a: GET /api/my-listings with token
    try:
        headers = {"Authorization": f"Bearer {vendor_token}"}
        response = requests.get(f"{BASE_URL}/my-listings", headers=headers, timeout=30)
        data = response.json()
        
        if response.status_code == 200 and isinstance(data, list):
            if len(data) > 0:
                # Check that owned listing is in the list
                has_owned = any(item['id'] == owned_listing_id for item in data)
                # Check all listings have matching ownerId
                all_owned = all(item.get('ownerId') == vendor_id for item in data)
                
                if has_owned and all_owned:
                    log_test("GET /api/my-listings (with token)", True, f"Returns {len(data)} vendor's listings, all with matching ownerId")
                else:
                    log_test("GET /api/my-listings (with token)", False, f"Issues: has_owned={has_owned}, all_owned={all_owned}")
                    all_passed = False
            else:
                log_test("GET /api/my-listings (with token)", False, "Expected at least 1 listing, got 0")
                all_passed = False
        else:
            log_test("GET /api/my-listings (with token)", False, f"Status {response.status_code} or not array: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/my-listings (with token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 10b: GET /api/my-listings without token
    try:
        response = requests.get(f"{BASE_URL}/my-listings", timeout=30)
        data = response.json()
        
        if response.status_code == 401:
            log_test("GET /api/my-listings (no token)", True, "Correctly returns 401 without token")
        else:
            log_test("GET /api/my-listings (no token)", False, f"Expected 401, got {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/my-listings (no token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def test_11_vendor_my_stats():
    """Test 11: POST /api/leads for vendor's listing and GET /api/my-stats"""
    print("\n=== TEST 11: Vendor Stats ===")
    all_passed = True
    
    # Test 11a: Create lead for vendor's listing
    try:
        payload = {"listingId": owned_listing_id}
        response = requests.post(f"{BASE_URL}/leads", json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            log_test("POST /api/leads (vendor's listing)", True, "Lead created for vendor's listing")
        else:
            log_test("POST /api/leads (vendor's listing)", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("POST /api/leads (vendor's listing)", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 11b: GET /api/my-stats with token
    try:
        headers = {"Authorization": f"Bearer {vendor_token}"}
        response = requests.get(f"{BASE_URL}/my-stats", headers=headers, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            required_fields = ['listings', 'leads', 'commissionOwedUSD', 'recentLeads']
            missing_fields = [f for f in required_fields if f not in data]
            
            # Check values
            has_listing = data.get('listings', 0) >= 1
            has_lead = data.get('leads', 0) >= 1
            # Commission should be ~$10 (5% of $200)
            commission = data.get('commissionOwedUSD', 0)
            commission_correct = abs(commission - 10.0) < 0.5
            
            if not missing_fields and has_listing and has_lead and commission_correct:
                log_test("GET /api/my-stats (with token)", True, f"Returns correct stats: listings={data['listings']}, leads={data['leads']}, commissionOwedUSD={commission} (~$10 = 5% of $200)")
            else:
                log_test("GET /api/my-stats (with token)", False, f"Issues: missing={missing_fields}, has_listing={has_listing}, has_lead={has_lead}, commission_correct={commission_correct} (expected ~10, got {commission})")
                all_passed = False
        else:
            log_test("GET /api/my-stats (with token)", False, f"Status {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/my-stats (with token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    # Test 11c: GET /api/my-stats without token
    try:
        response = requests.get(f"{BASE_URL}/my-stats", timeout=30)
        data = response.json()
        
        if response.status_code == 401:
            log_test("GET /api/my-stats (no token)", True, "Correctly returns 401 without token")
        else:
            log_test("GET /api/my-stats (no token)", False, f"Expected 401, got {response.status_code}: {data}")
            all_passed = False
    except Exception as e:
        log_test("GET /api/my-stats (no token)", False, f"Exception: {str(e)}")
        all_passed = False
    
    return all_passed


def main():
    """Run all tests"""
    print("=" * 80)
    print("OSARE BACKEND TEST SUITE - PostgreSQL Migration Verification")
    print("=" * 80)
    print(f"Base URL: {BASE_URL}")
    print("=" * 80)
    
    # Run all tests in sequence
    tests = [
        test_1_seed,
        test_2_get_listings,
        test_3_crud_listings,
        test_4_leads,
        test_5_leads_and_stats,
        test_6_vendor_register,
        test_7_vendor_login,
        test_8_vendor_me,
        test_9_vendor_create_listing,
        test_10_vendor_my_listings,
        test_11_vendor_my_stats,
    ]
    
    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test_func.__name__}: {str(e)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in test_results if r['passed'])
    failed = sum(1 for r in test_results if not r['passed'])
    total = len(test_results)
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed > 0:
        print("\n❌ FAILED TESTS:")
        for r in test_results:
            if not r['passed']:
                print(f"  - {r['step']}: {r['details']}")
    
    print("\n" + "=" * 80)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! PostgreSQL migration successful.")
    else:
        print(f"⚠️  {failed} test(s) failed. Review details above.")
    
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
