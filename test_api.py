#!/usr/bin/env python3
"""
Simple test script to verify OpenAI API is working.
Supports both direct API and proxy-based access.
"""

from app.config import OPENAI_API_KEY, OPENAI_API_BASE
from openai import OpenAI


def test_api() -> None:
    """Test OpenAI API with a simple prompt."""
    if not OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("   Please create .env file with:")
        print("   OPENAI_API_KEY=your-key-here")
        print("   OPENAI_API_BASE=https://api.proxyapi.ru/openai/v1")
        return
    
    print("=" * 70)
    print("TESTING OPENAI API")
    print("=" * 70)
    
    # Determine if using proxy
    use_proxy = bool(OPENAI_API_BASE)
    
    if use_proxy:
        print(f"Mode: PROXY")
        print(f"Proxy Base URL: {OPENAI_API_BASE}")
        print(f"API Key: {OPENAI_API_KEY[:7]}...{OPENAI_API_KEY[-4:]}")
    else:
        print(f"Mode: DIRECT")
        print(f"API Key: {OPENAI_API_KEY[:7]}...{OPENAI_API_KEY[-4:]}")
        print("\n💡 Tip: To use proxy, add to .env file:")
        print("   OPENAI_API_BASE=https://api.proxyapi.ru/openai/v1")
    print()
    
    try:
        # Initialize client with proxy if configured
        if use_proxy:
            # Use proxy base URL
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_API_BASE
            )
        else:
            # Direct API access
            client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Test prompt
        test_prompt = "Say 'Hello, API is working!' and tell me what 2+2 equals."
        
        print(f"Prompt: {test_prompt}")
        print("\nSending request to OpenAI API...")
        print("-" * 70)
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract response
        answer = response.choices[0].message.content
        
        print("\n✅ API RESPONSE:")
        print("-" * 70)
        print(answer)
        print("-" * 70)
        
        # Show usage info
        if hasattr(response, 'usage'):
            usage = response.usage
            print(f"\n📊 Usage:")
            print(f"   Tokens used: {usage.total_tokens}")
            print(f"   Prompt tokens: {usage.prompt_tokens}")
            print(f"   Completion tokens: {usage.completion_tokens}")
        
        print("\n✅ SUCCESS: API is working correctly!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        print("\nPossible issues:")
        
        error_str = str(e).lower()
        if "unsupported_country" in error_str or "403" in error_str:
            print("  ⚠ Geographic restriction: Your region is not supported")
            print("     Solutions:")
            print("     - Use a VPN to a supported region")
            print("     - Contact OpenAI support")
        elif "401" in error_str or "invalid" in error_str:
            print("  - Invalid API key")
        elif "quota" in error_str or "429" in error_str:
            print("  - API quota exceeded")
        else:
            print("  - Network connection problem")
            print("  - API service unavailable")


if __name__ == "__main__":
    test_api()

