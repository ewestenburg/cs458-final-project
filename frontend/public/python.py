import sys

# Get user input from command line arguments
user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"

# Print a message using the user input
print(f"Python script executed with user input: {user_input}")