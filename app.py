from flask import Flask, render_template, request, session, jsonify
import google.generativeai as genai
import markdown
import re
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")


def clean_and_format(text):
    # Basic sanitization or formatting if needed
    return markdown.markdown(text) if not text.strip().startswith("<") else text

def get_gemini_response(prompt, context=""):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again in a moment."

@app.route("/")
def index():
    # Sample health tips
    tips = [
        {
            "title": "Daily Exercise Essentials",
            "category": "Physical Health",
            "content": "Regular physical activity is crucial for maintaining a healthy body. Aim for at least 30 minutes of moderate exercise daily, including cardio, strength training, and flexibility exercises.",
            "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=800&amp;q=80",
            "link": "https://www.cdc.gov/physicalactivity/basics/index.htm"
        },
        {
            "title": "Balanced Nutrition Guide",
            "category": "Nutrition",
            "content": "A well-balanced diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. Learn how to create nutritious meals that support your overall health.",
            "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=500&auto=format&fit=crop&q=60",
            "link": "https://www.nhs.uk/live-well/eat-well/how-to-eat-a-balanced-diet/eating-a-balanced-diet/"
        },
        {
            "title": "Quality Sleep Habits",
            "category": "Sleep Health",
            "content": "Good sleep is essential for physical and mental health. Discover tips for better sleep hygiene, including consistent sleep schedules and creating a restful environment.",
            "image": "https://images.unsplash.com/photo-1511295742362-92c96b1cf484?w=500&auto=format&fit=crop&q=60",
            "link": "https://www.sleepfoundation.org/sleep-hygiene"
        },
        {
            "title": "Stress Management Techniques",
            "category": "Mental Health",
            "content": "Chronic stress can impact your physical health. Learn effective stress management techniques including meditation, deep breathing, and regular relaxation practices.",
            "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=500&auto=format&fit=crop&q=60",
            "link": "https://www.apa.org/topics/stress"
        },
        {
            "title": "Hydration Importance",
            "category": "Physical Health",
            "content": "Proper hydration is vital for body function. Learn how much water you need daily and tips for staying hydrated throughout the day.",
            "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=500&auto=format&fit=crop&q=60",
            "link": "https://hsph.harvard.edu/news/the-importance-of-hydration/"
        },
        {
            "title": "Posture and Ergonomics",
            "category": "Physical Health",
            "content": "Maintaining good posture and proper ergonomics can prevent pain and injury. Get tips for correct sitting, standing, and lifting techniques.",
            "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&auto=format&fit=crop&q=60",
            "link": "https://www.osha.gov/ergonomics"
        }
    ]
    return render_template("index.html", tips=tips)

@app.route("/symptom", methods=["GET", "POST"])
def symptom():
    result = None
    if request.method == "POST":
        symptoms = request.form.get("symptoms", "")
        severity = request.form.get("severity", "")
        duration = request.form.get("duration", "")
        
        prompt = f"""You are a medical AI assistant. Based on the following information, provide a comprehensive analysis:

Symptoms: {symptoms}
Severity: {severity}
Duration: {duration}

Please provide a detailed analysis in the following format:

1. Possible Conditions:
   - List 3-5 most likely conditions based on the symptoms
   - Include brief descriptions of each condition
   - Note that these are possibilities, not diagnoses
   - Consider the severity and duration in your analysis

2. Recommended Actions:
   - List immediate steps the person should take
   - Include when to seek emergency care
   - Suggest when to schedule a doctor's appointment
   - Consider the severity level in recommendations

3. Home Care Tips:
   - List 3-5 safe home remedies for symptom relief
   - Include lifestyle modifications that might help
   - Note any activities to avoid
   - Consider the duration of symptoms in suggestions

4. Department of Doctor to Consult:
   - Suggest the appropriate medical department based on symptoms
   - Provide a brief description of the department's focus
   - Note any specific tests or procedures they might perform

5. Important Disclaimer:
   - Clearly state this is not medical advice
   - Emphasize the need for professional medical consultation
   - Include a note about emergency situations


   
Format the response in clean HTML with appropriate headings and styling. Make it easy to read and understand."""

        try:
            response = model.generate_content(prompt)
            result = response.text
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template("symptom.html", result=result)

@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    if 'chat_history' not in session:
        session['chat_history'] = []
        # Add initial welcome message
        session['chat_history'].append({
            "role": "bot",
            "content": "Hello there! How can I help you today? What brings you in to see me?",
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
    
    if request.method == "POST":
        user_message = request.form.get("question")
        if user_message:
            # Add user message to chat history
            session['chat_history'].append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            
            # Build conversation context
            conversation_context = ""
            for msg in session['chat_history'][-5:]:  # Include last 5 messages for context
                role = "Patient" if msg["role"] == "user" else "Doctor"
                conversation_context += f"{role}: {msg['content']}\n"
            
            # Get AI response
            prompt = f"""You are a friendly and professional general practitioner. Respond to the patient's question in a warm, conversational manner while maintaining medical accuracy. 

Guidelines for your response:
1. Use a friendly, approachable tone
2. Explain medical terms in simple language
3. Show empathy and understanding
4. Provide practical advice when appropriate
5. If the question is not health-related, gently redirect to health topics
6. Answer in 2 or 3 lines
7. Remember and reference previous conversation points when relevant

Recent conversation history:
{conversation_context}

Patient's Question: {user_message}

Please format your response in clean HTML without code block markers like ```html and text in black. Keep the tone warm and professional, like a caring doctor talking to their patient."""

            try:
                ai_response = get_gemini_response(prompt)
                # Add AI response to chat history
                session['chat_history'].append({
                    "role": "bot",
                    "content": clean_and_format(ai_response),
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
            except Exception as e:
                session['chat_history'].append({
                    "role": "bot",
                    "content": "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again in a moment.",
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
            
            session.modified = True
    
    return render_template("assistant.html", chat_history=session.get('chat_history', []))

@app.route("/health-metrics", methods=["GET", "POST"])
def health_metrics():
    result = None
    if request.method == "POST":
        age = int(request.form["age"])
        gender = request.form["gender"]
        cholesterol = int(request.form["cholesterol"])
        sugar = int(request.form["sugar"])
        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])

        prompt = f"""
You are a professional medical assistant AI. Based on the following patient health metrics, provide an easy-to-understand, medically informed analysis.

Patient Information:
- Age: {age}
- Gender: {gender}
- Cholesterol: {cholesterol} mg/dL
- Blood Sugar: {sugar} mg/dL
- Blood Pressure: {systolic}/{diastolic} mmHg

Please provide the following sections in your response:

- headings in blue color

1. <h3>Individual Metric Analysis</h3>
   - Analyze each metric (Cholesterol, Sugar, Blood Pressure)
   - Indicate whether it’s Normal, Warning, or Dangerous in green , orange, or red respectively
   - Explain what that means in layman’s terms
   - Include optimal range for the age and gender

2. <h3>Health Risk Summary</h3> 
   - Assess overall health risk based on the metrics
   - Mention potential health conditions (e.g. prediabetes, hypertension)

3. <h3>Recommended Next Steps</h3>
   - Suggest medical follow-ups (e.g. tests, doctor visit)
   - Offer lifestyle tips for improvement (diet, exercise, etc.)

4. <h3>Disclaimer</h3>
   - Clearly mention this is not a medical diagnosis
   - Advise consultation with a healthcare professional

Make sure the response is in clean, readable HTML format and without code block markers like ```html..
        """

        try:
            response = model.generate_content(prompt)
            result = clean_and_format(response.text)
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template("health_metrics.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
