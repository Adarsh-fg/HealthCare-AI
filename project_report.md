# HealthCare AI Project Report

## A Web-Based Healthcare Analysis Platform

**Prepared by**: Adarsh P  
**Submitted on**: 13/06/2025

---

## 📌 Introduction

### Project Overview

The HealthCare AI project is a web-based application designed to provide users with accessible health-related insights through an intuitive interface. Leveraging artificial intelligence and modern web technologies, the platform offers three core functionalities:

- **Symptom Checker**
- **Health Assistant Chat**
- **Health Metrics Analysis**

These features empower users with preliminary health information while emphasizing the importance of professional medical consultation.

---

## 🎯 Objectives

- Develop a user-friendly platform for analyzing health symptoms and metrics.
- Integrate AI-driven insights using the Gemini API for accurate and conversational responses.
- Promote health awareness through actionable tips and recommendations.

---

## 🧠 System Design

### Architecture

The HealthCare AI platform follows a client-server architecture:

- **Front-End**: HTML (Jinja2), CSS, and JavaScript for responsive UI.
- **Back-End**: Python (Flask) to handle routing, session management, and AI API interactions.
- **AI Integration**: Google Gemini API powers AI-driven features.

### Technologies Used

| Component          | Technology                         |
|--------------------|-------------------------------------|
| Front-End          | HTML, CSS, JavaScript, Jinja2       |
| Back-End           | Python, Flask                       |
| AI Model           | Google Gemini API (gemini-1.5-flash-latest) |
| Session Management | Flask Session                       |
| Environment        | Python Virtual Environment          |

---

## 🧩 Modules

- **Home Page**: Health tips and navigation.
- **Symptom Checker**: Inputs symptoms, severity, and duration. Returns AI-generated insights, actions, and home care tips.
- **Health Assistant**: Chatbot for professional health-related Q&A.
- **Health Metrics**: Analyzes user metrics (cholesterol, blood sugar, BP) and provides risk summaries and recommendations.

---

## 🛠 Implementation

### Front-End Development

- Jinja2 templates with a consistent base layout.
- Forms for symptom and metric input.
- Chat interface with auto-scroll and interactive conversation.

### Back-End Development

- **Routing**: `/symptom`, `/assistant`, `/health-metrics`
- **Form Handling**: Validates and processes user inputs.
- **Session Management**: Stores chat history.
- **AI Integration**: Sends prompts to Gemini API and formats responses.

### AI Integration

- Gemini API used in Symptom Checker and Health Assistant.
- Prompts are engineered to return structured HTML responses.
- Ensures sections like *Possible Conditions* and *Recommended Actions* are clear.

---

## 🌟 Features

- **Symptom Checker**: AI-generated condition reports, actions, and tips.
- **Health Assistant**: Friendly chatbot with persistent conversation history.
- **Health Metrics Analysis**: Personalized health evaluation and risk reports.

---

## ✅ Conclusion

### Summary

The HealthCare AI project delivers an AI-powered platform offering accessible, informative, and interactive health insights. Its core modules—Symptom Checker, Health Assistant, and Health Metrics—successfully guide users with relevant health data while maintaining a clean and responsive interface.

---
