import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_questions(category):
    prompt = f"""
You are an exam question generator.

Generate EXACTLY 5 {category} questions.

Output MUST be ONLY valid JSON ARRAY.
NO extra text, NO markdown, NO ```json, NO comments.

Each item must follow this format:
{{
  "question": "",
  "options": {{"A":"","B":"","C":"","D":""}},
  "correct_answer": "",
  "explanation": ""
}}

For reasoning category include ONE image-based question (describe the image in text only).
Return ONLY a JSON array.
"""
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content.strip()

    # Parse JSON safely
    try:
        return json.loads(content)
    except:
        # Remove possible leading/trailing text if AI still added something
        start = content.find('[')
        end = content.rfind(']') + 1
        clean_json = content[start:end]
        return json.loads(clean_json)

def main():
    categories = ["aptitude", "reasoning", "verbal"]
    exam_data = {}

    for cat in categories:
        print(f"⚙️ Generating {cat} questions...")
        exam_data[cat] = generate_questions(cat)

    with open("exam_questions.json", "w", encoding="utf-8") as f:
        json.dump(exam_data, f, indent=2)

    print("✅ Done! Clean JSON saved to exam_questions.json")

if __name__ == "__main__":
    main()
