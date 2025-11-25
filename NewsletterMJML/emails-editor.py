import json
import shutil

def remove_email_with_backup(email_to_remove, filename='.emails.json'):
    backup_filename = filename + '.bak'
    
    # Create a backup of the original file
    shutil.copy2(filename, backup_filename)
    
    # Load emails from JSON file
    with open(filename, 'r') as file:
        email_data = json.load(file)

    # Track if email was found and removed
    removed = False

    # Search and remove email from all language lists
    for lang, emails in email_data.items():
        if email_to_remove in emails:
            emails.remove(email_to_remove)
            removed = True

    # Save the updated JSON data back to the file
    with open(filename, 'w') as file:
        json.dump(email_data, file, indent=2)

    return removed

# Example usage:
email_to_remove = 'user4@example.com'
if remove_email_with_backup(email_to_remove):
    print(f"Removed {email_to_remove} from the list (backup created).")
else:
    print(f"{email_to_remove} not found in any list.")
