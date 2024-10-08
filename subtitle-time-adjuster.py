import re

def adjust_subtitle_time(file_path, seconds_to_add, direction):
    """
    Adjusts the timing of a subtitle file by adding or subtracting a specified number of seconds to each timestamp.

    Args:
        file_path (str): Path to the subtitle file (e.g., SRT, VTT, or ASS)
        seconds_to_add (int): Number of seconds to add or subtract to each timestamp
        direction (str): Direction of time change (either "forward" or "backward")
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression pattern to match timestamp lines
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    # Find all timestamp lines and adjust the timing
    adjusted_content = pattern.sub(lambda match: adjust_timestamp(match, seconds_to_add, direction), content)

    # Write the adjusted content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(adjusted_content)

def adjust_timestamp(match, seconds_to_add, direction):
    """
    Adjusts a single timestamp by adding or subtracting the specified number of seconds.

    Args:
        match (re.Match): Match object containing the timestamp
        seconds_to_add (int): Number of seconds to add or subtract to the timestamp
        direction (str): Direction of time change (either "forward" or "backward")
    """
    start_time, end_time = match.groups()
    start_hours, start_minutes, start_seconds, start_milliseconds = map(int, start_time.replace(':', ',').split(','))
    end_hours, end_minutes, end_seconds, end_milliseconds = map(int, end_time.replace(':', ',').split(','))

    # Calculate the new timestamp values
    if direction == "forward":
        new_start_seconds = start_seconds + seconds_to_add
        new_end_seconds = end_seconds + seconds_to_add
    elif direction == "backward":
        new_start_seconds = start_seconds - seconds_to_add
        new_end_seconds = end_seconds - seconds_to_add

    # Handle cases where the seconds value exceeds 59
    new_start_minutes = start_minutes
    new_end_minutes = end_minutes
    if new_start_seconds >= 60:
        new_start_minutes += 1
        new_start_seconds -= 60
    elif new_start_seconds < 0:
        new_start_minutes -= 1
        new_start_seconds += 60

    if new_end_seconds >= 60:
        new_end_minutes += 1
        new_end_seconds -= 60
    elif new_end_seconds < 0:
        new_end_minutes -= 1
        new_end_seconds += 60

    # Format the new timestamp values
    new_start_time = f'{start_hours:02d}:{new_start_minutes:02d}:{new_start_seconds:02d},{start_milliseconds:03d}'
    new_end_time = f'{end_hours:02d}:{new_end_minutes:02d}:{new_end_seconds:02d},{end_milliseconds:03d}'

    return f'{new_start_time} --> {new_end_time}'

def main():
    print("Please enter the path to your SRT file:")
    file_path = input()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print("SRT file loaded successfully!")
    except FileNotFoundError:
        print("Error: SRT file not found. Please check the file path and try again.")
        return
    except UnicodeDecodeError:
        print("Error: Unable to decode file. Please try specifying a different encoding.")
        return

    print("Do you want to adjust the timing forward or backward?")
    direction = input().lower()
    while direction not in ["forward", "backward"]:
        print("Invalid input. Please enter 'forward' or 'backward':")
        direction = input().lower()

    print("How many seconds do you want to adjust the timing?")
    seconds_to_add = int(input())

    try:
        adjust_subtitle_time(file_path, seconds_to_add, direction)
        print(f"Timing adjustment successful! Your SRT file has been adjusted by {seconds_to_add} seconds {'forward' if direction == 'forward' else 'backward'}.")
    except Exception as e:
        print(f"Error: Timing adjustment failed. {str(e)}")

if __name__ == "__main__":
    main()