from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from datetime import datetime, timedelta
import pytz
from ics_handler import ICSHandler
import uuid
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure upload and samples directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('samples', exist_ok=True)

@app.route('/')
def index():
    """Home page with options to parse or create ICS files"""
    return render_template('index.html')

@app.route('/parse', methods=['GET', 'POST'])
def parse_ics():
    """Parse an uploaded ICS file and display its contents"""
    if request.method == 'POST':
        if 'ics_file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
            
        file = request.files['ics_file']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file:
            # Save the uploaded file
            file_path = os.path.join('uploads', f"{uuid.uuid4()}.ics")
            file.save(file_path)
            
            # Parse the file
            events = ICSHandler.parse_ics_file(file_path)
            
            return render_template('parse_result.html', events=events, file_path=file_path)
    
    return render_template('parse.html')

@app.route('/create', methods=['GET', 'POST'])
def create_ics():
    """Create a new ICS file from form data"""
    if request.method == 'POST':
        # Get form data
        event_details = {
            'summary': request.form.get('summary', 'No Title'),
            'description': request.form.get('description', 'No Description'),
            'location': request.form.get('location', ''),
            'start': request.form.get('start_date') + ' ' + request.form.get('start_time'),
            'end': request.form.get('end_date') + ' ' + request.form.get('end_time')
        }
        
        # Create a unique filename
        output_path = os.path.join('uploads', f"{uuid.uuid4()}.ics")
        
        # Create the ICS file
        result = ICSHandler.create_ics_file(event_details, output_path)
        
        if isinstance(result, str) and result.startswith('Error'):
            flash(result)
            return redirect(request.url)
        
        return redirect(url_for('download_ics', filename=os.path.basename(output_path)))
    
    # Default values for the form
    tz = pytz.timezone('UTC')
    now = datetime.now(tz)
    default_date = now.strftime('%Y-%m-%d')
    default_time = now.strftime('%H:%M')
    
    return render_template('create.html', 
                          default_date=default_date, 
                          default_time=default_time)

@app.route('/genai', methods=['GET', 'POST'])
def genai_ics():
    """Generate an ICS file using GenAI based on a meeting topic"""
    if request.method == 'POST':
        # Get the meeting topic from the form
        meeting_topic = request.form.get('meeting_topic', '')
        
        if not meeting_topic:
            flash('Please enter a meeting topic')
            return redirect(request.url)
        
        # Generate meeting details using "AI" (simulated for now)
        event_details = generate_meeting_details(meeting_topic)
        
        # Create a unique filename
        output_path = os.path.join('uploads', f"{uuid.uuid4()}.ics")
        
        # Create the ICS file
        result = ICSHandler.create_ics_file(event_details, output_path)
        
        if isinstance(result, str) and result.startswith('Error'):
            flash(result)
            return redirect(request.url)
        
        # Show the generated details before downloading
        return render_template('genai_result.html', 
                              event=event_details, 
                              filename=os.path.basename(output_path))
    
    return render_template('genai.html')

def generate_meeting_details(topic):
    """
    Generate meeting details based on the topic using "AI"
    This is a simple simulation of AI-generated content
    """
    # Current time for reference
    tz = pytz.timezone('UTC')
    now = datetime.now(tz)
    
    # Dictionary of meeting types and their details
    meeting_types = {
        'project': {
            'prefixes': ['Project', 'Sprint', 'Development', 'Planning', 'Status'],
            'descriptions': [
                f"Discuss progress on {topic} project and next steps",
                f"Review {topic} milestones and address blockers",
                f"Plan next phase of {topic} implementation",
                f"{topic} project status update and task allocation"
            ],
            'locations': ['Conference Room A', 'Zoom Meeting', 'Microsoft Teams', 'Project War Room'],
            'duration': 60  # minutes
        },
        'review': {
            'prefixes': ['Review', 'Evaluation', 'Assessment', 'Analysis'],
            'descriptions': [
                f"Detailed review of {topic} performance and metrics",
                f"Evaluate {topic} results and discuss improvements",
                f"Quarterly assessment of {topic} initiative",
                f"Deep dive analysis of {topic} data and insights"
            ],
            'locations': ['Board Room', 'Analytics Lab', 'Virtual Meeting Room', 'Executive Suite'],
            'duration': 90  # minutes
        },
        'training': {
            'prefixes': ['Training', 'Workshop', 'Seminar', 'Learning Session'],
            'descriptions': [
                f"Hands-on training session on {topic} fundamentals",
                f"Interactive workshop to improve {topic} skills",
                f"Educational seminar covering {topic} best practices",
                f"Learning and development session focused on {topic}"
            ],
            'locations': ['Training Center', 'Learning Lab', 'Virtual Classroom', 'Workshop Room'],
            'duration': 120  # minutes
        },
        'brainstorm': {
            'prefixes': ['Brainstorming', 'Ideation', 'Creative Session', 'Innovation'],
            'descriptions': [
                f"Open brainstorming session to generate ideas for {topic}",
                f"Creative thinking workshop focused on {topic} challenges",
                f"Collaborative ideation to improve {topic} approach",
                f"Innovation session to reimagine {topic} strategy"
            ],
            'locations': ['Innovation Lab', 'Creative Space', 'Breakout Room', 'Design Studio'],
            'duration': 75  # minutes
        }
    }
    
    # Randomly select a meeting type
    meeting_type = random.choice(list(meeting_types.keys()))
    meeting_info = meeting_types[meeting_type]
    
    # Generate a summary
    prefix = random.choice(meeting_info['prefixes'])
    summary = f"{prefix} Meeting: {topic}"
    
    # Select a description
    description = random.choice(meeting_info['descriptions'])
    
    # Select a location
    location = random.choice(meeting_info['locations'])
    
    # Generate start time (sometime in the next 7 days, during business hours)
    days_ahead = random.randint(1, 7)
    hours = random.randint(9, 16)  # 9 AM to 4 PM
    minutes = random.choice([0, 15, 30, 45])
    
    start_time = now.replace(hour=hours, minute=minutes) + timedelta(days=days_ahead)
    end_time = start_time + timedelta(minutes=meeting_info['duration'])
    
    # Create the event details dictionary
    event_details = {
        'summary': summary,
        'description': description,
        'location': location,
        'start': start_time,
        'end': end_time
    }
    
    return event_details

@app.route('/download/<filename>')
def download_ics(filename):
    """Download an ICS file"""
    file_path = os.path.join('uploads', filename)
    return send_file(file_path, as_attachment=True, download_name='event.ics')

@app.route('/sample')
def create_sample():
    """Create and download a sample ICS file"""
    sample_path = ICSHandler.create_sample_ics()
    return send_file(sample_path, as_attachment=True, download_name='sample_event.ics')

if __name__ == '__main__':
    print("Starting ICS File Handler on port 8080...")
    print("Open your browser and navigate to:")
    print("http://localhost:8080")
    print("http://127.0.0.1:8080")
    print("http://10.0.0.144:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 