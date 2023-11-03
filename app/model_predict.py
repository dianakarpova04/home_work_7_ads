"""Module for punctuation"""
import string
from pathlib import Path


class Baseline:
    """
    Class for baseline
    """

    @staticmethod
    def prediction(baseline: str, message: str) -> str:
        """
        Def for detect fraud in message
        :param baseline: 'constant-clean', 'constant-fraud', 'first-hypothesis'
        :param message: message for detecting
        :return: 'clean' or 'fraud' result
        """
        if baseline == 'constant-fraud':
            result = "fraud"
        elif baseline == 'constant-clean':
            result = 'clean'
        else:
            punctuation = string.punctuation
            message = message.lower()
            message = ''.join([char for char in message if char not in punctuation]).split()  # noqa

            # Get the current directory of the script
            script_dir = Path(__file__).resolve().parent

            # Construct the full path to the file
            file_path = script_dir / 'word_list.txt'

            # Open the file
            with file_path.open('r') as file:
                fraud_keywords = [line.strip() for line in file]

            fraud_words = 0
            for keyword in fraud_keywords:
                for word in message:
                    if keyword in word:
                        fraud_words += 1

            fraud_rate = fraud_words / len(message)

            result = 'fraud' if fraud_rate > 0.1 else 'clean'

        return result
