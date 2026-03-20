#  Podcast Summarizer

A full-stack application that extracts, transcribes, and summarizes podcasts using AI.

##  Features
-  Extract podcast audio
-  AI summarization (BART / FLAN-T5)
-  Key insights instead of generic summaries
-  Full-stack architecture

##  Tech Stack
- Frontend: React (Vite)
- Backend: Python (Flask), Spring Boot
- AI: HuggingFace Transformers

##  Project Structure
frontend/
python-service/
spring_backend/

##  Setup Instructions

--> Frontend
cd frontend
npm install
npm run dev

--> Python Service
cd python-service
pip install -r requirements.txt
python app.py

--> Spring Backend
cd spring_backend
mvn spring-boot:run

##  Steps to use
--> Search for the youtube video you want a summary to.
--> Select the model you want
--> Click on the dotted buttons on the right side of the video and start the summarization
--> Chill out, it will take some time. 
--> Voila! Your summary is ready!

##  Live Demo
Frontend: (add later)
Backend: (add later)

##  Author
Riddhesh Karnik
