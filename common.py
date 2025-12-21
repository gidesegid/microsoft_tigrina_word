
import csv
import os
import shutil
import fnmatch
import inflect
import re
from urllib.parse import urlparse
import ast
import emoji
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from datetime import datetime
import unicodedata

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"}
def get_downloads_info():
    input_list=[]
    with open('order.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) > 0:
                if row[0]=='10' and row[1]=='fill_downloads':
                    input_list=row[2].split(',')
    input_list = [s.strip() for s in input_list]
    return input_list

listOfTigrinaAlphabets=['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ', 'ለ', 'ሉ', 'ሊ', 'ላ', 'ሌ', 'ል', 'ሎ', 
                        'ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሕ', 'ሖ', 'መ', 'ሙ', 'ሚ', 'ማ', 'ሜ', 'ም', 'ሞ', 
                        'ረ', 'ሩ', 'ሪ', 'ራ', 'ሬ', 'ር', 'ሮ', 'ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 
                        'ሸ', 'ሹ', 'ሺ', 'ሻ', 'ሼ', 'ሽ', 'ሾ', 'ቀ', 'ቁ', 'ቂ', 'ቃ', 'ቄ', 'ቅ', 'ቆ', 
                        'ቈ', 'ቊ', 'ቋ', 'ቌ', 'ቍ', 'ቐ', 'ቑ', 'ቒ', 'ቓ', 'ቔ', 'ቕ', 'ቖ', 'ቘ', 'ቚ', 'ቛ', 'ቜ', 'በ', 'ቡ', 'ቢ', 'ባ', 'ቤ', 'ብ', 'ቦ', 'ቨ', 'ቩ', 'ቪ', 'ቫ', 'ቬ', 'ተ', 'ቱ', 'ቲ', 'ታ', 'ቴ', 'ት', 'ቶ', 'ቸ', 'ቹ', 'ቺ', 'ቻ', 'ቼ', 'ች', 'ቾ', 'ነ', 'ኑ', 'ኒ', 'ና', 'ኔ', 'ን', 'ኖ', 'ኘ', 'ኙ', 'ኚ', 'ኛ', 'ኜ', 'ኝ', 'ኞ', 'አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ', 'ከ', 'ኩ', 'ኪ', 'ካ', 'ኬ', 'ክ', 'ኮ', 'ኰ', 'ኲ', 'ኳ', 'ኴ', 'ኵ', 'ኸ', 'ኹ', 'ኺ', 'ኻ', 'ኼ', 'ኽ', 'ኾ', 'ዀ', 'ዂ', 'ዃ', 'ዄ', 'ዅ', 'ወ', 'ዉ', 'ዊ', 'ዋ', 'ዌ', 'ው', 'ዎ', 'ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ', 'ዘ', 'ዙ', 'ዚ', 'ዛ', 'ዜ', 'ዝ', 'ዞ', 'ዠ', 'ዡ', 'ዢ', 'ዣ', 'ዤ', 'ዥ', 'ዦ', 'የ', 'ዩ', 'ዪ', 'ያ', 'ዬ', 'ይ', 'ዮ', 'ደ', 'ዱ', 'ዲ', 'ዳ', 'ዴ', 'ድ', 'ዶ', 'ጀ', 'ጁ', 'ጂ', 'ጃ', 'ጄ', 'ጅ', 'ጆ', 'ገ', 'ጉ', 'ጊ', 'ጋ', 'ጌ', 'ግ', 'ጎ', 'ጐ', 'ጒ', 'ጓ', 'ጔ', 'ጕ', 'ጠ', 'ጡ', 'ጢ', 'ጣ', 'ጤ', 'ጥ', 'ጦ', 'ጨ', 'ጩ', 'ጪ', 'ጫ', 'ጬ', 'ጭ', 'ጮ', 'ጰ', 'ጱ', 'ጲ', 'ጳ', 'ጴ', 'ጵ', 'ጶ', 'ጶ', 'ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ፈ', 'ፉ', 'ፊ', 'ፋ', 'ፌ', 'ፍ', 'ፎ', 'ፐ', 'ፑ', 'ፒ', 'ፓ', 'ፔ', 'ፕ', 'ፖ']

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def update_order(task_id, field, value):
    """
    Update a row in the CSV file. For certain task_ids (append_ids), update specific key-value pairs
    within a comma-separated string in the field.
    For other task_ids, replace the field value with the new one.
    
    Args:
        task_id (str): The ID of the task to update.
        field (str): The field to update.
        value (str): The new value or key-value pairs to update.
        append_ids (list, optional): A list of task_ids where specific key-value updates should occur.
                                     Default is None, meaning no appending behavior.
    """
    try:
        # if append_ids is None:
        append_ids = ["12","20","21","22","23","24","25","26"]  # Default to an empty list if not provided

        # Helper function to parse and update key-value pairs in a string
        def update_key_value_pairs(existing_value, new_key_values):
            # Parse the existing value into a dictionary
            pairs = dict(item.split("=", 1) for item in existing_value.split(",") if "=" in item)
            # Parse the new key-value pairs and update the dictionary
            new_pairs = dict(item.split("=", 1) for item in new_key_values.split(",") if "=" in item)
            pairs.update(new_pairs)  # Update with the new key-value pairs
            # Reconstruct the updated string
            return ",".join(f"{k}={v}" for k, v in pairs.items())

        # Read the CSV file and update the specific row
        rows = []
        with open('order.csv', mode='r',encoding="utf-8", newline='') as file:
            csv_reader = csv.DictReader(file)
            
            # Iterate through each row (as a dictionary)
            for row in csv_reader:
                if row['task'] == task_id:  # Check if it's the row to update
                    if task_id in append_ids:
                        # Update key-value pairs in the existing field value
                        existing_value = row.get(field, "")
                        row[field] = update_key_value_pairs(existing_value, value)
                    else:
                        # Replace the value
                        row[field] = value
                rows.append(row)

        # Write the updated data back to the CSV file
        with open('order.csv', mode='w',encoding="utf-8", newline='') as file:
            fieldnames = ['task', 'type', 'content_or_location', 'extra_info', 'done']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            # Write the header
            csv_writer.writeheader()
            
            # Write the updated rows
            csv_writer.writerows(rows)

        return "Updating completed"
    except Exception as error:
            return f"Error:{error}"

def is_question(sentence):
    question_words = ('who', 'what', 'when', 'where', 'why', 'how', 'is', 'are', 'do', 'does', 'can', 'should')
    sentence_clean = sentence.strip().lower()
    return sentence_clean.endswith('?') or sentence_clean.startswith(question_words)
  
def check_if_done(task_id):
    is_done='0'
    with open('order.csv', mode='r',encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) > 0:
                if row[0]==task_id:
                    if row[4]=='1':
                        is_done='1'
    return is_done
def get_order_info(task_id,column):
    column_order=0
    # task,type,content_or_location,extra_info,done
    if column=='task':
        column_order=0
    elif column=='type':
        column_order=1
    elif column=='content_or_location':
        column_order=2
    elif column=='extra_info':
        column_order=3   
    elif column=='done':
        column_order=4 
    with open('order.csv', mode='r',encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        info=""
        for row in csv_reader:
            if len(row) > 0:
                if row[0]==task_id:
                   info = row[column_order]
        return info        
def delete_files(under_directory,exceptions=None):
    """
    Deletes all files under a directory, except those specified in the exceptions list.
    
    :param under_directory: Path to the directory.
    :param exceptions: List of filenames to exclude or a comma-separated string of filenames.
    """
    if exceptions:
        # Convert exceptions to a list if it's a string
        if isinstance(exceptions, str):
            exceptions = exceptions.split(",")
            exceptions = [item.strip() for item in exceptions]  # Strip spaces
        elif not isinstance(exceptions, list):
            raise ValueError("exceptions must be a list or a comma-separated string")
    else:
        exceptions = []  # If None, set to an empty list

    # Iterate over files in the directory
    for filename in os.listdir(under_directory):
        if filename in exceptions:
            print(f"Skipping file: {filename}")
            continue
        else:
            file_path = os.path.join(under_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

def delete_files_under_multiple_directories(list_of_directories,exceptions=None):
    """
    Deletes files under multiple directories, with optional exceptions.

    :param list_of_directories: List of directory paths to clean.
    :param exceptions: List of filenames to exclude or a comma-separated string of filenames.
    :return: Status message.
    """
    print("listOfDirectories:", list_of_directories)
    errors = []

    for directory in list_of_directories:
        try:
            print("Cleaning directory:", directory)
            delete_files(directory, exceptions)
        except Exception as error:
            errors.append(f"Error in {directory}: {error}")

    if errors:
        return f"Some directories could not be cleaned:\n" + "\n".join(errors)
    return "Files under all directories were deleted successfully."
def get_files(directory,extra_info=None):
    try:
        selections=""
        collections=[]
        files = [os.path.join(directory, f).replace(os.path.sep, '/') for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if extra_info != None:
            if isinstance(extra_info, str):
                selections=extra_info.split(',')
            else:
                selections=extra_info
        if selections !="":
            for item1 in files:
                for item2 in selections:
                    if item2 in item1:
                        collections.append(item1)
        else:
            collections=files
        return collections
    except Exception as error:
        return f"There is something wrong! {error}"
def start_new_process():
    pass
    # update_order('3','done','0')

def balance_lists(list1, list2):
    len1 = len(list1)
    len2 = len(list2)

    if len1 > len2:
        list2.extend([""] * (len1 - len2))
    elif len2 > len1:
        list1.extend([""] * (len2 - len1))

    return list1, list2
def split_text_by_delimiters(text, delimiters):
    # Create regex pattern like "[.,፡?።]"
    pattern = "[" + re.escape("".join(delimiters)) + "]"
    
    parts = [part.strip() for part in re.split(pattern, text) if part.strip()]
    
    # If splitting produced nothing, return the original text in a list
    if not parts:
        return [text.strip()]
    
    return parts
# Function to list file names without extensions
def list_files_without_extension(directory):
    files_without_extension = []
    # Iterate through the files in the directory
    for file in os.listdir(directory):
        # Check if it is a file
        if os.path.isfile(os.path.join(directory, file)):
            # Remove the extension from the file name
            file_name_without_extension = os.path.splitext(file)[0]
            files_without_extension.append(file_name_without_extension)
    
    return files_without_extension
def list_files_with_extension(directory):
    files_with_extension = []
    # Iterate through the files in the directory
    for file in os.listdir(directory):
        # Check if it is a file (and not a directory)
        if os.path.isfile(os.path.join(directory, file)):
            # Append the file name (with extension) to the list
            files_with_extension.append(file)
    
    return files_with_extension
# Example usage
# directory = '/path/to/your/directory'
# files = list_files_without_extension(directory)
# print(files)
def text_file_content_length(input_file):
    try:
        # Read the content of the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        # Calculate the total number of chunks needed
        total_length = len(content)
        return total_length
    except Exception as error:
            return f"Error: There is something wrong! {error}"

def split_text_file_into_chunks(filePath, text_splitting_chunk_size):
    try:
        text_input_directory = os.path.dirname(filePath)
        
        # Read the content of the input file
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        length = len(content)
        if int(text_splitting_chunk_size) > 0:
            whatIsInputFile = check_file_type(filePath)  # Assuming this function exists
            
            if length > int(text_splitting_chunk_size):
                # Split the content by full stops and keep the delimiter
                sentences = content.split('.')
                
                # Initialize variables
                current_chunk = []
                chunk_count = 0
                current_chunk_size = 0

                # Iterate through the sentences and build chunks
                for sentence in sentences:
                    sentence = sentence.strip()
                    
                    # Check if adding this sentence exceeds the chunk size
                    if current_chunk_size + len(sentence) + 1 <= int(text_splitting_chunk_size):  # +1 for the period
                        current_chunk.append(sentence + ".")  # Add period back to the sentence
                        current_chunk_size += len(sentence) + 1  # Update chunk size
                    else:
                        # Write the current chunk to a new file
                        chunk_count += 1
                        output_file = f"{text_input_directory}/chunk_{chunk_count}.txt"
                        
                        with open(output_file, 'w', encoding='utf-8') as chunk_file:
                            chunk_file.write("\n".join(current_chunk))  # Write sentences in multiple lines
                        
                        print(f"Created: {output_file} ({current_chunk_size} characters)")
                        
                        # Start a new chunk with the current sentence
                        current_chunk = [sentence + "."]
                        current_chunk_size = len(sentence) + 1

                # Write any remaining sentences as the last chunk
                if current_chunk:
                    chunk_count += 1
                    output_file = f"{text_input_directory}/{whatIsInputFile['file_name']}_chunk_{chunk_count}.txt"
                    
                    with open(output_file, 'w', encoding='utf-8') as chunk_file:
                        chunk_file.write("\n".join(current_chunk))  # Write sentences in multiple lines
                    
                    print(f"Created: {output_file} ({current_chunk_size} characters)")
                
                return "Done: Chunks created successfully"
            else:
                return "Text did not split because the file content size is less than the chunk size"
        else:
            return "Text did not split because chunk size is too small"
        
    except Exception as error:
        return f"Error: There is something wrong! {error}"



def object_to_string(obj):
    """
    Convert a dictionary into a single string with 'field=value' pairs, separated by commas.
    
    Args:
        obj (dict): The dictionary to convert.
        
    Returns:
        str: The formatted string.
    """
    return ",".join(f"{key}={value}" for key, value in obj.items())


def action_from_orderInfo(id_at_order,field_at_order,implimentation_function):
    try:
        # # get_thumbnail=get_order_info("12","content_or_location")
        # get_thumbnail=get_order_info(id_at_order,field_at_order)
        # data=get_thumbnail.split(",")
        # # Parsing the list and creating variables dynamically
        # for item in data:
        #     key, value = item.split('=', 1)
        #     try:
        #         value = int(value)
        #     except ValueError:
        #         try:
        #             value = float(value)
        #         except ValueError:
        #             value = value.strip()
        #     locals()[key] = value  # Assign dynamically to local variables


        # # Parsing the list into a dictionary
        # parsed_data = {}
        # for item in data:
        #     key, value = item.split('=', 1)
        #     # Special handling for "text" to replace "\\n" with "\n"
        #     if key == "text":
        #         value = value.replace("\\n", "\n")
        #     try:
        #         value = int(value)
        #     except ValueError:
        #         try:
        #             value = float(value)
        #         except ValueError:
        #             value = value.strip()
        #     parsed_data[key] = value  # Store key-value pairs in a dictionary
        parsed_data=parse_input_order(id_at_order,field_at_order)
        # Dynamically filter and pass only required arguments to the function
        function_args = {key: parsed_data[key] for key in implimentation_function.__code__.co_varnames if key in parsed_data}

        # Call the function with unpacked arguments
        implimentation_function(**function_args)
        return "done"
    except Exception as error:
            return error

def parse_input_order(id_at_order, field_at_order):
    getInfo = get_order_info(id_at_order, field_at_order)
    # print("getInfo:", getInfo)
    
    parsed_data = {}
    
    # Adjust regex to correctly capture lists and key-value pairs
    pattern = r'(\w+)=((?:\[.*?\]|[^,]*))'
    matches = re.findall(pattern, getInfo)
    
    for key, value in matches:
        key = key.strip()
        value = value.strip()
        
        if key == "text":
            value = value.replace("\\n", "\n")
        
        # Ensure lists with nested brackets are fully captured
        if value.startswith("["):
            bracket_count = 0
            full_value = ""
            for char in getInfo[getInfo.index(value):]:
                full_value += char
                if char == "[":
                    bracket_count += 1
                elif char == "]":
                    bracket_count -= 1
                if bracket_count == 0:
                    break
            value = full_value
            try:
                value = ast.literal_eval(value)  # Safely parse lists
            except (SyntaxError, ValueError):
                pass  # Keep value as string if parsing fails
        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep value as string if not a number

        parsed_data[key] = value  # Store key-value pairs in a dictionary 
    
    return parsed_data


def time_to_seconds(time_ranges):
    def convert(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    
    result = []
    for time_range in time_ranges:
        start, end = time_range.split('-')
        result.append((convert(start), convert(end)))
    
    return result
# Example usage
time_ranges = [
    "00:06:35-00:07:30",
    "00:07:37-00:07:43",
    "00:08:23-00:08:29",
    "00:19:54-00:19:56"
]

# converted = time_to_seconds(time_ranges)
# print(converted)  # [(395, 450), (457, 463), (503, 509), (1194, 1196)]
# test=parse_input_order("15","content_or_location")
# print("test:",test)

def get_row_by_id(file_path, target_id, id_column='id'):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get(id_column) == str(target_id):
                    return row  
        return None
    except Exception as error:
        return f"Error: There was error while retrieving data by id.{error}"

def identify_text_language(text):
    # Remove leading and trailing spaces, tabs, and newlines
    text = text.strip()

    # Define Unicode ranges for English and Tigrinya
    english_ranges = [(0x0041, 0x005A), (0x0061, 0x007A)]  # A-Z, a-z
    tigrinya_range = (0x1200, 0x137F)  # Ge'ez script range

    # Helper function to check if a character is within a given Unicode range
    def is_within_range(char, start, end):
        return start <= ord(char) <= end

    # Flags for English and Tigrinya detection
    is_english = False
    is_tigrinya = False

    # Check each character in the stripped text
    for char in text:
        # Check English ranges
        if any(is_within_range(char, start, end) for start, end in english_ranges):
            is_english = True
        # Check Tigrinya range
        elif is_within_range(char, *tigrinya_range):
            is_tigrinya = True

    # If both are detected, we can say the text is a mix
    if is_english and is_tigrinya:
        return "Mixed (English + Tigrinya)"
    elif is_english:
        return "English"
    elif is_tigrinya:
        return "Tigrinya"
    else:
        return "Unknown"

def separate_english_tigrinya_obj(text):
    tigrinya_pattern = r'[\u1200-\u137F\s።፣.,!?]+'
    english_pattern = r'[A-Za-z\s.,!?]+'
    combined_pattern = f'({tigrinya_pattern})|({english_pattern})'

    matches = re.finditer(combined_pattern, text)

    english_text = ""
    tigrinya_text = ""
    first_lang = None

    for match in matches:
        part = match.group().strip()
        if not part:
            continue

        # Determine which language the part belongs to
        if re.fullmatch(english_pattern, part):
            if not first_lang:
                first_lang = "English"
            english_text += part + " "
        elif re.fullmatch(tigrinya_pattern, part):
            if not first_lang:
                first_lang = "Tigrinya"
            tigrinya_text += part + " "

    return {
        "firstOrderText": first_lang or "",
        "english": english_text.strip(),
        "tigrinya": tigrinya_text.strip()
    }
def normalize_text(text):
    """
    Replace newlines and tabs in the given text with their escape sequences.
    
    Parameters:
        text (str): Input text to process.
    
    Returns:
        str: Processed text with newlines replaced by '\\n' and tabs by '\\t'.
    """
    normalized_text = text.replace("\n", "\\n").replace("\t", "\\t")
    return normalized_text

def time_to_seconds(t):
    """Convert HH:MM:SS to total seconds."""
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

def is_valid_path(path_str):
    try:
        Path(path_str)
        return True
    except Exception:
        return False
def check_file_type(filePath):
    try:
        # Split file name, extension, and directory path
        file_name, file_extension = os.path.splitext(os.path.basename(filePath))
        file_extension = file_extension.lower().strip()  # Ensure case-insensitivity
        directory_path = os.path.dirname(filePath)  # Extract the directory path
        file_type=""
        # Determine file type
        if file_extension in AUDIO_EXTENSIONS:
            file_type = "audio"
        elif file_extension in IMAGE_EXTENSIONS:
            file_type = "image"
        elif file_extension in VIDEO_EXTENSIONS:
            file_type = "video"
        elif file_extension ==".pdf":
            file_type = "pdf"
        elif file_extension == ".txt" or file_extension==".text":
            file_type = "text"
        elif file_extension == ".docx":
            file_type="word_document"
        elif file_extension == ".json":
            file_type="json"
        else:
            file_type = "unknown"
    
        # Return file details as an object (dictionary)
        return {
            "file_name": file_name,
            "file_extension": file_extension,
            "file_type": file_type,
            "directory_path": directory_path
        }
    except Exception as error:
        print("error:",error)
        return f"Error: There is error on figuring out the type of file. {error}"
def combine_path(directory_path, file_name, file_extension=None):
    # Combine the directory, file name, and extension into a full file path
    if file_extension !=None:
      return os.path.join(directory_path, file_name + file_extension)
    else:
        return os.path.join(directory_path, file_name)

def putTokenPathToOrderFile(token_path):
    update_order("150", "content_or_location", token_path)
def putTodoPathToOrderFile(todo_path):
    update_order("90", "content_or_location", todo_path)

def looks_like_file_path(path):
    # Must not end with a separator (like "/" or "\\")
    # and must have a filename part
    return os.path.basename(path) != "" and not path.endswith(os.path.sep)

def copy_directory_contents(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # create the target directory if it doesn't exist

    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)  # copy subdirectory
        else:
            shutil.copy2(s, d)  # copy file with metadata
# title="Top 5 AI Tools You NEED in 2025"
# sourceCollectionFolderName=title.replace(" ","_")
# sourceFolder="C:\\Users\\GideSegid\\Desktop\\test\\current_project"
# destinationFolder="C:\\Users\\GideSegid\\Desktop\\test\\translatedTextCollection"
# copy_directory_contents(f"{sourceFolder}",f"{destinationFolder}/{sourceCollectionFolderName}")
def sanitize_folder_name(name):
    # Replace invalid characters with underscore
    return re.sub(r'[\\/*?:"<>|]', "_", name)
def extract_task_credential_info():
        try:
            task_info=parse_input_order("3","content_or_location")
            task_name=task_info["task_name"]
            base_url=task_info["base_url"]
            username=task_info["username"]
            email=task_info["email"]
            password=task_info["password"]
            return {
                    "task_name": task_name,
                    "base_url": base_url,
                    "username": username,
                    "password": password,
                    "email":email
                }
        except Exception as error:
            return f"Error: There was error on retrieving task credentials {error}"
 # # youtube thumbnail image
    # font_path = "arial.ttf"  # Path to a .ttf font file on your system
    # font_size = 50
    # image_path = output+"/thumbnail.png"
    # image_width=400
    # image_height=400
    # image_background_color=(184, 135, 236)
    # x_text_position=10
    # y_text_position=10
    # text_color=(113, 100, 236)
    # shadow_offset=6
    # shadow_color=(133, 40, 160)
    # create_3d_text_image(youtube_title, font_path, font_size, image_path,image_width,image_height,image_background_color,x_text_position,y_text_position,text_color,shadow_offset,shadow_color)
   
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
def create_project_directories(root_path, directories):
    """
    Creates directories in the root project path if they do not exist.

    :param root_path: The root directory of the project.
    :param directories: A dictionary where values are subdirectory names.
    """
    for key, directory in directories.items():
        # Full path for the directory
        full_path = os.path.join(root_path, directory)
        
        # Create the directory if it does not exist
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")
        else:
            print(f"Directory already exists: {full_path}")

# updatetest=update_order(task_id='29', field='content_or_location', value='cutStarts=20')
def get_main_text_for_process(directory):
    list_text_file_for_processs=list_files_with_extension(directory)

def copy_file(source_file, destination_folder, new_file_name=None):
    try:
        """
        Copy a file to a destination folder with an optional new name.

        :param source_file: Path to the source file.
        :param destination_folder: Path to the destination folder.
        :param new_file_name: (Optional) New name for the file. If None, keeps the original name.
        """
        # Ensure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        
        # Use the original file name if no new name is provided
        if new_file_name is None:
            new_file_name = os.path.basename(source_file)
        
        # Full path for the new file
        destination_file = os.path.join(destination_folder, new_file_name)
        
        # Copy the file
        shutil.copy(source_file, destination_file)

        print(f"File copied to: {destination_file}")
        return destination_file
    except Exception as error:
        return f"Error: There was error while copying file {error}"

def isFileWithFullPath(input):
        if os.path.exists(input):
            print("full path")
        else:
            print("Input file for process is not found")

def getSpecificFilesFromDirectory(directory,extensions):
    files = [f for f in os.listdir(directory) if fnmatch.fnmatch(f, '*') and f.lower().endswith(tuple(extensions))]
    return files

def number_to_words(n):
    p = inflect.engine()
    try:
        num = float(n)  # Convert to float to handle numbers
        if "." in str(n):  # Check if it's a decimal number
            integer_part, decimal_part = str(n).split(".")
            integer_words = p.number_to_words(int(integer_part), andword="")  # Convert integer part
            decimal_words = p.number_to_words(int(decimal_part), andword="")  # Convert decimal part as a whole number
            return f"{integer_words} point {decimal_words}".replace(",", "")
        else:
            return p.number_to_words(int(num), andword="").replace(",", "")
    except ValueError:
        return n  # Return original text if not a number

def currency_with_number_to_words(amount_str):
    # Currency mapping
    currency_map = {
        "$": "dollar",
        "€": "euro",
        "£": "pound",
        "¥": "yen",
        "₹": "rupee"
    }

    p = inflect.engine()
    if amount_str.startswith("."):
        return False
    # Ensure the input is valid
    if not amount_str or len(amount_str) < 2:
        return False

    # Extract the currency symbol and number
    currency_symbol = amount_str[0]
    number_part = amount_str[1:]
    
    # Ensure the number is valid
    try:
        num = float(number_part)  # Convert to float for decimal handling
    except ValueError:
        return False

    # Convert integer and decimal separately
    if "." in number_part:
        integer_part, decimal_part = number_part.split(".")
        integer_words = p.number_to_words(int(integer_part), andword="") if integer_part else "zero"
        decimal_words = p.number_to_words(int(decimal_part), andword="")  # Convert decimal part as whole number
        number_words = f"{integer_words} point {decimal_words}"
    else:
        number_words = p.number_to_words(int(num), andword="")

    # Get currency word
    currency_word = currency_map.get(currency_symbol, "")

    # Add plural 's' if necessary
    plural_suffix = "s" if num > 1 else ""

    return f"{number_words} {currency_word}{plural_suffix}"

def is_currency_number(text):
    # Remove currency symbols ($, €, ¥, £, etc.) and commas
    clean_text = re.sub(r"[^\d.]", "", text)

    # Ensure the number is valid:
    # - Must not be empty
    # - Must not have a lone decimal (e.g., "4." or ".5" should be invalid)
    if not clean_text or clean_text.endswith(".") or clean_text.startswith("."):
        return False

    # Check if it's a valid number
    try:
        float(clean_text)
        return True
    except ValueError:
        return False

def is_number(text):
    # Check for empty string or invalid formats like "4." or ".5"
    if not text or text.endswith(".") or text.startswith("."):
        return False
    try:
        float(text)  # Try converting to a number
        return True
    except ValueError:
        return False

def separate_text_number(text):
    # Find all text and number parts while preserving order
    parts = re.findall(r'[^\d]+|\d+', text)
    return parts

def read_txt_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def convert_to_list(data):
    """
    Converts a string representation of a list into an actual list.
    If it's already a list, return as-is.
    If empty, return an empty string.
    If conversion fails, return an error message.
    """
    try:
        # If input is an empty string or empty-like list representations, return ""
        if data in ["", "[]", "[[]]"]:
            return ""
        
        # If input is already a list, process it directly
        if isinstance(data, list):
            return [has_subset(data), data]
        
        # Convert string to list
        mydata = ast.literal_eval(data)
        return [has_subset(mydata), mydata]
    
    except Exception as error:
        return f"Error: There is an error converting string to list. {error}"

def has_subset(data):
    return any(isinstance(item, list) for item in data)
# whatIsTakeFromDownload= [False, '[[3,5]]']
# video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
# getVideosFromDirectory=getSpecificFilesFromDirectory("temp",video_extensions)

# listOfVideos=[]
# for item in getVideosFromDirectory:
#     path=combine_path("temp",item)
#     obj={
#         "filePath":path
#     }
#     listOfVideos.append(obj)

# print("listOfVideos:",listOfVideos)

def normalize_lists(l1, l2, l3):
    # Determine the minimum length among the three lists
    min_len = min(len(l1), len(l2), len(l3))

    # Function to reduce a list to a target length by merging from the end with spaces
    def reduce_list(lst, target_len):
        lst = lst[:]  # Copy to avoid modifying original list
        while len(lst) > target_len:
            lst[-2] = f"{lst[-2]} {lst[-1]}"
            lst.pop()
        return lst

    # Reduce each list to the minimum length
    l1 = reduce_list(l1, min_len)
    l2 = reduce_list(l2, min_len)
    l3 = reduce_list(l3, min_len)

    return l1, l2, l3

def find_item_in_list(lst, target):
    if target in lst:
        return target
    return None

def list_subdirectories(directory):
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    return subdirectories


def read_unicode_csv(file_path):
    """
    Reads a CSV file with potential Unicode (e.g., Tigrinya) characters and returns
    a list of dictionaries where each dictionary maps field names to their values.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        List[dict]: A list of rows as dictionaries.
    """
    with open(file_path, mode='r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def update_row_by_id(file_path, target_id, update_dict, id_field='id'):
    """
    Updates a row in the CSV file by matching the ID and writes changes back to the file.
    
    Args:
        file_path (str): Path to the CSV file.
        target_id (str): The ID value to search for.
        update_dict (dict): Dictionary of fields to update.
        id_field (str): The name of the ID field (default: 'id').
    """
    updated = False
    with open(file_path, mode='r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    for row in rows:
        if row.get(id_field) == str(target_id):
            row.update(update_dict)
            updated = True

    if updated:
        with open(file_path, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        print(f"No row found with {id_field} = {target_id}")


def mark_done_by_id(file_path, target_id, id_field='id', done_field='done'):
    updated = False
    with open(file_path, mode='r', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames

    for row in rows:
        if row.get(id_field) == str(target_id):
            row[done_field] = "1"
            updated = True

    if updated:
        with open(file_path, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        print(f"No row found with {id_field} = {target_id}")

def copy_folder_contents_to_destination_folder(src, dst):
    try:
       shutil.copytree(src, dst)
       return f"Files transfored to {dst}"
    except Exception as error:
        return f"Error: There was error while taking the files to currently process folder.{error}"
# Function to find an object by Name
def get_voice_by_name(name):
    # Load the JSON file
    with open('my_input_google_voices.json', 'r') as f:
        voices = json.load(f)
    for voice in voices:
        if voice["Name"] == name:
            return voice
    return None  # If not found

def normalize_keys(data: dict) -> dict:
    """
    Convert dict keys to snake_case:
    - lowercase
    - spaces -> underscores
    - remove trailing 's'
    """
    new_data = {}
    for key, value in data.items():
        new_key = key.lower().replace(" ", "_")
        if new_key.endswith("s"):  # handle plurals like 'codes'
            new_key = new_key[:-1]
        new_data[new_key] = value
    return new_data

def getVoiceCredentialInfo():
    voiceCredentialFile=get_order_info("152","content_or_location")
    # Open and read the JSON file
    if os.path.exists(voiceCredentialFile):
        with open(voiceCredentialFile, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["client_id"]
    else:
        return ""
def save_voice_to_csv(voice_data, characters_used, csv_file='my_input_google_text_speech_recorder.csv'):
    """
    Appends a new row to the CSV file with voice details.

    Parameters:
        voice_data (dict): A voice dictionary with keys 'Name', 'language_code', and 'gender'.
        characters_used (int): Number of characters used.
        csv_file (str): Path to the CSV file.
    """
    try:
        if not voice_data:
            print("No voice data provided.")
            return

        # Check if file exists to decide whether to write headers
        file_exists = os.path.isfile(csv_file)

        # Determine the next ID
        next_id = 1
        if file_exists:
            with open(csv_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                ids = [int(row["id"]) for row in reader if row["id"].isdigit()]
                if ids:
                    next_id = max(ids) + 1

        # Prepare the row
        
        normalized = normalize_keys(voice_data)
        print("normalized:",normalized)
        client_id=getVoiceCredentialInfo()
        row = {
            "id": next_id,
            "voice": normalized["name"],
            "voice_category": normalized["language_code"],
            "gender": normalized["gender"],
            "characters_used": characters_used,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client_id":client_id
        }

        # Write the row to CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        
        return csv_file
    except Exception as error:
        return f"Error:There was error saving voice info to csv file.{error}"

def remove_bracketed(text):
    return re.sub(r"\[.*?\]", "", text)
# voice = get_voice_by_name("en-US-Wavenet-F")
# save_voice_to_csv(voice, characters_used=150)
def textCleaningForSpeech(text):
    try:
        # Replace newlines and unwanted symbols
        text = text.replace('\n', ' ').replace('\r', ' ').replace('-', ' ').replace('*', '').replace('_',' ').replace('  ',' ').replace('??','')
        text = re.sub(r'\s{2,}', ' ', text).strip()
        text=remove_emojis(text)
        text=remove_bracketed(text)
        # Check for any English letters
        if not re.search(r'[A-Za-z]', text):
            return ""  # Entirely Tigrinya or no English content

        # Remove non-English (Tigrinya, etc.)
        english_only_text = re.sub(r'[^A-Za-z0-9.,;:?!\'"()\[\] ]+', '', text)

        # Normalize any extra spaces caused by removal
        english_only_text = re.sub(r'\s{2,}', ' ', english_only_text).strip()

        return english_only_text

    except Exception as error:
        return f"Error: There was error on cleaning text. {error}"

def split_text_by_bytes_smart(text, max_bytes=3000, encoding='utf-8'):
    def encode_len(s):
        return len(s.encode(encoding))

    # Try to find block-level tags first
    blocks = re.findall(r'(<[^>]+>.*?</[^>]+>)', text, flags=re.DOTALL)

    # If no tags found, fallback to sentence splitting
    if not blocks:
        # Split on sentence endings (. or ?) with optional whitespace after
        sentences = re.split(r'(?<=[.؟?])\s+', text)
        blocks = sentences

    chunks = []
    current_chunk = ''
    current_bytes = 0

    for block in blocks:
        block_bytes = encode_len(block)

        if current_bytes + block_bytes > max_bytes:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = block
            current_bytes = block_bytes
        else:
            if current_chunk:
                current_chunk += ' ' + block
            else:
                current_chunk = block
            current_bytes += block_bytes + (1 if current_chunk else 0)  # account for space

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# inputText="E:\\test\\current_project\\current.txt"
# with open(inputText, "r", encoding="iso-8859-1") as file:
#     text = file.read()
# text="this is test እዚ ፈተንና ኢዩ love ። he will come today. ክመጽእ ኢዩ ሎሚ። he can not come today"
# clean_text=textCleaningForSpeech(text)
# print("clean_text:",clean_text)
# # Example usage
# text = clean_text  # Replace with actual content
# chunks = split_text_by_bytes_smart(text)
# chunks_collection=0
# for i, chunk in enumerate(chunks):
#     chunks_collection +=len(chunk)
#     print(f"Chunk_{i+1} ({len(chunk.encode('utf-8'))} bytes):")
#     print(chunk)
#     print("-" * 40)

# print("chunks_collection:",chunks_collection)


def get_sorted_chunks(folder_path, prefix="Chunk"):
    folder = Path(folder_path)
    chunk_files = []

    # Pattern to match e.g., chunk1, chunk2_more.txt, chunk10_extra.log, etc.
    pattern = re.compile(rf"{re.escape(prefix)}(\d+)")

    for f in folder.iterdir():
        if f.is_file():
            match = pattern.search(f.name)
            if match:
                chunk_number = int(match.group(1))
                chunk_files.append((chunk_number, f))

    # Sort by the extracted number
    sorted_chunks = [f for _, f in sorted(chunk_files, key=lambda x: x[0])]
    return sorted_chunks

# # Example usage
# folder_path = "temp"  # replace with your actual folder path
# chunks = get_sorted_chunks(folder_path)

# for f in chunks:
#     print(f.name)

def summarize_voice_usage_with_limits(csv_file_path, target_month,client_id=None):
    # Voice categories and their monthly free tier limits
    category_limits = {
        "Standard": 4_000_000,
        "WaveNet": 1_000_000,
        "Neural2": 1_000_000,
        "Polyglot": 1_000_000,
        "Studio": 100_000,
    }

    # Voice type -> category mapping
    voice_category_map = {
        "Casual": "Standard",
        "Chirp-HD": "WaveNet",
        "Chirp3-HD": "WaveNet",
        "Neural2": "Neural2",
        "News": "WaveNet",
        "Polyglot": "Polyglot",
        "Standard": "Standard",
        "Studio": "Studio",
        "Wavenet": "WaveNet",
    }

    # Accumulate usage per category
    usage_summary = defaultdict(int)

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            voice_field = row.get('voice', '')
            characters_str = row.get('characters_used', '').strip()
            date_str = row.get('date', '').strip()
            client_id_in_file=row.get('client_id', '')

            # Skip invalid characters_used
            try:
                characters_used = int(characters_str)
            except ValueError:
                continue

            # Skip non-matching months
            if not date_str or not date_str.startswith(target_month):
                continue

            # Match voice to a category
            for voice_name, category in voice_category_map.items():
                if voice_name in voice_field and client_id==client_id_in_file:
                    usage_summary[category] += characters_used
                    break

    # Build final result
    final_summary = {}
    for category, used in usage_summary.items():
        limit = category_limits.get(category, 0)
        remaining = max(limit - used, 0)
        percent_used = used / limit if limit else 0

        final_summary[category] = {
            "used_characters": used,
            "remaining": remaining,
            "percentage_used": round(percent_used, 4),
            "limit":limit
        }

    return final_summary

# # client_id=getVoiceCredentialInfo()
# client_id="12345"
# print("client_id:",client_id)
# summary = summarize_voice_usage_with_limits("my_input_google_text_speech_recorder.csv", "2025-09",client_id)
# print(summary)

def extract_voice_names_from_json_file_voice(json_file_path):
    """
    Reads a JSON file and returns a list of all 'Name' values from voice objects.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return [voice.get("Name") for voice in data if "Name" in voice]

# voice_names = extract_voice_names_from_json_file_voice("my_input_google_voices.json")
# print(voice_names)
# getNameInfo=get_voice_by_name("en-US-Chirp3-HD-Autonoe")
# print("getNameInfo:",getNameInfo)

def get_url_type(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()

    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    video_exts = {'.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm', '.mkv'}

    if ext in image_exts:
        return "image"
    elif ext in video_exts:
        return "video"
    else:
        return "unknown"


# url = "https://example.com/video.mp4"
# print(get_url_type(url))  # Output: video

def extract_descriptions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # print("lines::",lines)
    # Define valid section headers (without colons)
    valid_headers = {
        "english_title", "tigrina_title",
        "english_description", "tigrina_description",
        "english_chapters", "tigrina_chapters",
        "english_tags", "tigrina_tags","start_video_text","ending_video_text",
        "tiktok_text","hook_text","video_collection",
        "collection_download_from","thumbnail_image",
        "thumbnail_overlay_image","video_type_to_be_generated","task_name",
        "translate_text_file","add_caption","left_side_slid_text","left_side_slide_text_inclination_degree",
        "right_side_slid_text","right_side_slid_text_inclination_degree","background_music","upload_to_youtube_after_process",
        "given_video","working_directory","after_process_collection_directory","output_directory","process_folder","audio_file_or_ai_voice_to_be_used_during_audio_generation"
    }


    # startVideo:
    # ``This is staring video

    # endingVideo:
    # This is ending video

    # tiktok:
    # This is tiktok text

    # hook:
    # This is hook text``

    data = {header: "" for header in valid_headers}
    current_section = None
    buffer = []
    found_section = False

    for line in lines:
        stripped = line.strip()
        lower_stripped = stripped.lower().rstrip(":")

        if lower_stripped in valid_headers:
            if current_section:
                data[current_section] = '\n'.join(buffer).strip()
                buffer = []
            current_section = lower_stripped
            found_section = True
        else:
            buffer.append(line.rstrip())

    if current_section:
        data[current_section] = '\n'.join(buffer).strip()

    if not found_section:
        # If no headers found, treat whole text as generic English fallback
        data["english_description"] = '\n'.join([line.rstrip() for line in lines]).strip()

    return data

# filePath=r"E:\test\current_project\info.txt"
# test=extract_descriptions(filePath)
# print("test:",test["tigrina_title"])


def clean_filename(name):
    # Normalize and remove accents (e.g., ó → o)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')

    # Replace unwanted characters with underscore, except for . _ -
    name = re.sub(r'[^\w.-]', '_', name)

    # Optional: Remove repeated underscores
    name = re.sub(r'__+', '_', name)

    return name.strip('_')

def rename_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
                cleaned_name = clean_filename(name) + ext
                new_path = os.path.join(folder_path, cleaned_name)

                if new_path != file_path:
                    os.rename(file_path, new_path)
                    print(f'Renamed: {filename} -> {cleaned_name}')