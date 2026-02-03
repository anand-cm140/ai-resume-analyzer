from google import genai
import os

def generate_ai_suggestions(match_result, jd_skills):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a career assistant.

Job Requirements:
Must-have skills: {jd_skills['must_have']}
Good-to-have skills: {jd_skills['good_to_have']}

Candidate Analysis:
Match percentage: {match_result['match_score']}%
Missing must-have skills: {match_result['missing_must']}
Missing good-to-have skills: {match_result['missing_good']}

Rules:
- Do NOT assume experience
- Do NOT invent skills
- Suggest learning or resume improvements only
- Keep advice practical and concise

Provide (in Markdown format):
### 📌 Why this score?
[Explanation here]

### 🛠️ What to improve?
[Suggestions here]

### 📚 Skills to focus on
[Skills list here]

"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
