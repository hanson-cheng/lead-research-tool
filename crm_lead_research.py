import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize clients with API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not openai_api_key or not tavily_api_key:
    raise ValueError(
        "Please set OPENAI_API_KEY and TAVILY_API_KEY in your .env file. "
        "Create a .env file in the project root and add:\n"
        "OPENAI_API_KEY=your_openai_api_key_here\n"
        "TAVILY_API_KEY=your_tavily_api_key_here"
    )

openai_client = OpenAI(api_key=openai_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

class LeadResearcher:
    def __init__(self, tavily_client, openai_client):
        self.tavily_client = tavily_client
        self.openai_client = openai_client

    def research_company(self, company_name, domain=None):
        try:
            query = f"Information about {company_name}"
            if domain:
                query += f" ({domain})"
            
            print(f"Researching company: {company_name}...")
            return self.tavily_client.get_company_info(
                query=query,
                search_depth="advanced",
                max_results=7
            )
        except Exception as e:
            print(f"Error researching company: {str(e)}")
            return f"Error retrieving company information: {str(e)}"

    def research_person(self, name, company=None, email=None):
        try:
            query = f"Information about {name}"
            if company:
                query += f" at {company}"
            if email:
                query += f" {email}"

            print(f"Researching person: {name}...")
            return self.tavily_client.get_search_context(
                query=query,
                search_depth="advanced",
                max_results=5
            )
        except Exception as e:
            print(f"Error researching person: {str(e)}")
            return f"Error retrieving person information: {str(e)}"

    def analyze_research(self, company_context, person_context, lead_info):
        try:
            PROMPT = f"""
            You are a business development analyst tasked with analyzing a new lead. Using the provided context and lead information,
            create a comprehensive research report that will help in understanding and approaching this potential client.

            Lead Information:
            {lead_info}

            Company Research Context:
            {company_context}

            Person Research Context:
            {person_context}

            Please provide a structured analysis with the following sections:
            1. Company Overview
               - Company background (founding date, location, legal status)
               - Services/Products (be specific about what they offer)
               - Market position (based on revenue, team size, and market presence)
               - Online presence (only include verifiable information like website, active social profiles)
               - Notable clients or projects (if found in the research data)

            2. Decision Maker Profile (Nicholas Delgado)
               - Professional background (verified roles and experience)
               - Role and responsibilities at the company
               - Online presence (only include active, verified profiles with meaningful information)
               - Notable achievements or mentions (only include if found in research data)

            3. Opportunity Analysis
               - Alignment with provided needs (AI PM system integration)
               - Potential pain points based on company size and industry
               - Specific value propositions
               - Potential challenges or competitors

            4. Recommended Approach
               - Key talking points
               - Specific solutions to propose
               - Relevant case studies or examples to reference

            5. Risk Assessment
               - Potential obstacles
               - Competition analysis
               - Budget considerations

            Important Guidelines:
            - Only include information that is directly supported by the research data
            - For online presence, focus on active and verifiable profiles/websites
            - Do not make assumptions about social media engagement or reach
            - If certain information is not found, state that it's not available rather than making assumptions

            Format the response in a clear, professional manner with bullet points where appropriate.
            Include relevant URLs or sources at the end of each section, but only if they are working links found in the research data.
            """

            print("Analyzing research data...")
            completion = self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": PROMPT,
                    }
                ],
                temperature=0.4,
                max_tokens=4000,
                model="gpt-4o-mini",
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error analyzing research data: {str(e)}")
            return f"Error analyzing research data: {str(e)}"

def main():
    try:
        # Lead information
        lead_info = {
            "name": "Nicholas Delgado",
            "email": "Nicholas@tna.associates",
            "company": "TNA associates",
            "position": "Owner",
            "revenue": "more_than_$1m/yr",
            "team_size": "5-25",
            "ai_needs": "Integrate with our PM system to expedite the delivery of assets from inception to deployment",
            "is_marketing_agency": True
        }

        # Initialize researcher
        researcher = LeadResearcher(tavily_client, openai_client)

        # Conduct research
        company_context = researcher.research_company(
            lead_info["company"],
            domain="tna.associates"
        )
        
        person_context = researcher.research_person(
            lead_info["name"],
            company=lead_info["company"],
            email=lead_info["email"]
        )

        # Analyze and generate report
        report = researcher.analyze_research(
            company_context,
            person_context,
            lead_info
        )

        # Print report
        print("\n=== LEAD RESEARCH REPORT ===\n")
        print(report)
    except Exception as e:
        print(f"An error occurred during research: {str(e)}")

if __name__ == "__main__":
    main()
