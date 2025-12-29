from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)
STORAGE_FILE = "notes.json"

def load_notes():
    """Load notes from JSON file, return empty list if file missing or invalid."""
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # If file is empty or corrupted, reset to empty list
        return []

def save_notes(notes):
    """Save notes to JSON file safely."""
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except Exception as e:
        print(f"Error saving notes: {e}")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'GET':
        try:
            return jsonify(load_notes())
        except Exception as e:
            print(f"Error loading notes: {e}")
            return jsonify([]), 500

    elif request.method == 'POST':
        data = request.json
        try:
            notes = load_notes()
            # Remove old note if it exists
            notes = [n for n in notes if n.get('id') != data.get('id')]
            notes.append(data)
            save_notes(notes)
            return jsonify({"status": "ok"})
        except Exception as e:
            print(f"Error saving note: {e}")
            return jsonify({"status": "error"}), 500

@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        notes = load_notes()
        notes = [n for n in notes if n.get('id') != note_id]
        save_notes(notes)
        return jsonify({"status": "deleted"})
    except Exception as e:
        print(f"Error deleting note: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    # Make sure the notes.json file exists and is valid
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "w") as f:
            json.dump([], f)

    app.run(debug=True, host="0.0.0.0", port=5000)


