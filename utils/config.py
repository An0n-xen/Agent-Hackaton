search_op = """
    here is the format
    
    key : Search operators

    acquirer_identifier :  blank, contains, eq, includes, not_contains, not_eq, not_includes, starts
    
    aliases : blank, contains, eq, not_contains, not_eq, starts
    
    categories : blank, includes, includes_all, not_includes, not_includes_all
    
    closed_on : Date the organization was closed
    
    company_type : Whether an Organization is for profit or non-profit
    
    created_on : Date the organization was created
    
    delisted_on : The date when the Organization removed its stock from the stock exchange.
    
    demo_days : Whether an accelerator hosts any demo days
    
    description : Organization Description, Industries, Industry Groups
    
    diversity_spotlights : Types of diversity represented in an organization, specifically of those who are founding members, currently the CEO, or have check-writing abilities in an investment firm. This feature is in beta and may change with future updates.
    
    equity_funding_total : Total funding amount raised across all Funding Rounds excluding debt
    
    exited_on : Date the organization was acquired or went public
    
    founded_on : Date the Organization was founded
    
    founder_identifiers : Founders of the organization
    
    funding_stage : early_stage_venture, late_stage_venture, m_and_a, private_equity, seed, IPO
    
    funding_total : between, blank, eq, gt, gte, lt, lte, not_eq
    
    funds_total : between, blank, eq, gt, gte, lt, lte, not_eq
    
    identifier : Name of the Organization
    
    investor_identifiers : blank, includes, includes_all, not_includes, not_includes_all
    
    location_identifiers : blank, includes, includes_all,
    
    num_acquisitions : between, blank, eq, gt, gte, lt, lte, not_eq
    
    num_articles : between, blank, eq, gt, gte, lt, lte, not_eq
    
    num_employees_enum : blank, eq, includes, not_eq, not_includes
    
"""

parse_json_des = """
Extract the defined parameters from the given text and convert them into a JSON object. Use the descriptions to determine which key has its value in the text. Convert numbers represented in words (e.g., "25 million") to figures (e.g., 25000000). 

Below are the keys and their descriptions:

acquirer_identifier: Name of the organization that made the acquisition
aliases: Alternate or previous names for the organization
categories: Category the organization falls under, eg AI, biotech, Saas etc
closed_on: Date the organization was closed
company_type: Whether an Organization is for profit or non-profit
created_on: Date the organization was created
delisted_on: The date when the Organization removed its stock from the stock exchange.
demo_days: Whether an accelerator hosts any demo days
description: Organization Description, Industries, Industry Groups
diversity_spotlights: Types of diversity represented in an organization, specifically of those who are founding members, currently the CEO, or have check-writing abilities in an investment firm. This feature is in beta and may change with future updates.
equity_funding_total: Total funding amount raised across all Funding Rounds excluding debt
exited_on: Date the organization was acquired or went public
founded_on: Date the Organization was founded
founder_identifiers: Founders of the organization
funding_stage: This field describes an organization's most recent funding status (e.g. Early Stage Venture, Late Stage Venture, M&A). Possible values are: early_stage_venture, late_stage_venture, m_and_a, private_equity, seed, IPO
funding_total: Total amount raised across all funding rounds : Search Operators: between, blank, eq, gt, gte, lt, lte, not_eq
funds_total: Total funding amount raised across all Fund Raises
identifier: Name of the Organization
investor_identifiers: The top 5 investors with investments in this company
location_identifiers: Where the organization is headquartered
num_acquisitions: Total number of Acquisitions
num_articles: Number of news articles that reference the Organization
num_event_appearances : Total number of events an Organization appeared in or has attended (field type int)
num_employees_enum: Total number of employees. Possible values are: c_00001_00010 (maps to 1-10), c_00011_00050 (maps to 11-50), c_00051_00100 (maps to 51-100), c_00101_00250 (maps to 101-250), c_00251_00500 (maps to 251-500), c_00501_01000 (maps to 501-1000), c_01001_05000 (maps to 1001-5000), c_05001_10000 (maps to 5001-10000), c_10001_max (maps to 10001+)
operator_id: search operators like (blank), (contains),(between),(includes), (eq map to equal to), (gt map to greater than), (gte map to greater than or equal to), (lt map to less than), (lte map to less than or equal to), (ne map to not equal to).

Most of the keys have search operators like (blank), (contains), (between), (eq map to equal to), (gt map to greater than), (gte map to greater than or equal to), (lt map to less than), (lte map to less than or equal to), (ne map to not equal to).

Given a text, fill the defined parameters and leave the rest as null, convert number words to figures, and output it in a JSON format.

Note: all the parameters should be a string

With this task do not hallucination the text, wait for human input first before extracting 
"""

