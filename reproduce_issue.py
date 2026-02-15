from datetime import datetime

def load_prompt_buggy():
    """Simulates the buggy version using format()"""
    print("--- Testing Buggy Version ---")
    try:
        with open("prompts/daily_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
        today_str = datetime.now().strftime("%Y-%m-%d")
        # This should fail if the template has JSON braces
        result = template.format(date=today_str)
        print("Success!")
        return result
    except Exception as e:
        print(f"Failed as expected: {type(e).__name__}: {e}")

def load_prompt_fixed():
    """Simulates the fixed version using replace()"""
    print("\n--- Testing Fixed Version ---")
    try:
        with open("prompts/daily_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
        today_str = datetime.now().strftime("%Y-%m-%d")
        # This should succeed
        result = template.replace("{date}", today_str)
        print("Success! Prompt loaded correctly.")
        # print(result[:100] + "...") # Print first 100 chars
        return result
    except Exception as e:
        print(f"Failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    load_prompt_buggy()
    load_prompt_fixed()
