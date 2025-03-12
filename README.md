# ICS File Handler

A Flask-based web application for creating, parsing, and managing iCalendar (.ics) files with AI assistance.

## Features

- **Parse ICS Files**: Upload and view the contents of existing ICS files
- **Create ICS Files**: Create new calendar events and export them as ICS files
- **AI Event Generator**: Generate calendar events using AI based on meeting topics
- **Sample Download**: Download a sample ICS file to see how they work

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ics-file-handler.git
cd ics-file-handler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

4. Open your browser and navigate to:
   - http://localhost:8080

## Usage

### Parse ICS Files
Upload an existing ICS file to view its events and details.

### Create ICS Files
Fill out the form with event details to create a new ICS file.

### AI Event Generator
Enter a meeting topic, and the AI will generate appropriate event details including:
- Meeting title based on the topic
- Relevant description
- Appropriate location
- Suitable date and duration

## Technologies

- Python 3
- Flask
- icalendar
- pytz
- Bootstrap 5

## License

MIT License 