expected_format = """
    The output should be a json object in the form

{
  "field_ids": [
    "identifier",
    "categories",
    "location_identifiers",
    "short_description",
    "rank_org"
  ],
  "order": [
    {
      "field_id": "rank_org",
      "sort": "asc"
    }
  ],
  "query": [
    {
      "type": "predicate",
      "field_id": "funding_total",
      "operator_id": "between",
      "values": [
        {
          "value": 25000000,
          "currency": "usd"
        },
        {
          "value": 100000000,
          "currency": "usd"
        }
      ]
    },
    {
      "type": "predicate",
      "field_id": "location_identifiers",
      "operator_id": "includes",
      "values": [
        "6106f5dc-823e-5da8-40d7-51612c0b2c4e"
      ]
    },
  ],
  "limit": 10
}

 this is an example
 
 here is another example

{
  "field_ids": [
    "identifier",
    "categories",
    "location_identifiers",
    "short_description",
    "rank_org"
  ],
  "order": [
    {
      "field_id": "rank_org",
      "sort": "asc"
    }
  ],
  "query": [
    {
      "type": "predicate",
      "field_id": "num_employees_enum",
      "operator_id": "includes",
      "values": [
        "c_00101_00250"
      ]
    },
    {
      "type": "predicate",
      "field_id": "categories",
      "operator_id": "includes",
      "values": [
        "58842728-7ab9-5bd1-bb67-e8e55f6520a0"
      ]
    }
  ],
  "limit": 10
}

another one 
{
  "field_ids": [
    "identifier",
    "categories",
    "location_identifiers",
    "short_description",
    "rank_org"
  ],
  "order": [
    {
      "field_id": "rank_org",
      "sort": "asc"
    }
  ],
  "query": [
    {
      "type": "predicate",
      "field_id": "equity_funding_total",
      "operator_id": "includes",
      "values": [
        {
          "value": 50000000,
          "currency": "usd"
        }
      ]
    },
    {
      "type": "predicate",
      "field_id": "funding_total",
      "operator_id": "includes",
      "values": [
        {
          "value": 50000000,
          "currency": "usd"
        }
      ]
    },
    {
      "type": "predicate",
      "field_id": "location_identifiers",
      "operator_id": "includes",
      "values": [
        "San Francisco"
      ]
    },
    {
      "type": "predicate",
      "field_id": "num_event_appearances",
      "operator_id": "includes",
      "values": [
        5
      ]
    },
    {
      "type": "predicate",
      "field_id": "num_employees_enum",
      "operator_id": "includes",
      "values": [
        "c_00051_00100"
      ]
    }
  ],
  "limit": 10
}

"""

