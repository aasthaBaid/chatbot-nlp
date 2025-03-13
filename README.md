# General Conversation Short Forms Chatbot

## Overview
This chatbot helps users understand the meaning of common short forms and abbreviations used in general conversation. Users can input an abbreviation, and the bot will respond with its full form and explanation.

## Features
- Recognizes and expands common conversational short forms
- Covers internet slang, texting abbreviations, and everyday acronyms
- Provides clear and concise explanations

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/conversation-shortforms-chatbot.git
   ```
2. Navigate to the project folder:
   ```bash
   cd conversation-shortforms-chatbot
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the chatbot script:
```bash
python chatbot.py
```
Then, enter queries like:
- "What does LOL stand for?"
- "Expand BRB"
- "Meaning of TTYL"

## Data Format
The chatbot uses a JSON file (`conversation_shortforms_intents.json`) containing intents in the following format:
```json
{
  "intents": [
    {
      "tag": "lol",
      "patterns": ["What is LOL?", "Expand LOL", "Meaning of LOL"],
      "responses": ["LOL stands for 'Laugh Out Loud,' commonly used in texting and online chats to indicate amusement."]
    }
  ]
}
```

## Contributing
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes
4. Push to your branch and submit a Pull Request

## License
This project is licensed under the MIT License.

