#!/usr/bin/env python3
"""
OSARE Backend API Test Suite
Tests all API endpoints under /api prefix
"""
import requests
import json
import sys

# Base URL from environment
BASE_URL = "https://mara-guide.preview.emergentagent.com/api"

def print_test(name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {name}")
    if details:
        print(f"   {details}")
    if not passed:
        print()

def test_seed_listings():
    """Test POST /api/seed - should return {inserted: 15}"""
    print("\n=== TEST 1: POST /api/seed ===")
    try:
        response = requests.post(f"{BASE_URL}/seed", timeout=10)
        data = response.json()
        
        # Check status code
        if response.status_code != 200:
            print_test("Seed endpoint status", False, f"Expected 200, got {response.status_code}")
            return False
        
        # Check inserted count
        if data.get("inserted") != 15:
            print_test("Seed inserted count", False, f"Expected 15, got {data.get('inserted')}")
            return False
        
        print_test("Seed endpoint", True, f"Successfully seeded {data['inserted']} listings")
        return True
    except Exception as e:
        print_test("Seed endpoint", False, f"Exception: {str(e)}")
        return False

def test_get_all_listings():
    """Test GET /api/listings - should return 15 listings with UUID ids"""
    print("\n=== TEST 2: GET /api/listings (all) ===")
    try:
        response = requests.get(f"{BASE_URL}/listings", timeout=10)
        data = response.json()
        
        # Check status code
        if response.status_code != 200:
            print_test("Get all listings status", False, f"Expected 200, got {response.status_code}")
            return None
        
        # Check count
        if len(data) != 15:
            print_test("Get all listings count", False, f"Expected 15, got {len(data)}")
            return None
        
        # Check for UUID id and no _id leakage
        for item in data:
            if "_id" in item:
                print_test("No MongoDB _id leakage", False, f"Found _id in listing: {item.get('title')}")
                return None
            if "id" not in item:
                print_test("UUID id present", False, f"Missing id in listing: {item.get('title')}")
                return None
            # Check UUID format (basic check)
            if not isinstance(item["id"], str) or len(item["id"]) < 32:
                print_test("UUID format", False, f"Invalid UUID format: {item['id']}")
                return None
        
        # Check required fields
        required_fields = ["type", "category", "title", "vendor", "priceLabel", "image", "keywords"]
        for item in data:
            for field in required_fields:
                if field not in item:
                    print_test("Required fields", False, f"Missing field '{field}' in listing: {item.get('title')}")
                    return None
        
        print_test("Get all listings", True, f"Retrieved {len(data)} listings with valid UUIDs and fields")
        return data
    except Exception as e:
        print_test("Get all listings", False, f"Exception: {str(e)}")
        return None

def test_filter_by_type_safari():
    """Test GET /api/listings?type=safari - should return exactly 10 items"""
    print("\n=== TEST 3: GET /api/listings?type=safari ===")
    try:
        response = requests.get(f"{BASE_URL}/listings?type=safari", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Filter by type=safari status", False, f"Expected 200, got {response.status_code}")
            return False
        
        if len(data) != 10:
            print_test("Filter by type=safari count", False, f"Expected 10, got {len(data)}")
            return False
        
        # Verify all are safari type
        for item in data:
            if item.get("type") != "safari":
                print_test("Filter by type=safari validation", False, f"Found non-safari item: {item.get('title')}")
                return False
        
        print_test("Filter by type=safari", True, f"Retrieved {len(data)} safari listings")
        return True
    except Exception as e:
        print_test("Filter by type=safari", False, f"Exception: {str(e)}")
        return False

def test_filter_by_type_local():
    """Test GET /api/listings?type=local - should return exactly 5 items"""
    print("\n=== TEST 4: GET /api/listings?type=local ===")
    try:
        response = requests.get(f"{BASE_URL}/listings?type=local", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Filter by type=local status", False, f"Expected 200, got {response.status_code}")
            return False
        
        if len(data) != 5:
            print_test("Filter by type=local count", False, f"Expected 5, got {len(data)}")
            return False
        
        # Verify all are local type
        for item in data:
            if item.get("type") != "local":
                print_test("Filter by type=local validation", False, f"Found non-local item: {item.get('title')}")
                return False
        
        print_test("Filter by type=local", True, f"Retrieved {len(data)} local listings")
        return True
    except Exception as e:
        print_test("Filter by type=local", False, f"Exception: {str(e)}")
        return False

def test_search_kilimanjaro():
    """Test GET /api/listings?q=kilimanjaro - should return at least 1 result"""
    print("\n=== TEST 5: GET /api/listings?q=kilimanjaro ===")
    try:
        response = requests.get(f"{BASE_URL}/listings?q=kilimanjaro", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Search kilimanjaro status", False, f"Expected 200, got {response.status_code}")
            return False
        
        if len(data) < 1:
            print_test("Search kilimanjaro results", False, f"Expected at least 1 result, got {len(data)}")
            return False
        
        # Verify results contain kilimanjaro in title or keywords
        found_match = False
        for item in data:
            title_lower = item.get("title", "").lower()
            keywords = [k.lower() for k in item.get("keywords", [])]
            if "kilimanjaro" in title_lower or "kilimanjaro" in keywords:
                found_match = True
                break
        
        if not found_match:
            print_test("Search kilimanjaro relevance", False, "No results contain 'kilimanjaro' in title or keywords")
            return False
        
        print_test("Search kilimanjaro", True, f"Found {len(data)} results matching 'kilimanjaro'")
        return True
    except Exception as e:
        print_test("Search kilimanjaro", False, f"Exception: {str(e)}")
        return False

def test_filter_by_category():
    """Test GET /api/listings?type=safari&category=Hotel & Resort"""
    print("\n=== TEST 6: GET /api/listings?type=safari&category=Hotel & Resort ===")
    try:
        response = requests.get(f"{BASE_URL}/listings?type=safari&category=Hotel%20%26%20Resort", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Filter by category status", False, f"Expected 200, got {response.status_code}")
            return False
        
        # Should have at least some results
        if len(data) < 1:
            print_test("Filter by category results", False, f"Expected at least 1 result, got {len(data)}")
            return False
        
        # Verify all are Hotel & Resort category
        for item in data:
            if item.get("category") != "Hotel & Resort":
                print_test("Filter by category validation", False, f"Found non-Hotel & Resort item: {item.get('title')} ({item.get('category')})")
                return False
        
        print_test("Filter by category", True, f"Retrieved {len(data)} Hotel & Resort listings")
        return True
    except Exception as e:
        print_test("Filter by category", False, f"Exception: {str(e)}")
        return False

def test_create_listing():
    """Test POST /api/listings - create a new listing"""
    print("\n=== TEST 7: POST /api/listings (create) ===")
    try:
        payload = {
            "type": "safari",
            "category": "Sightseeing",
            "title": "Test Tour",
            "vendor": "Test Vendor",
            "priceValue": 100,
            "currency": "USD",
            "priceLabel": "$100",
            "includes": "A,B,C",
            "keywords": "test,tour"
        }
        
        response = requests.post(f"{BASE_URL}/listings", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Create listing status", False, f"Expected 200, got {response.status_code}: {data}")
            return None
        
        # Check for UUID id
        if "id" not in data:
            print_test("Create listing id", False, "Missing id in response")
            return None
        
        if "_id" in data:
            print_test("Create listing no _id", False, "Found MongoDB _id in response")
            return None
        
        # Check includes and keywords are arrays
        if not isinstance(data.get("includes"), list):
            print_test("Create listing includes array", False, f"includes should be array, got {type(data.get('includes'))}")
            return None
        
        if not isinstance(data.get("keywords"), list):
            print_test("Create listing keywords array", False, f"keywords should be array, got {type(data.get('keywords'))}")
            return None
        
        print_test("Create listing", True, f"Created listing with id: {data['id']}")
        return data["id"]
    except Exception as e:
        print_test("Create listing", False, f"Exception: {str(e)}")
        return None

def test_update_listing(listing_id):
    """Test PUT /api/listings/:id - update a listing"""
    print("\n=== TEST 8: PUT /api/listings/:id (update) ===")
    if not listing_id:
        print_test("Update listing", False, "No listing_id provided (create test failed)")
        return False
    
    try:
        payload = {
            "priceLabel": "$120",
            "priceValue": 120
        }
        
        response = requests.put(f"{BASE_URL}/listings/{listing_id}", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Update listing status", False, f"Expected 200, got {response.status_code}: {data}")
            return False
        
        # Check updated values
        if data.get("priceLabel") != "$120":
            print_test("Update listing priceLabel", False, f"Expected '$120', got {data.get('priceLabel')}")
            return False
        
        if data.get("priceValue") != 120:
            print_test("Update listing priceValue", False, f"Expected 120, got {data.get('priceValue')}")
            return False
        
        print_test("Update listing", True, f"Updated listing {listing_id} with new price")
        return True
    except Exception as e:
        print_test("Update listing", False, f"Exception: {str(e)}")
        return False

def test_delete_listing(listing_id):
    """Test DELETE /api/listings/:id - delete a listing"""
    print("\n=== TEST 9: DELETE /api/listings/:id ===")
    if not listing_id:
        print_test("Delete listing", False, "No listing_id provided (create test failed)")
        return False
    
    try:
        response = requests.delete(f"{BASE_URL}/listings/{listing_id}", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Delete listing status", False, f"Expected 200, got {response.status_code}: {data}")
            return False
        
        if not data.get("deleted"):
            print_test("Delete listing response", False, f"Expected deleted=true, got {data}")
            return False
        
        # Verify it's gone
        verify_response = requests.get(f"{BASE_URL}/listings", timeout=10)
        all_listings = verify_response.json()
        for item in all_listings:
            if item.get("id") == listing_id:
                print_test("Delete listing verification", False, f"Listing {listing_id} still exists after deletion")
                return False
        
        print_test("Delete listing", True, f"Deleted listing {listing_id} and verified removal")
        return True
    except Exception as e:
        print_test("Delete listing", False, f"Exception: {str(e)}")
        return False

def test_create_lead(listings):
    """Test POST /api/leads - create a booking lead"""
    print("\n=== TEST 10: POST /api/leads (with listingId) ===")
    if not listings or len(listings) == 0:
        print_test("Create lead", False, "No listings available (get listings test failed)")
        return None
    
    try:
        # Use first listing
        listing_id = listings[0]["id"]
        payload = {"listingId": listing_id}
        
        response = requests.post(f"{BASE_URL}/leads", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Create lead status", False, f"Expected 200, got {response.status_code}: {data}")
            return None
        
        # Check for UUID id
        if "id" not in data:
            print_test("Create lead id", False, "Missing id in response")
            return None
        
        if "_id" in data:
            print_test("Create lead no _id", False, "Found MongoDB _id in response")
            return None
        
        # Check whatsappUrl
        if "whatsappUrl" not in data:
            print_test("Create lead whatsappUrl", False, "Missing whatsappUrl in response")
            return None
        
        if "wa.me/254758378729" not in data["whatsappUrl"]:
            print_test("Create lead whatsappUrl format", False, f"whatsappUrl doesn't contain wa.me/254758378729: {data['whatsappUrl']}")
            return None
        
        # Check commission
        if "commission" not in data:
            print_test("Create lead commission", False, "Missing commission in response")
            return None
        
        if not isinstance(data["commission"], (int, float)):
            print_test("Create lead commission type", False, f"commission should be numeric, got {type(data['commission'])}")
            return None
        
        # Verify commission is 5% of priceValue
        expected_commission = listings[0]["priceValue"] * 0.05
        if abs(data["commission"] - expected_commission) > 0.01:
            print_test("Create lead commission value", False, f"Expected {expected_commission}, got {data['commission']}")
            return None
        
        print_test("Create lead", True, f"Created lead with id: {data['id']}, commission: {data['commission']}")
        return data["id"]
    except Exception as e:
        print_test("Create lead", False, f"Exception: {str(e)}")
        return None

def test_create_lead_fallback():
    """Test POST /api/leads with non-existent listingId and inline data"""
    print("\n=== TEST 11: POST /api/leads (fallback with inline data) ===")
    try:
        payload = {
            "listingId": "non-existent-id",
            "title": "Fallback Tour",
            "priceValue": 200,
            "currency": "USD"
        }
        
        response = requests.post(f"{BASE_URL}/leads", json=payload, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Create lead fallback status", False, f"Expected 200, got {response.status_code}: {data}")
            return False
        
        # Check whatsappUrl still works
        if "whatsappUrl" not in data:
            print_test("Create lead fallback whatsappUrl", False, "Missing whatsappUrl in response")
            return False
        
        if "wa.me/254758378729" not in data["whatsappUrl"]:
            print_test("Create lead fallback whatsappUrl format", False, f"whatsappUrl doesn't contain wa.me/254758378729")
            return False
        
        print_test("Create lead fallback", True, "Fallback lead creation works with inline data")
        return True
    except Exception as e:
        print_test("Create lead fallback", False, f"Exception: {str(e)}")
        return False

def test_get_leads():
    """Test GET /api/leads - list all leads"""
    print("\n=== TEST 12: GET /api/leads ===")
    try:
        response = requests.get(f"{BASE_URL}/leads", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Get leads status", False, f"Expected 200, got {response.status_code}")
            return False
        
        # Should have at least the leads we created
        if len(data) < 1:
            print_test("Get leads count", False, f"Expected at least 1 lead, got {len(data)}")
            return False
        
        # Check for UUID id and no _id leakage
        for item in data:
            if "_id" in item:
                print_test("Get leads no _id", False, f"Found _id in lead")
                return False
            if "id" not in item:
                print_test("Get leads id", False, f"Missing id in lead")
                return False
        
        print_test("Get leads", True, f"Retrieved {len(data)} leads with valid UUIDs")
        return True
    except Exception as e:
        print_test("Get leads", False, f"Exception: {str(e)}")
        return False

def test_get_stats():
    """Test GET /api/stats - dashboard statistics"""
    print("\n=== TEST 13: GET /api/stats ===")
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            print_test("Get stats status", False, f"Expected 200, got {response.status_code}")
            return False
        
        # Check required fields
        required_fields = ["totalListings", "safariCount", "localCount", "totalLeads", "estRevenueUSD", "leadsByType", "leadsByCategory"]
        for field in required_fields:
            if field not in data:
                print_test("Get stats fields", False, f"Missing field: {field}")
                return False
        
        # Check numeric fields
        numeric_fields = ["totalListings", "safariCount", "localCount", "totalLeads", "estRevenueUSD"]
        for field in numeric_fields:
            if not isinstance(data[field], (int, float)):
                print_test("Get stats numeric", False, f"{field} should be numeric, got {type(data[field])}")
                return False
        
        # Check leadsByType structure
        if not isinstance(data["leadsByType"], dict):
            print_test("Get stats leadsByType", False, f"leadsByType should be object, got {type(data['leadsByType'])}")
            return False
        
        if "safari" not in data["leadsByType"] or "local" not in data["leadsByType"]:
            print_test("Get stats leadsByType keys", False, f"leadsByType missing safari or local keys")
            return False
        
        # Check leadsByCategory structure
        if not isinstance(data["leadsByCategory"], list):
            print_test("Get stats leadsByCategory", False, f"leadsByCategory should be array, got {type(data['leadsByCategory'])}")
            return False
        
        print_test("Get stats", True, f"Stats: {data['totalListings']} listings, {data['totalLeads']} leads, ${data['estRevenueUSD']} revenue")
        return True
    except Exception as e:
        print_test("Get stats", False, f"Exception: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("OSARE Backend API Test Suite")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    
    results = []
    
    # Test 1: Seed
    results.append(("Seed listings", test_seed_listings()))
    
    # Test 2: Get all listings
    all_listings = test_get_all_listings()
    results.append(("Get all listings", all_listings is not None))
    
    # Test 3-6: Filters and search
    results.append(("Filter by type=safari", test_filter_by_type_safari()))
    results.append(("Filter by type=local", test_filter_by_type_local()))
    results.append(("Search kilimanjaro", test_search_kilimanjaro()))
    results.append(("Filter by category", test_filter_by_category()))
    
    # Test 7-9: CRUD operations
    created_id = test_create_listing()
    results.append(("Create listing", created_id is not None))
    results.append(("Update listing", test_update_listing(created_id)))
    results.append(("Delete listing", test_delete_listing(created_id)))
    
    # Test 10-12: Leads
    lead_id = test_create_lead(all_listings)
    results.append(("Create lead", lead_id is not None))
    results.append(("Create lead fallback", test_create_lead_fallback()))
    results.append(("Get leads", test_get_leads()))
    
    # Test 13: Stats
    results.append(("Get stats", test_get_stats()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed:")
        for name, result in results:
            if not result:
                print(f"  - {name}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
