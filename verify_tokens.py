import requests
import json
import os
from datetime import datetime
from pathlib import Path

class DiscordTokenVerifier:
    def __init__(self):
        self.discord_api_url = "https://discordapp.com/api/v9"
        self.results = []
    
    def verify_token(self, token):
        """Verify a single Discord token and retrieve user information"""
        try:
            headers = {
                "Authorization": token,
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.get(
                f"{self.discord_api_url}/users/@me",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "token": token,
                    "valid": True,
                    "username": user_data.get("username", "N/A"),
                    "user_id": user_data.get("id", "N/A"),
                    "email": user_data.get("email", "N/A"),
                    "avatar": user_data.get("avatar", "N/A"),
                    "created_at": self.get_creation_date(user_data.get("id")),
                    "verified": user_data.get("verified", False),
                    "mfa_enabled": user_data.get("mfa_enabled", False),
                    "status": "Valid Token"
                }
            elif response.status_code == 401:
                return {
                    "token": token,
                    "valid": False,
                    "username": "N/A",
                    "user_id": "N/A",
                    "email": "N/A",
                    "avatar": "N/A",
                    "created_at": "N/A",
                    "verified": False,
                    "mfa_enabled": False,
                    "status": "Invalid Token - Unauthorized"
                }
            else:
                return {
                    "token": token,
                    "valid": False,
                    "username": "N/A",
                    "user_id": "N/A",
                    "email": "N/A",
                    "avatar": "N/A",
                    "created_at": "N/A",
                    "verified": False,
                    "mfa_enabled": False,
                    "status": f"Error - HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "token": token,
                "valid": False,
                "username": "N/A",
                "user_id": "N/A",
                "email": "N/A",
                "avatar": "N/A",
                "created_at": "N/A",
                "verified": False,
                "mfa_enabled": False,
                "status": f"Connection Error: {str(e)}"
            }
        except Exception as e:
            return {
                "token": token,
                "valid": False,
                "username": "N/A",
                "user_id": "N/A",
                "email": "N/A",
                "avatar": "N/A",
                "created_at": "N/A",
                "verified": False,
                "mfa_enabled": False,
                "status": f"Error: {str(e)}"
            }
    
    def get_creation_date(self, user_id):
        """Calculate Discord account creation date from user ID (snowflake)"""
        try:
            if user_id:
                timestamp = (int(user_id) >> 22) + 1420070400000
                creation_date = datetime.fromtimestamp(timestamp / 1000)
                return creation_date.strftime("%Y-%m-%d %H:%M:%S")
            return "N/A"
        except:
            return "N/A"
    
    def verify_from_file(self, file_path):
        """Verify tokens from a file"""
        try:
            with open(file_path, 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
            
            print(f"\n[*] Found {len(tokens)} token(s) to verify")
            print("[*] Starting verification...\n")
            
            for token in tokens:
                result = self.verify_token(token)
                self.results.append(result)
                
                status_icon = "✓" if result["valid"] else "✗"
                print(f"{status_icon} Token: {token[:20]}... | Status: {result['status']}")
                if result["valid"]:
                    print(f"   Username: {result['username']}")
                    print(f"   User ID: {result['user_id']}")
                    print(f"   Email: {result['email']}")
                    print(f"   Account Created: {result['created_at']}")
                    print(f"   MFA Enabled: {result['mfa_enabled']}")
                print()            
            return self.results
        except FileNotFoundError:
            print(f"[!] Error: File '{file_path}' not found")
            return []
        except Exception as e:
            print(f"[!] Error reading file: {str(e)}")
            return []
    
    def save_results_json(self, output_file="results.json"):
        """Save verification results to JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"[+] Results saved to {output_file}")
        except Exception as e:
            print(f"[!] Error saving JSON: {str(e)}")
    
    def save_results_txt(self, output_file="results.txt"):
        """Save verification results to text file"""
        try:
            with open(output_file, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("DISCORD TOKEN VERIFICATION RESULTS\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for result in self.results:
                    f.write(f"Token: {result['token'][:30]}...\n")
                    f.write(f"Status: {result['status']}\n")
                    f.write(f"Valid: {result['valid']}\n")
                    if result['valid']:
                        f.write(f"Username: {result['username']}\n")
                        f.write(f"User ID: {result['user_id']}\n")
                        f.write(f"Email: {result['email']}\n")
                        f.write(f"Account Created: {result['created_at']}\n")
                        f.write(f"Verified Account: {result['verified']}\n")
                        f.write(f"MFA Enabled: {result['mfa_enabled']}\n")
                    f.write("-" * 80 + "\n\n")
            
            print(f"[+] Results saved to {output_file}")
        except Exception as e:
            print(f"[!] Error saving TXT: {str(e)}")

def main():
    """Main function"""
    print("=" * 80)
    print("DISCORD TOKEN VERIFICATION TOOL v1.0")
    print("=" * 80 + "\n")
    
    verifier = DiscordTokenVerifier()
    
    # Check if tokens.txt exists
    if os.path.exists("tokens.txt"):
        input_file = "tokens.txt"
    else:
        input_file = input("[?] Enter the path to your tokens file: ").strip()
    
    # Verify tokens
    verifier.verify_from_file(input_file)
    
    # Save results
    if verifier.results:
        print("\n[*] Saving results...")
        verifier.save_results_json("results.json")
        verifier.save_results_txt("results.txt")
        print("\n[+] Verification complete!")
    else:
        print("\n[!] No tokens were verified")

if __name__ == "__main__":
    main()