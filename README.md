# Lead Research Tool

A tool that combines Tavily's search capabilities with GPT-4 analysis to generate comprehensive research reports for new leads.

## Features

- Company research using Tavily's company_info endpoint
- Person research using Tavily's search_context endpoint
- AI-powered analysis of gathered data
- Structured reports including:
  - Company Overview
  - Decision Maker Profile
  - Opportunity Analysis
  - Recommended Approach
  - Risk Assessment

## Setup

1. Clone the repository:
```bash
git clone https://github.com/hanson-cheng/lead-research-tool.git
cd lead-research-tool
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the script:
```bash
python crm_lead_research.py
```

The tool will:
1. Research the company using Tavily
2. Research the person using Tavily
3. Analyze the gathered data using GPT-4
4. Generate a comprehensive report

## Example Output

The tool generates a detailed report including:
- Verified company information (founding date, location, legal status)
- Professional background and roles
- Market position and online presence
- Opportunity analysis and recommended approaches
- Risk assessment and potential challenges

## Requirements

- Python 3.8+
- OpenAI API key
- Tavily API key

## License

MIT
