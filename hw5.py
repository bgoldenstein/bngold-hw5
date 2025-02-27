# Name: Benjamin Goldenstein
# Student ID: 
# Email: bngold@umich.edu
# List who you have worked with on this homework: 
# List any AI tool (e.g. ChatGPT, GitHub Copilot): 

import re
import os
import unittest
from datetime import datetime
import tempfile

def get_user_info(file_name: str) -> list:
    """
    This function reads the file and returns a list of strings.
    Each string should contain all the information about one user.

    Args:
        file_name (str): The name of the file containing user data.

    Returns:
        user_data (list): A list of strings with each user's information.
    """
    # TODO: implement this function
    user_data = []
    file = open(file_name, "r")
    lines = file.readlines()
    for i in lines:
        user_data.append(i.strip())
    return user_data

def create_comment_dict(user_data: list, hashtag_category_file: str) -> dict:
    """
    Takes a list of user info strings + a path to a hashtag mapping file.
    For each user, parse:
        - username
        - comment text
        - like count
        - hashtag-based categories (from hashtag_category_file)
    Returns:
        comment_dict (dict): {
            username: (comment_text, like_count, [list_of_categories])
        }
    """
    comment_dict = {}
    
    for user_info in user_data:
        username = re.search(r'username:(\w+)|@cc0uNT:(\w+)', user_info)
        if username.group(1):
            username = username.group(1)
        else:
            username = username.group(2)

        comment_found = re.search(r'COMMENT:"([^"]+)"\s*-\s*(\d+)\s*likes', user_info)
        comment = comment_found.group(1)
        likes = int(comment_found.group(2))
        hashtags = re.findall(r'#\w+', comment)
        
        categories = classify_comment_hashtags(hashtags, hashtag_category_file)
        comment_dict[username] = (comment, categories, likes)
    return comment_dict

def classify_comment_hashtags(hashtags: list, hashtag_category_file: str) -> list:
    """
    Reads a hashtag mapping from 'hashtag_category_file'.
    Given a list of hashtags (e.g. ['#happy', '#2025SuperBowl']),
    determine which categories they belong to.

    Returns a list of category names in the same order as their corresponding hashtags.
    Example: For hashtags ['#happy', '#2025SuperBowl'], returns ['emotion', 'event']

    If no matches found, returns an empty list.
    
    Detailed explanation:
    1. Takes a list of hashtags and path to mapping file as input
    2. Creates a dictionary mapping categories to lists of hashtags
    3. For each input hashtag, finds its category and adds to result list
    4. Returns list of categories in same order as input hashtags
    """

    categoriesDict = {}
    
    file = open(hashtag_category_file, "r")
    lines = file.readlines()
    for i in lines:
        if ":" in i:
            category, allHashtags = i.strip().split(":")
            allHashtagsList = []
            for i in allHashtags.split("#"):
                allHashtagsList.append(i.strip())
            categoriesDict[category.strip()] = allHashtagsList
    categories = []
    
    for i in hashtags:
        hashtagAfterHash = i[1:]
        for i, j in categoriesDict.items():
            if hashtagAfterHash in j:
                break
        categories.append(i)
    return categories


def sort_email_domain(user_data: list) -> dict:
    """
    This function extracts email addresses and returns a sorted dictionary
    where the domain name is the key and the count is the value.

    Args:
        user_data (list): A list of strings with each user's information.

    Returns:
        email_data (dict): A dictionary sorted by domain frequency in descending order.
    """
    counts = {}
    
    for i in user_data:
        emailFound = re.search(r'Email:([^@]+@([^/\s]+))', i)
        if emailFound:
            domain = emailFound.group(2)
            counts[domain] = counts.get(domain, 0) + 1
    sortedDict = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    return sortedDict

################## EXTRA CREDIT ##################
def validate_michigan_number(user_data: list) -> list:
    """
    This function checks for southeast Michigan phone numbers and returns a list of valid numbers.

    Args:
        user_data (list): A list of strings with each user's information.

    Returns:
        michigan_numbers (list): A list of valid southeast Michigan phone numbers.
    """
    validNumbers = []
    
    for i in user_data:
        numberFound = re.search(r'Phone:(?:(\d{3})[-.\ ](\d{3})[-.\ ](\d{4}))', i)
        if numberFound:
            area = numberFound.group(1)
            if area in ['734', '313', '810']:
                number = area + "-" + numberFound.group(2) + "-" + numberFound.group(3)
                validNumbers.append(number)
                
    return validNumbers


