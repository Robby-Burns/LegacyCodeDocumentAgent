from file_handler import read_code_file

# Test with our sample SQL file
result = read_code_file("sample_code.sql")

print("=== FILE HANDLER TEST ===")
print(f"Filename: {result['filename']}")
print(f"Language: {result['language']}")
print(f"Success:  {result['success']}")
print(f"Error:    {result['error']}")
print(f"\n=== FILE CONTENT (first 200 chars) ===")
if result['content']:
    print(result['content'][:200] + "...")
else:
    print("No content loaded.")