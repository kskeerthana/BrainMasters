
import requests
import sys
import time
from datetime import datetime

class InstagramBotAPITester:
    def __init__(self, base_url="https://36bd9c5a-4f33-4f69-b1e9-22a0c30e5d9b.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                print(f"Response: {response.json()}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.text:
                    print(f"Response: {response.text}")

            return success, response.json() if success else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_status(self):
        """Test the status endpoint"""
        return self.run_test(
            "Bot Status",
            "GET",
            "api/status",
            200
        )

    def test_stats(self):
        """Test the stats endpoint"""
        return self.run_test(
            "Bot Stats",
            "GET",
            "api/stats",
            200
        )

    def test_start_scraping(self):
        """Test starting a scraping job"""
        return self.run_test(
            "Start Scraping",
            "POST",
            "api/scraping/start",
            200,
            data={}
        )

    def test_start_scheduler(self):
        """Test starting the scheduler"""
        return self.run_test(
            "Start Scheduler",
            "POST",
            "api/scheduler/start",
            200,
            data={}
        )

    def test_stop_scheduler(self):
        """Test stopping the scheduler"""
        return self.run_test(
            "Stop Scheduler",
            "POST",
            "api/scheduler/stop",
            200,
            data={}
        )

def main():
    # Setup
    tester = InstagramBotAPITester()
    
    # Run tests
    tester.test_status()
    tester.test_stats()
    tester.test_start_scraping()
    tester.test_start_scheduler()
    time.sleep(2)  # Wait a bit before stopping
    tester.test_stop_scheduler()

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
