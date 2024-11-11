import google.generativeai as gemini
import os

def gemini_query(query):
    gemini.configure(api_key=os.environ["GEMINI_API_KEY"])
    model=gemini.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content(query)
    print(response.text)

if __name__=="__main__":
    gemini_query("https://www.eni.com/content/dam/enicom/documents/ita/azioni/attivita-mondo/italia/progetti/venezia/Dichiarazione_Ambientale_Venezia_2025.pdf è un bilancio di sostenibilità? rispondi solo Y/N")
    