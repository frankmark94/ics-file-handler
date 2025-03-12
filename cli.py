#!/usr/bin/env python3
"""
ICS File Handler - Command Line Interface
A simple CLI tool for working with ICS (iCalendar) files.
"""

import argparse
import os
import sys
from datetime import datetime
import pytz
from ics_handler import ICSHandler

def main():
    parser = argparse.ArgumentParser(description='ICS File Handler - Command Line Interface')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse an ICS file')
    parse_parser.add_argument('file', help='Path to the ICS file to parse')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new ICS file')
    create_parser.add_argument('--summary', required=True, help='Event title/summary')
    create_parser.add_argument('--description', help='Event description')
    create_parser.add_argument('--location', help='Event location')
    create_parser.add_argument('--start', required=True, help='Start time (YYYY-MM-DD HH:MM)')
    create_parser.add_argument('--end', required=True, help='End time (YYYY-MM-DD HH:MM)')
    create_parser.add_argument('--output', required=True, help='Output file path')
    
    # Sample command
    sample_parser = subparsers.add_parser('sample', help='Create a sample ICS file')
    sample_parser.add_argument('--output', default='sample_event.ics', help='Output file path')
    
    args = parser.parse_args()
    
    if args.command == 'parse':
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            return 1
            
        events = ICSHandler.parse_ics_file(args.file)
        
        if not events:
            print("No events found in the ICS file.")
            return 0
            
        for i, event in enumerate(events):
            print(f"\n--- Event {i+1} ---")
            if 'error' in event:
                print(f"Error: {event['error']}")
                continue
                
            print(f"Summary: {event['summary']}")
            print(f"Description: {event['description']}")
            print(f"Location: {event['location']}")
            print(f"Start: {event['start']}")
            print(f"End: {event['end']}")
            print(f"UID: {event['uid']}")
            print(f"Created: {event['created']}")
    
    elif args.command == 'create':
        try:
            # Parse start and end times
            start_dt = datetime.strptime(args.start, '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(args.end, '%Y-%m-%d %H:%M')
            
            # Add timezone information (UTC)
            tz = pytz.timezone('UTC')
            start_dt = tz.localize(start_dt)
            end_dt = tz.localize(end_dt)
            
            event_details = {
                'summary': args.summary,
                'description': args.description or 'No Description',
                'location': args.location or '',
                'start': start_dt,
                'end': end_dt
            }
            
            result = ICSHandler.create_ics_file(event_details, args.output)
            
            if isinstance(result, str) and result.startswith('Error'):
                print(result)
                return 1
                
            print(f"ICS file created successfully: {args.output}")
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Date format should be 'YYYY-MM-DD HH:MM'")
            return 1
    
    elif args.command == 'sample':
        try:
            result = ICSHandler.create_sample_ics()
            print(f"Sample ICS file created: {result}")
        except Exception as e:
            print(f"Error creating sample file: {str(e)}")
            return 1
    
    else:
        parser.print_help()
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 