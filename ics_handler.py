from icalendar import Calendar, Event
from datetime import datetime
import pytz
import uuid
import os
from dateutil import parser

class ICSHandler:
    @staticmethod
    def parse_ics_file(file_path):
        """
        Parse an ICS file and return event details
        
        Args:
            file_path (str): Path to the ICS file
            
        Returns:
            list: List of dictionaries containing event details
        """
        events = []
        
        try:
            with open(file_path, 'rb') as f:
                calendar = Calendar.from_ical(f.read())
                
                for component in calendar.walk():
                    if component.name == "VEVENT":
                        event = {
                            'summary': str(component.get('summary', 'No Title')),
                            'description': str(component.get('description', 'No Description')),
                            'location': str(component.get('location', 'No Location')),
                            'start': component.get('dtstart').dt if component.get('dtstart') else None,
                            'end': component.get('dtend').dt if component.get('dtend') else None,
                            'uid': str(component.get('uid', '')),
                            'created': component.get('dtstamp').dt if component.get('dtstamp') else None
                        }
                        events.append(event)
                        
            return events
        except Exception as e:
            return [{'error': str(e)}]
    
    @staticmethod
    def create_ics_file(event_details, output_path):
        """
        Create an ICS file from event details
        
        Args:
            event_details (dict): Dictionary containing event details
            output_path (str): Path to save the ICS file
            
        Returns:
            str: Path to the created ICS file or error message
        """
        try:
            cal = Calendar()
            cal.add('prodid', '-//ICS File Handler//example.com//')
            cal.add('version', '2.0')
            
            event = Event()
            event.add('summary', event_details.get('summary', 'No Title'))
            event.add('description', event_details.get('description', 'No Description'))
            
            if event_details.get('location'):
                event.add('location', event_details['location'])
            
            # Handle start and end times
            tz = pytz.timezone('UTC')
            
            # Parse start time
            start_dt = event_details.get('start')
            if isinstance(start_dt, str):
                start_dt = parser.parse(start_dt)
            if start_dt and start_dt.tzinfo is None:
                start_dt = tz.localize(start_dt)
            event.add('dtstart', start_dt)
            
            # Parse end time
            end_dt = event_details.get('end')
            if isinstance(end_dt, str):
                end_dt = parser.parse(end_dt)
            if end_dt and end_dt.tzinfo is None:
                end_dt = tz.localize(end_dt)
            event.add('dtend', end_dt)
            
            # Add timestamp and UID
            event.add('dtstamp', datetime.now(tz))
            event['uid'] = event_details.get('uid', f'{uuid.uuid4()}@icshandler.example.com')
            
            cal.add_component(event)
            
            # Save to file
            with open(output_path, 'wb') as f:
                f.write(cal.to_ical())
                
            return output_path
        except Exception as e:
            return f"Error creating ICS file: {str(e)}"
    
    @staticmethod
    def create_sample_ics():
        """
        Create a sample ICS file with a demo event
        
        Returns:
            str: Path to the created sample ICS file
        """
        sample_event = {
            'summary': 'Sample Event - Team Meeting',
            'description': 'This is a sample event created by ICS File Handler',
            'location': 'Conference Room A',
            'start': datetime.now(pytz.UTC).replace(hour=10, minute=0, second=0, microsecond=0),
            'end': datetime.now(pytz.UTC).replace(hour=11, minute=0, second=0, microsecond=0)
        }
        
        # Ensure the samples directory exists
        os.makedirs('samples', exist_ok=True)
        
        return ICSHandler.create_ics_file(sample_event, 'samples/sample_event.ics') 