class TestAllFunc(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()

        # Create a dictionary of file paths.
        # NOTE: The keys must match exactly what you use when opening them.
        self.test_files = {
            "test1": os.path.join(self.test_dir.name, "test1.txt"),
            "test2": os.path.join(self.test_dir.name, "test2.txt"),
            "test3": os.path.join(self.test_dir.name, "test3.txt"),
            "test4": os.path.join(self.test_dir.name, "test4.txt"),
            "hashtag_map": os.path.join(self.test_dir.name, "hashtag_map.txt")
        }

        # Sample data to write to files
        sample_data = [
            "username:User1 / @cc0uNT:user1 / Email:user1@domain.com / Phone:313-111-2222 || COMMENT:\"#happy #pizza #LOL\" - 5 likes",
            "username:User2 * @cc0uNT:user2 * Email:user2@umich.edu / Phone:734.202.3030 || COMMENT:\"#sad #Concert #Relatable\" - 10 likes",
            "username:User3 / @cc0uNT:user3 / Email:user3@random.org / Phone:810-333-9999 || COMMENT:\"#hopeful #KendrickLamar #Paris\" - 8 likes"
        ]

        # Write data to test1
        with open(self.test_files["test1"], 'w', encoding='utf-8') as f:
            f.write(sample_data[0])

        # Write data to test2 (first and second lines separated by a blank line)
        with open(self.test_files["test2"], 'w', encoding='utf-8') as f:
            f.write(sample_data[0] + "\n\n" + sample_data[1])

        # Write data to test3
        with open(self.test_files["test3"], 'w', encoding='utf-8') as f:
            f.write(sample_data[2])

        # Write all sample data to test4, separated by blank lines
        with open(self.test_files["test4"], 'w', encoding='utf-8') as f:
            f.write("\n\n".join(sample_data))

        # Sample hashtag map data for classification
        sample_map = """emotion: #happy #sad #angry #joyful
                        event: #2025SuperBowl #2024Election
                        food: #pizza #coffee
                        """
        with open(self.test_files["hashtag_map"], 'w', encoding='utf-8') as f:
            f.write(sample_map)



    def test_get_user_info(self):
        # TODO: implement this test case
        # Example test usage (replace with your actual code & assertions)
        # line = open(self.test_files["test1"]).readline().strip()
        # result = get_user_info(line)
        # self.assertEqual(result["username"], "User1")
        line = open(self.test_files["test1"]).readline().strip()
        lineToCompare = get_user_info(self.test_files["test1"])
        self.assertEqual(line, lineToCompare[0])

        line = open(self.test_files["test3"]).readline().strip()
        lineToCompare = get_user_info(self.test_files["test3"])
        self.assertEqual(line, lineToCompare[0])
        

    def test_create_comment_dict(self):
        # TODO: implement this test case
        element = {"User1": ("#happy #pizza #LOL", ["emotion", "food", "meme"], 5)}
        elementToCompare = create_comment_dict(get_user_info(self.test_files["test1"]), "mapping.txt")
        self.assertEqual(element, elementToCompare)

        element = {"User3": ("#hopeful #KendrickLamar #Paris", ["emotion", "celebrity", "travel"], 8)}
        elementToCompare = create_comment_dict(get_user_info(self.test_files["test3"]), "mapping.txt")
        self.assertEqual(element, elementToCompare)

    def test_classify_comment_hashtags(self):
        # TODO: implement this test case
        categories = ["emotion", "food", "meme"]
        categoriesToCompare = classify_comment_hashtags(["#happy", "#pizza", "#LOL"], "mapping.txt")
        self.assertEqual(categories, categoriesToCompare)
        
        categories = ["emotion", "celebrity", "travel"]
        categoriesToCompare = classify_comment_hashtags(["#hopeful", "#KendrickLamar", "#Paris"], "mapping.txt")
        self.assertEqual(categories, categoriesToCompare)
        pass

    def test_sort_email_domain(self):
        # TODO: implement this test case
        emails = {"domain.com": 1, "random.org": 1, "umich.edu": 1}
        emailsToCompare = sort_email_domain(get_user_info(self.test_files["test4"]))
        self.assertEqual(emails, emailsToCompare)

    # ############ EXTRA CREDIT ############
    def test_validate_michigan_number(self):
        # TODO: implement this test case
        numbers = ["313-111-2222", "734-202-3030", "810-333-9999"]
        numbersToCompare = validate_michigan_number(get_user_info(self.test_files["test4"]))
        self.assertEqual(numbers, numbersToCompare)
        pass


def main():
    x = get_user_info("comments.txt")
    print(validate_michigan_number(x))
    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()
