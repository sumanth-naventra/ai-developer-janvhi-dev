import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json

# Load your Azure environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_coding_question(language="Python", difficulty="Easy"):
    prompt = f"""
You are a code question generator.

Generate 1 {difficulty} level coding question for {language}.

Output must be in valid JSON ONLY, no text outside JSON.

Format:
{{
  "question": "",
  "difficulty": "{difficulty}",
  "language": "{language}",
  "input": "",
  "expected_output": "",
  "test_cases": [{{"input":"", "output":""}}, {{"input":"", "output":""}}],
  "solution": ""
}}
"""
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    # Handle any accidental extra text
    try:
        data = json.loads(content)
    except:
        start = content.find('{')
        end = content.rfind('}') + 1
        data = json.loads(content[start:end])

    return data


def main():
    # You can change these values to test
    languages = ["Python", "Java", "C++"]
    difficulties = ["Easy", "Medium", "Hard"]

    coding_questions = {}

    for lang in languages:
        coding_questions[lang] = {}
        for level in difficulties:
            print(f"⚙️ Generating {level} {lang} question...")
            coding_questions[lang][level] = generate_coding_question(lang, level)

    with open("coding_questions.json", "w", encoding="utf-8") as f:
        json.dump(coding_questions, f, indent=2)

    print("✅ All coding questions generated successfully.")
    print("📁 Saved to coding_questions.json")


if __name__ == "__main__":
    main()
