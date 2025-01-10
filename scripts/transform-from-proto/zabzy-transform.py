# zabzy transform from proto-language

import os
import yaml

# Load the phonology data from the YAML file
def load_phonology(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Transform the word based on translit mappings
def transform_word_translit(input_word, phonology):
    # Initialize results with the input word
    results = {"translit-1": input_word, "translit-2": input_word, "translit-3": input_word}

    # Stage 1: Apply vowel and consonant changes
    for category in ["vowels", "consonants"]:
        for change in phonology["sounds"][category]:
            proto_sound = change.get("translit-0")
            if proto_sound:  # Only process if translit-0 is defined
                for variant in ["translit-1", "translit-2", "translit-3"]:
                    # Get the replacement value, defaulting to an empty string if None or "null"
                    replacement = change.get(variant)
                    if replacement is None or replacement == "null":
                        replacement = ""
                    # Apply the replacement
                    results[variant] = results[variant].replace(proto_sound, replacement)

    # Stage 2: Apply sound changes on the results of stage 1
    for change in phonology["sounds"]["sound-changes"]:
        proto_sound = change.get("translit-0")
        if proto_sound:  # Only process if translit-0 is defined
            for variant in ["translit-1", "translit-2", "translit-3"]:
                # Get the replacement value, defaulting to an empty string if None or "null"
                replacement = change.get(variant)
                if replacement is None or replacement == "null":
                    replacement = ""
                # Apply the replacement to the already transformed results
                results[variant] = results[variant].replace(proto_sound, replacement)

    return results

# Process a list of words from a file
def process_words(input_file, phonology):
    with open(input_file, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]  # Read non-empty lines

    results = {}
    for word in words:
        results[word] = transform_word_translit(word, phonology)

    return results

# Main function
def main():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file = os.path.join(script_dir, "../../phonology.yaml")  # Path to your YAML file
    input_file = os.path.join(script_dir, "input_words.txt")     # Path to the file containing input words
    output_file = os.path.join(script_dir, "output_words.txt")   # Path to save the transformed words

    # Load the phonology data
    phonology = load_phonology(yaml_file)

    # Process the list of words
    results = process_words(input_file, phonology)

    # Save results to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, transformations in results.items():
            file.write(f"Input word (translit-0): {word}\n")
            for variant, transformed_word in transformations.items():
                file.write(f"  {variant}: {transformed_word}\n")
            file.write("\n")  # Separate entries for readability

    print(f"Processed words saved to {output_file}")

if __name__ == "__main__":
    main()
