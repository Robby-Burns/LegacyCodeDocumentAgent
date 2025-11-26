from file_handler import read_code_file
from agent import generate_documentation

# Step 1: Read the sample SQL file
print("📄 Reading code file...")
file_result = read_code_file("sample_code.sql")

if not file_result["success"]:
    print(f"❌ Error: {file_result['error']}")
    exit()

print(f"✅ Loaded: {file_result['filename']} ({file_result['language']})")

# Step 2: Send to the LLM
print(f"\n🤖 Sending to AI for analysis...")
print("   (This may take 10-30 seconds)\n")

doc_result = generate_documentation(
    filename=file_result["filename"],
    language=file_result["language"],
    code_content=file_result["content"]
)

# Step 3: Display the result
if doc_result["success"]:
    print(f"✅ Documentation generated using: {doc_result['model_used']}\n")
    print("=" * 60)
    print(doc_result["documentation"])
    print("=" * 60)
else:
    print(f"❌ Error: {doc_result['error']}")