from flask import Flask, render_template_string, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage (in production, you'd use a database)
questions = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💕 Marriage Game - Who Said It? 💕</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
        }

        .header h1 {
            color: #d63384;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .header p {
            color: #6c757d;
            font-size: 1.2em;
            font-style: italic;
        }

        .question-form {
            background: linear-gradient(145deg, #ffffff, #f8f9fa);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #495057;
            font-weight: 600;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #d63384;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(214, 51, 132, 0.2);
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }



        .submit-btn {
            background: linear-gradient(145deg, #d63384, #e83e8c);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
        }

        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(214, 51, 132, 0.4);
        }

        .questions-section {
            margin-top: 40px;
        }

        .section-title {
            color: #d63384;
            font-size: 1.8em;
            margin-bottom: 25px;
            text-align: center;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #d63384, #e83e8c);
            border-radius: 2px;
        }

        .question-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #d63384;
            transition: all 0.3s ease;
        }

        .question-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        }

        .question-text {
            font-size: 1.1em;
            color: #495057;
            margin-bottom: 15px;
            line-height: 1.6;
        }

        .question-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
            color: #6c757d;
        }

        .answer-badge {
            background: linear-gradient(145deg, #28a745, #20c997);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }

        .no-questions {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .question-card {
            animation: fadeIn 0.5s ease;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .answer-options {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💕 Questions for the Newlyweds 💕</h1>
            <p>Submit your questions to ask the happy couple live!</p>
        </div>

        <form class="question-form" id="questionForm">
            <div class="form-group">
                <label for="guest_name">Your Name:</label>
                <input type="text" id="guest_name" name="guest_name" required placeholder="Enter your name...">
            </div>

            <div class="form-group">
                <label for="question">Your Question for the Couple:</label>
                <textarea id="question" name="question" required placeholder="What question would you like to ask the newlyweds? (e.g., Who is more likely to burn dinner? What's your funniest memory together?)"></textarea>
            </div>

            <button type="submit" class="submit-btn">Submit Question 💕</button>
        </form>

        <div class="questions-section">
            <h2 class="section-title">Questions from Guests</h2>
            <div id="questionsList">
                {% if questions %}
                    {% for q in questions %}
                    <div class="question-card">
                        <div class="question-text">{{ q.question }}</div>
                        <div class="question-meta">
                            <span>Asked by: <strong>{{ q.guest_name }}</strong></span>
                            <span class="answer-badge">Pending</span>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-questions">
                        No questions yet! Be the first to ask one! 💕
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        document.getElementById('questionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                guest_name: formData.get('guest_name'),
                question: formData.get('question')
            };

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    // Reset form
                    this.reset();
                    // Reload page to show new question
                    window.location.reload();
                } else {
                    alert('Error submitting question. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting question. Please try again.');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, questions=questions)

@app.route('/submit', methods=['POST'])
def submit_question():
    try:
        data = request.get_json()
        
        question_data = {
            'guest_name': data['guest_name'].strip(),
            'question': data['question'].strip(),
            'timestamp': datetime.now().isoformat()
        }
        
        questions.append(question_data)
        
        return jsonify({'success': True, 'message': 'Question submitted successfully!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

# For Vercel deployment
app = app

if __name__ == '__main__':
    app.run(debug=True)