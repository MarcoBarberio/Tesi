import google.generativeai as gemini
import os

def gemini_query(query):
    gemini.configure(api_key=os.environ["GEMINI_API_KEY"])
    model=gemini.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content(query)
    return response