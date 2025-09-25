from fastapi import APIRouter, HTTPException, Form
import google.generativeai as genai
import os



genai_router = APIRouter(tags=["AI Features"])
# Configure Gemini API (key set in main.py)
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    raise ValueError(f"Failed to configure Gemini API: {e}")

genai_router = APIRouter(prefix="/ai", tags=["AI Features"])


@genai_router.post("/generate-ad-description")
def generate_ad_description(
    title: str = Form(...),
    category: str = Form(...)
):
    """
    Generate an advertisement description using Google's Gemini AI.
    """
    try:
        prompt = f"""
        Generate a compelling advertisement description for the following:
        - Title: {title}
        - Category: {category}
       
        The description should be engaging, persuasive, and around 100-150 words.
                 Highlight key features and benefits to attract potential customers
        """
       
        response = model.generate_content(prompt)
        generated_description = response.text.strip()
       
        return {"title": title, "category": category, "generated_description": generated_description}
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating description: {str(e)}")



@genai_router.post("/suggest-salary")
def suggest_salary(
    title: str = Form(...),
    category: str = Form(...)
):
    """
    Suggest a salary range using Google's Gemini AI.
    """
    try:
        prompt = f"""
        Suggest a reasonable salary range for the following advertisement:
        - Title: {title}
        - Category: {category}
       
        Provide a low, medium, and high price range in USD.
        """
       
        response = model.generate_content(prompt)
        salary_suggestion = response.text.strip()
       
        return {"title": title, "category": category, "salary_suggestion": salary_suggestion}
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting price: {str(e)}")


@genai_router.post("/score-ad-quality")
def score_ad_quality(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...)
):
    """
    Score the quality of an advertisement using Google's Gemini AI.
    """
    try:
        prompt = f"""
        Rate the quality of the following advertisement on a scale of 1-10 for clarity, attractiveness, and relevance.
        - Title: {title}
        - Description: {description}
        - Category: {category}
       
        Provide a score and brief explanation for each criterion.
        """
       
        response = model.generate_content(prompt)
        quality_score = response.text.strip()
       
        return {"title": title, "description": description, "category": category, "quality_score": quality_score}
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring ad quality:{str(e)}")