correct_format = """
Your job is to parse it correctly and ensure it is properly formatted as a single-line JSON string. 

Here is an example JSON string and its just and example to help you,  do no hallucinate values from this example:

    ```json
      {"field_ids": ["identifier", "categories", "location_identifiers", "short_description", "rank_org"], "order": [{"field_id": "rank_org", "sort": "asc"}], "query": [{"type": "predicate", "field_id": "equity_funding_total", "operator_id": "includes", "values": [{"value": 50000000, "currency": "usd"}]}, {"type": "predicate", "field_id": "funding_total", "operator_id": "includes", "values": [{"value": 50000000, "currency": "usd"}]}, {"type": "predicate", "field_id": "location_identifiers", "operator_id": "includes", "values": ["6106f5dc-823e-5da8-40d7-51612c0b2c4e"]}, {"type": "predicate", "field_id": "categories", "operator_id": "includes", "values": ["6a733ac8-b79c-e2d2-55b9-cc3d66435eb6"]}], "limit": 10}
    ```
    
    so with the example above, you should parse the above JSON string and output it in a well-formatted, single-line JSON string structure. Ensure that all the keys and values are properly indented and that the JSON string is valid.

    The output should be in a format like this:
    '
      {
    "field_ids": [
      "identifier",
      "categories",
      "location_identifiers",
      "short_description",
      "rank_org"
    ],
    "order": [
      {
        "field_id": "rank_org",
        "sort": "asc"
      }
    ],
    "query": [
      {
        "type": "predicate",
        "field_id": "num_employees_enum",
        "operator_id": "includes",
        "values": [
          "c_01001_05000"
        ]
      },
      {
        "type": "predicate",
        "field_id": "categories",
        "operator_id": "includes",
        "values": [
          "d82f9f46-8a29-6c2b-791c-8006474b7e42"
        ]
      },
      {
        "type": "predicate",
        "field_id": "location_identifiers",
        "operator_id": "includes",
        "values": [
          "528f5e3c-90d1-1111-5d1c-2e4ff979d58e"
        ]
      }
    ],
    "limit": 10
  }
  '
  notice how the expected output does not have ```json``` in front of it.
  what I mean is you json string should not have ```json{}``` but it should be '{}' and replace (```)
  with (')  format it as such 

Note: I say again the above is an example and not a real JSON string, do not hallucinate values.  
Remember, the input JSON string can vary, but the output should always be a correctly formatted JSON string.
"""

news_trend_sentiment = """
  Identify the Key Information: Identify the main points or events described in each news description.

  Identify Trends and Implications: Look for any trends, patterns, or implications related to the topic.

  Generate a Reflection: Based on the key information and identified trends, provide a reflection that highlights the significance of the data. This reflection should connect the data to broader themes or trends and consider its impact .

  Filter Articles:
  Include Articles with Clear VC Trends: Based on the reflections, include only those articles that clearly indicate a trend relevant to VC investments.

  Exclude Articles without Clear Trends: Ignore articles that do not provide clear insights or trends for VC investments.
  
  Develop Sourcing Strategies: Based on the summarized reflections, develop sourcing strategies for potential investment opportunities in the AI sector

  Example
  News description: Hackers accessed OpenAI's internal systems last year and stole messages about AI design, prompting security concerns.
  Reflection: OpenAI, a tech giant, is even being hacked, so cybersecurity for AI is important. 

  News description: Wallace Shawn's Father Ignatius tangles with technology in this scene from episode 9, "How to Build a Chatbot."
  Reflection: No clear trend for a VC. 

  News description: Stay up to date on the latest AI technology advancements and learn about the challenges and opportunities AI presents now and for the future.
  Reflection: No clear trend for a VC. 

  News description: A California judge dismissed many of the claims outlined in a copyright lawsuit that accuses GitHub, Microsoft, and OpenAI of copying developers’ code.
  Reflection: Governments are getting more sensitive about AI's impact on copyright, so making data copyrightable or enabling publishers to monetize their data for AI training are getting more important.

  Note: the above is just an example do not hallucinate news descriptions from the above example
  
  The results you output should be of the format
  News description: The actual news description
  Reflection: The reflection you had on the news description
"""

functions_description = [
    {
        "name": "getNewsDesc",
        "description": "Useful when you need to get the news descriptions ",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "the news topics presented"}
            },
        },
    }
]
