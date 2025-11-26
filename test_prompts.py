from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

print("=== SYSTEM PROMPT ===")
print(SYSTEM_PROMPT[:200] + "...")  # First 200 characters

print("\n=== USER TEMPLATE TEST ===")
test_message = USER_PROMPT_TEMPLATE.format(
    language="SQL",
    filename="test_procedure.sql",
    code_content="SELECT * FROM Members WHERE Status = 'Active'"
)
print(test_message)