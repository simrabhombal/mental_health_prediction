import os

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file
from reportlab.pdfgen import canvas

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCpOKk13YHmpIGddABFUvGkMUs-LIIzLDA")  
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Flask app
app = Flask(__name__)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# API Route to Get Explanation from Gemini and Generate PDF
@app.route("/explain", methods=["GET"])
def get_llm_explanation():
    try:
        data = request.get_json()
        condition = data.get("condition", "").strip()

        if not condition:
            return jsonify({"error": "No condition provided"}), 400

        # Prepare the prompt for the model
        prompt = f"Provide a brief explanation of {condition} and suggest effective coping strategies."
        response = model.generate_content(prompt)
        # response = model.generate_content(prompt)
        print("Raw Gemini Response:", response)  # Debugging output


        # Convert response to text
        explanation = response.text.strip() if response and hasattr(response, "text") else "No explanation available."

        # Generate PDF file
        pdf_filename = f"{condition.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(os.getcwd(), pdf_filename)

        create_pdf(condition, explanation, pdf_path)

        # Return the generated PDF as a downloadable file
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print("Error during processing:", str(e))
        return jsonify({"error": str(e)}), 500


def create_pdf(title, content, filename):
    """
    Generate a PDF with the given title and content.
    """
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, f"Mental Health Condition: {title}")

    c.setFont("Helvetica", 12)
    text = c.beginText(100, 780)
    text.setFont("Helvetica", 12)
    text.setTextOrigin(100, 760)

    # Wrap text to fit within the PDF
    max_width = 400  # Adjust based on your preference
    lines = []
    words = content.split()
    line = ""
    for word in words:
        if c.stringWidth(line + word, "Helvetica", 12) < max_width:
            line += f" {word}"
        else:
            lines.append(line)
            line = word
    lines.append(line)

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.save()


# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
